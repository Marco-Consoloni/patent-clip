import json
import os
from qdrant_client import QdrantClient, models 
from transformers import CLIPModel, CLIPProcessor
import torch
from tqdm import tqdm
from PIL import Image
import uuid

from src.model import PatentModel
from src.config import get_cfg

@torch.no_grad()
def ingest(*, cfg, client, model, processor, path, cls, device):

    # Document Processing Loop
    for patent in tqdm(os.listdir(os.path.join(path, cls))):
        fname = os.path.join(path, cls, patent)
        doc_id = patent.split(".")[0] # remove .json extension from patent filename

        # Split patent filename to get query and patent ID 
        # This step raises error if the filename is not in the format: "queryID_documentID.json"
        query_id = f"{doc_id.split('_')[0]}_{doc_id.split('_')[1]}"
        patent_id = doc_id.split('_')[2]

        with open(fname, "r") as f:
            data = json.load(f)

        text = data[cfg.query.fields.text]
        img_path = data[cfg.query.fields.image]
        image = Image.open(img_path)

        # CLIP Processing
        inputs = processor(
            text=[text],
            images=image,
            return_tensors="pt",
            truncation=True,
            padding='max_length',
            max_length=cfg.model.max_length
        ).to(device)

        # Embedding Generation
        with torch.no_grad():
            outputs = model(**inputs)

        text_embedding = outputs.text_embeds.cpu().numpy()[0].tolist()
        image_embedding = outputs.image_embeds.cpu().numpy()[0].tolist()
        joint_embedding = (outputs.text_embeds + outputs.image_embeds).cpu().numpy()[0].tolist()

        # Database Storage
        client.upsert(collection_name="text", points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=text_embedding,
                payload=dict(
                    patent_id=patent_id,
                    query_id = query_id,
                    doc_id = doc_id,
                    path=path,
                    cls=cls,
                    text=text,
                    img_path=img_path,
                    collection_name = "text"
                )
            )
        ])

        client.upsert(collection_name="images", points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=image_embedding,
                payload=dict(
                    patent_id=patent_id,
                    query_id = query_id,
                    doc_id = doc_id,
                    path=path,
                    cls=cls,
                    text=text,
                    img_path=img_path,
                    collection_name = "images"
                )
            )
        ])

        client.upsert(collection_name="joint", points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=joint_embedding,
                payload=dict(
                    patent_id=patent_id,
                    query_id = query_id,
                    doc_id = doc_id,
                    path=path,
                    cls=cls,
                    text=text,
                    img_path=img_path,
                    collection_name = "joint"
                )
            )
        ])


def main():
    cfg = get_cfg()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    if not cfg.qdrant.memory:
        print(f"Using db {cfg.qdrant.db}")
        client = QdrantClient(path=cfg.qdrant.db)
    else:
        client = QdrantClient(":memory:")

    # Database Initialization
    collection_names = ["images", "text", "joint"]
    for collection_name in collection_names:
        try:
            collection = client.get_collection(collection_name)
        except:
            collection = None
        if not collection:
            print(f"Collection {collection_name} does not exist, creating...")
            client.create_collection(collection_name, vectors_config={"size": 512, "distance": "Cosine"})

    # Model Loading
    print(f"Using model {cfg.query.model}")
    if cfg.query.model == "base":
        model = CLIPModel.from_pretrained(cfg.model.base).to(device)
        processor = CLIPProcessor.from_pretrained(cfg.model.base)
    else:
        checkpoint = PatentModel.load_from_checkpoint(cfg.query.model, base_model=cfg.model.base)
        model = checkpoint.model.to(device) 
        processor = CLIPProcessor.from_pretrained(cfg.model.base)

    ingest(
        cfg=cfg,
        client=client,
        model=model,
        processor=processor,
        path=cfg.query.paths.documents,
        cls=cfg.query.cls,
        device=device
    )

if __name__ == "__main__":
    main()
