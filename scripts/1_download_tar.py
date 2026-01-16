import os
import requests
import time
import re
import argparse


def download_tar_files(tar_urls, tar_directory):

    # Create the download directory if it doesn't exist
    os.makedirs(tar_directory, exist_ok=True)

    # Iterate over tar urls to download .tar archives 
    for tar_url in tar_urls:
        start_time = time.time()
        tar_url = tar_url.strip()
        tar_filename = os.path.basename(tar_url)

        # Check for tar name format
        if re.match(r'^I\d{8}.tar$', tar_filename):
            year = tar_filename[1:5] # Extract year from tar filename to create corresponding subdirectory
        else:
            print(f"Not standard tar filename: {tar_filename}")
            continue

        # Create the year directory if it doesn't exist
        tar_year_directory = os.path.join(tar_directory, year)
        os.makedirs(tar_year_directory, exist_ok=True)

        # Defining full path to the tar file
        tar_filepath = os.path.join(tar_year_directory, tar_filename)
        temp_filepath = tar_filepath + ".tmp" # Temporary file path

        # Check if the tar is already present in the directory.
        if os.path.exists(tar_filepath):
            print(f"File already exists: {tar_filepath}\t Skipping download.")
            continue  # Skip to the next tar_url

        try:
            response = requests.get(tar_url, stream=True)  # Send a GET request to download the tar file
            if response.status_code == 200: # Check if the request was successful
                print(f"Downloading: {tar_filename}\t ...")
                with open(temp_filepath, 'wb') as tar_file: # Write the temporary tar file to the download directory
                    for chunk in response.iter_content(chunk_size=8192):
                        tar_file.write(chunk) 
                # Rename the temporary file if the download was succesful
                os.rename(temp_filepath, tar_filepath)
                end_time = time.time()
                print(f"{tar_filename} has been downloaded\t Elapsed time: {end_time - start_time:.2f}")
                #break # extract only one tar file then stop
            else:
                print(f"Failed to download: {tar_url}\t Status code: {response.status_code}")
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath) # Remove temporary file if the download wasn't successful
                    
        except Exception as e:
            print(f"An error occurred while downloading {tar_url}: {str(e)}")
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath) # Remove temporary file if an exception occurs



if __name__ == "__main__":

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Download .tar files from specified URLs.')
    
    # Add argument for the file containing the list of URLs to .tar archives
    parser.add_argument('-i', '--input', type=str, default='/vast/marco/Data/urls_to_tar.txt',
                        help='Input file path containing URLs to download .tar files.')
    
    # Add argument for the download directory
    parser.add_argument('-o', '--output', type=str, default='/vast/marco/Data/tar/',
                        help='Directory to save downloaded .tar files.')
    
    # Pars arguments
    args = parser.parse_args()
    path_to_tar_urls = args.input
    tar_directory = args.output

    # Read the file .txt containing the URLs to tar files
    with open(path_to_tar_urls, 'r') as file:
        tar_urls = file.readlines()

    # Call the function to download tar files
    download_tar_files(tar_urls, tar_directory)