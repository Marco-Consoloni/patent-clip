import os
import json
import random
import argparse
import time
from tqdm import tqdm

def merge_json_files(json_directory):
    all_files = []  # Initialize an empty list to store file names

    # Traverse through the directory
    for root, _, files in os.walk(json_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"Accessing JSON: {file} ...")
                all_files.append(file_path)

    return all_files

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Split JSON file paths into train, evaluation, and test set.')
    parser.add_argument('-j', '--json_directory', type=str, default='/vast/marco/Data/json',
                        help='Directory containing JSON files.')
    parser.add_argument('-d', '--data_directory', type=str, default='/vast/marco/Data/',
                        help='Directory containing the data')
    parser.add_argument('--train_ratio', type=float, default=0.8,
                        help='Ratio of data to use for training set.')
    parser.add_argument('--eval_ratio', type=float, default=0.1,
                        help='Ratio of data to use for evaluation set.')
    parser.add_argument('--seed', type=int, default=1999,
                        help='Random seed for shuffling data.')

    # Parse arguments
    args = parser.parse_args()
    json_directory = args.json_directory
    train_ratio = args.train_ratio
    eval_ratio = args.eval_ratio
    seed = args.seed

    # Create datasets directory if it doesn't exist
    datasets_dir = os.path.join(args.data_directory, 'datasets')
    os.makedirs(datasets_dir, exist_ok=True)

    # Create train, eval, and test directories
    train_dir = os.path.join(datasets_dir, 'train')
    eval_dir = os.path.join(datasets_dir, 'eval')
    test_dir = os.path.join(datasets_dir, 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Merge JSON file names into a list
    start_time_merge = time.time()
    all_files = merge_json_files(json_directory)
    end_time_merge = time.time()
    print(f'All file names have been collected.\tElapsed time: {end_time_merge - start_time_merge:.2f}')

    print("Reading files..")
    all_entries = []
    for file in tqdm(all_files):
        with open(file, "r") as f:
            content = json.load(f)
        all_entries.extend(list(content.items()))
    
    print(f'Total entries collected: {len(all_entries)}')

    # Shuffle all entries using the provided seed
    random.seed(seed)
    random.shuffle(all_entries)

    # Determine the split sizes
    total_entries = len(all_entries)
    train_size = int(total_entries * train_ratio)
    eval_size = int(total_entries * eval_ratio)
    test_size = total_entries - train_size - eval_size

    # Split the entries into train, eval, and test sets
    train_set = all_entries[:train_size]
    eval_set = all_entries[train_size:train_size + eval_size]
    test_set = all_entries[train_size + eval_size:]

    # Save the entries into respective folders
    print("Saving train set...")
    for id, entry in tqdm(train_set):
        save_json(entry, os.path.join(train_dir, f'{id}.json'))

    print("Saving eval set...")
    for id, entry in tqdm(eval_set):
        save_json(entry, os.path.join(eval_dir, f'{id}.json'))

    print("Saving test set...")
    for id, entry in tqdm(test_set):
        save_json(entry, os.path.join(test_dir, f'{id}.json'))

    print("Data split and saved successfully!")
