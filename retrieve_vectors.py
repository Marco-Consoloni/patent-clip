from qdrant_client import QdrantClient
from tqdm import tqdm
from src.config import get_cfg
import numpy as np
import numpy as np
import csv
import os
import pickle

def get_all_vectors(client, collection_name):
    """
    Retrieve vectors from Qdrant return them as a list of numpy array.
    reference: https://qdrant.tech/documentation/concepts/points/?q=client.scroll
    """
    collection_info = client.get_collection(collection_name)
    total_points = collection_info.points_count
    vectors = []
    payloads = []
    
    with tqdm(total=total_points, desc="Retrieving Vectors", unit="point") as pbar:
        response = client.scroll(
            collection_name=collection_name,
            limit=total_points,
            with_payload=True,
            with_vectors = True
            )
        points, __ = response
        for point in points:
            if point.vector is not None and point.payload is not None:
                vectors.append(point.vector)
                payloads.append((point.payload.get('doc_id', None),
                                 point.payload.get('cls', None),
                                 point.payload.get('text', None),
                                 point.payload.get('img_path', None),
                                 point.payload.get('collection_name', None)
                                 ))
        pbar.update(len(points))

    print(f"Total vectors retrieved: {len(vectors)}")
    return np.array(vectors), payloads


def main():
    cfg = get_cfg()

    if not cfg.qdrant.memory:
        print(f"Using db {cfg.qdrant.db}")
        client = QdrantClient(path=cfg.qdrant.db)
    else:
        client = QdrantClient(":memory:")

    # Retrieve vectors and pyloads
    vectors, payloads = get_all_vectors(client = client, collection_name = cfg.retrieve.collection)

    # Create output directory and file path to save vectors and pyloads
    os.makedirs(cfg.retrieve.paths.vectors, exist_ok=True)
    print(f"Using output folder: {cfg.retrieve.paths.vectors}")
    pickle_output_path = os.path.join(cfg.retrieve.paths.vectors, f"{cfg.retrieve.cls}-{cfg.retrieve.collection}.pkl")

    # Save vectors and payloads in a pickle file
    with open(pickle_output_path, "wb") as pkl_file:
        pickle.dump({"vectors": vectors, "payloads": payloads}, pkl_file)
    print(f"Vectors and payloads saved to {pickle_output_path}")


if __name__ == "__main__":
    main()