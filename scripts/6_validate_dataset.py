import os
import json
import argparse
from PIL import Image
from multiprocessing import Pool, cpu_count

def check_image(json_file, image_key):
    try:
        with open(json_file, 'r') as f:
            metadata = json.load(f)
        image_path = metadata[image_key]

        if not os.path.isabs(image_path):
            json_dir = os.path.dirname(json_file)
            image_path = os.path.join(json_dir, image_path)

        image = Image.open(image_path)
    except Exception as e:
        print(f"Failed to open image for JSON file: {json_file}. Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Check images from JSON files.')
    parser.add_argument('json_dir', help='Directory containing JSON files.')
    parser.add_argument('--image-key', default='front_img', help='Key in JSON for image path.')
    parser.add_argument('--processes', type=int, default=cpu_count(), help='Number of processes.')
    args = parser.parse_args()

    json_dir = args.json_dir
    image_key = args.image_key
    num_processes = args.processes

    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]

    pool_args = [(json_file, image_key) for json_file in json_files]

    with Pool(processes=num_processes) as pool:
        pool.starmap(check_image, pool_args)

if __name__ == '__main__':
    main()
