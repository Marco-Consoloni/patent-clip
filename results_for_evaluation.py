import os
import argparse
import json


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process the results and prepare them in a format suitable for evaluation.')
    parser.add_argument('--results_dir', type=str, default='/home/fantoni/marco/patent-clip/docker/results/A42B3-A62B18-H02K19-base',
                        help='Directory to read JSON files containing results for each query (separately).') 
    parser.add_argument('--output_dir', type=str, default='/home/fantoni/marco/patent-clip/docker/results_for_evaluation',
                        help='Directory to write JSON files containing results for all the queries of a CPC.')
    args = parser.parse_args() 

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)  

    results = {}
    for query in os.listdir(args.results_dir):
        query_path = os.path.join(args.results_dir, query)
        query_id = query.replace(".json", "")

        with open(query_path, "r") as f:
            data = json.load(f)
            text_documents_ids = [item["payload"]["doc_id"] for item in data.get("text")] # get patent_ids of document patents from the "text" section
            img_documents_ids = [item["payload"]["doc_id"] for item in data.get("image")] # get patent_ids of document patents from the "image" section
            joint_documents_ids = [item["payload"]["doc_id"] for item in data.get("joint")] # get patent_ids of document patents from the "image" section
            # Add to the dictionaries using the query as the key
            results[query_id] = {"text": text_documents_ids, "image": img_documents_ids, "joint": joint_documents_ids}

# Save the text_result dictionary to a JSON file
filename = os.path.basename(args.results_dir)
result_file = os.path.join(args.output_dir, f"{filename}.json")
with open(result_file, 'w') as f:
    json.dump(results, f, indent=4)
print(f"Saved results to: {result_file}")









