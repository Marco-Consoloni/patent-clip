import json
import os
from qdrant_client import QdrantClient, models 
from transformers import CLIPModel, CLIPProcessor
import torch
from tqdm import tqdm
from PIL import Image
import numpy as np

from src.model import PatentModel
from src.config import get_cfg

@torch.no_grad()
def do_query(*, client, model, processor, collection, device, text=None, image_path=None, top_n=5, apply_filter, joint=False, query_id, cls):
    
    # Takes either text OR image input (not both)
    if not joint and text is None and image_path is None:
        raise ValueError("Either text or image input must be provided for the query.")
    if not joint and text is not None and image_path is not None:
        raise ValueError("Cannot process both text and image unless joint=True")
    
    # Initilize a list to store text and image embeddings
    embeddings = []

    # Create ebedding of query text if provided
    if text:
        inputs = processor(
            text=[text],
            return_tensors="pt",
            truncation=True,
            padding='max_length',
            max_length=77
        ).to(device)
        outputs = model.get_text_features(**inputs)
        text_embedding = outputs.cpu().numpy()[0].tolist()
        embeddings.append(text_embedding)

    # Create ebedding of query image if provided
    if image_path:
        image = Image.open(image_path)
        inputs = processor(
            images=image,
            return_tensors="pt"
        ).to(device)
        outputs = model.get_image_features(pixel_values=inputs['pixel_values'])
        image_embedding = outputs.cpu().numpy()[0].tolist()
        embeddings.append(image_embedding)
    
    # Initialize filter_condition as None (default state when no filter is applied)  
    filter_condition = None 
    
    # Create filter condition if the filter is enabled 
    if apply_filter and query_id and cls:
        # The filter should meet the conditions listed in the 'should' block (OR logic)
        filter_condition = models.Filter(
            should=[
                models.FieldCondition(
                    key="query_id", match=models.MatchValue(value=query_id)
                ),
                models.FieldCondition(
                    key="cls", match=models.MatchExcept(**{"except": [cls]})
                )
            ]
         )

    # Prepare query vector
    if joint and len(embeddings) > 1:
        query_vector= np.sum(embeddings, axis=0).tolist() # sum text and image embeddings when both are present for joint queries
    else:
        query_vector = embeddings[0] # use single embedding for non-joint queries

    # Perform search
    search_results = client.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=top_n,
        query_filter=filter_condition
    )

    return search_results


def main():
    cfg = get_cfg()

    os.makedirs(cfg.query.paths.results, exist_ok=True)
    print(f"Using output folder: {cfg.query.paths.results}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    if not cfg.qdrant.memory:
        client = QdrantClient(path=cfg.qdrant.db)
    else:
        raise ValueError("Can't use Qdrant in memory here")

    # Load Model
    print(f"Using model {cfg.query.model}")
    if cfg.query.model == "base":
        model = CLIPModel.from_pretrained(cfg.model.base).to(device)
        processor = CLIPProcessor.from_pretrained(cfg.model.base)
    else:
        checkpoint = PatentModel.load_from_checkpoint(cfg.query.model, base_model=cfg.model.base)
        model = checkpoint.model.to(device) 
        processor = CLIPProcessor.from_pretrained(cfg.model.base)
    
    # Iterates through query files
    for query in tqdm(os.listdir(os.path.join(cfg.query.paths.query, cfg.query.cls))):
        fname = os.path.join(cfg.query.paths.query, cfg.query.cls, query)
        query_id = query.split(".")[0]

        with open(fname, "r") as f:
            data = json.load(f)

        text = data[cfg.query.fields.text]
        img_path = data[cfg.query.fields.image]

        text_results = do_query(
            client=client,
            collection="images",
            model=model,
            processor=processor,
            device=device,
            text=text,
            top_n=cfg.query.n,
            apply_filter = cfg.query.apply_filter,
            query_id = query_id,
            cls = cfg.query.cls

        )

        image_results = do_query(
            client=client,
            collection="text",
            model=model,
            processor=processor,
            device=device,
            image_path=img_path,
            top_n=cfg.query.n,
            apply_filter = cfg.query.apply_filter,
            query_id = query_id,
            cls = cfg.query.cls
        )

        joint_results = do_query(
            client=client,
            collection="joint",
            model=model,
            processor=processor,
            device=device,
            text=text,
            image_path=img_path,
            top_n=cfg.query.n,
            apply_filter = cfg.query.apply_filter,
            joint = cfg.query.joint,
            query_id = query_id,
            cls = cfg.query.cls
        )

        result = dict(
            text=[t.dict() for t in text_results],
            image=[i.dict() for i in image_results],
            joint=[j.dict() for j in joint_results]
        )

        json_fname = os.path.join(cfg.query.paths.results, f"{query_id}.json")        
        with open(json_fname, "w") as f:
            json.dump(result, f, indent=4)

if __name__ == "__main__":
    main()
