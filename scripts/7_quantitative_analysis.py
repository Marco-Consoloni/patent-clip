import os 
import json
import statistics
import argparse

# Counts number of files in a certain directory
# and calculates total size
def get_file_count_and_size(directory, extension):
    
    total_size = 0
    total_files = 0

    # Iterate through all directories
    for root, _, files in os.walk(directory):
        for file in files:
            # Check file extension
            if any(file.endswith(ext) for ext in extension):
                total_files += 1
                total_size += os.path.getsize(os.path.join(root, file))

    return total_files, total_size

# Reads JSON files and counts
# - how many entries
# - entries with an existing image
# - average length of textual elements
def analyze_json_content(json_directory):

    text_lengths = {
        'title': [],
        'abstract': [],
        'first_claim': [],
        'description_of_drawings': []
    }

    entries_count = 0   # Counts total entries
    images_count = 0    # Counts total images

    # Iterate through JSON directory
    for root, _, files in os.walk(json_directory):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)     # Load JSON content
                for _, entry in data.items():
                    entries_count += 1

                    # Calculate text lengths
                    if entry.get("title"):
                        text_lengths['title'].append(len(entry["title"]))
                    if entry.get("abstract"):
                        text_lengths['abstract'].append(len(entry["abstract"]))
                    if entry.get("first_claim"):
                        text_lengths['first_claim'].append(len(entry["first_claim"]))
                    if entry.get("description_of_drawings") and isinstance(entry["description_of_drawings"], list):
                        total_paragraph_text = " ".join(entry["description_of_drawings"])
                        text_lengths['description_of_drawings'].append(len(total_paragraph_text))

                    # Checks for image validity and adds it to total
                    if entry.get("front_img") and os.path.exists(entry["front_img"]):
                        images_count += 1
    
    return entries_count, images_count, text_lengths

# Prints number of files and and total size (MB)
def print_stats(name, count, size_bytes):

    size_MB = size_bytes / (1024 * 1024)    # Converts from bytes to megabytes
    print(f"{name}:")
    print(f"  - Count: {count}")
    print(f"  - Total size: {size_MB:.2f} MB")


def main():

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Quantitative analysis of the dataset.')

    parser.add_argument('--json_dir', type=str, default='/vast/marco/Data/json',
                        help='Directory with JSON files.')
    parser.add_argument('--xml_dir', type=str, default='/vast/marco/Data/XML',
                        help='Directory with XML files.')
    parser.add_argument('--img_dir', type=str, default='/vast/marco/Data/front_imgs',
                        help='Directory with front images.')
    args = parser.parse_args()

    print("\n Analyzing files...")

    # Count number of JSON files and their size
    json_count, json_size = get_file_count_and_size(args.json_dir, ['.json'])

    # Count number of XML files and their size
    xml_count, xml_size = get_file_count_and_size(args.xml_dir, ['.XML'])

    # Count number of TIF images and their size
    img_count, img_size = get_file_count_and_size(args.img_dir, ['.TIF'])

    # Print stats
    print_stats("JSON files", json_count, json_size)
    print_stats("XML files", xml_count, xml_size)
    print_stats("TIF images", img_count, img_size)

    # Analyze and print JSON content
    print("\nAnalyzing JSON content...")

    entries, imgs, text_lengths = analyze_json_content(args.json_dir)

    print(f"Total entries in dataset: {entries}")
    print(f"Entries with valid image paths: {imgs}")

    # Calculate and print average + std dev of text lengths
    for field, lengths in text_lengths.items():
        if lengths:
            avg_len = sum(lengths) / len(lengths)
            std_len = statistics.stdev(lengths) if len(lengths) > 1 else 0.0
            min_len = min(lengths)
            max_len = max(lengths)
            print(f"{field}:")
            print(f"  - Average length: {avg_len:.2f} characters")
            print(f"  - Standard deviation: {std_len:.2f} characters")
            print(f"  - Min length: {min_len} characters")
            print(f"  - Max length: {max_len} characters")
            
        else:
            print(f"No data found for {field}")


if __name__ == "__main__":
    main()