import os
import tarfile
import time
import argparse

# Define directory paths
tar_directory = '/vast/marco/Data/tar/'
zip_directory = '/vast/marco/Data/zip/'
os.makedirs(zip_directory, exist_ok=True) # Create the download directory if it doesn't exist


# Extract all the zip files from tar archive
def extract_zip_from_tar(tar_path, extract_to):
    
    with tarfile.open(tar_path, 'r') as tar:
        for member in tar.getmembers():
            if member.name.endswith('.ZIP'): # (case-sensitive)
                zip_filename = os.path.basename(member.name)
                zip_path = os.path.join(extract_to, zip_filename)

                # Check if the zip file already exists
                if not os.path.exists(zip_path):
                    member.name = zip_filename # Remove tar structure from member name
                    os.makedirs(extract_to, exist_ok=True)
                    tar.extract(member, path=extract_to) # Extract member in the specified directory
                    #print(f'{zip_filename} has been extracted.')
                # Do not perform the extraction of the zip
                else:
                    print(f'{zip_filename} already extracted.')



if __name__ == "__main__":
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Extract .ZIP files from .tar archives.')
    parser.add_argument('-t', '--tar_directory', type=str, default='/vast/marco/Data/tar/',
                        help='Directory containing TAR files.')
    parser.add_argument('-z', '--zip_directory', type=str, default='/vast/marco/Data/zip/',
                        help='Directory to extract ZIP files to.')

    # Parse arguments
    args = parser.parse_args()
    tar_directory = args.tar_directory
    zip_directory = args.zip_directory

    # Ensure the ZIP directory exists: create the download directory if it doesn't exist
    os.makedirs(zip_directory, exist_ok=True)

    # Iterate over the year subdirectories in the tar directory 
    for year in os.listdir(tar_directory):
        
        # Skip years from which all zip files have already been extracted.
        if year not in ['2020','2021', '2022', '2023']: # define the list manually
            start_time_year = time.time()
            year_path = os.path.join(tar_directory, year)

            # Iterate over the tar archives to extract zip files
            for tar in os.listdir(year_path):
                start_time_tar = time.time()
                tar_path = os.path.join(year_path, tar)
                extract_to = os.path.join(zip_directory, year, os.path.splitext(tar)[0]) # Extracting to a directory named after the file without extension
                print(f"Extracting: {tar}  ...")
                extract_zip_from_tar(tar_path, extract_to)
                end_time_tar = time.time()
                print(f'{tar} has been extracted.\t Elapsed time: {end_time_tar - start_time_tar:.2f}') # 50-60 sec (on average)
                # Uncomment the following line if you want to extract only one TAR per year
                #break

            end_time_year = time.time()
            print(f'Year: {year} has been extracted.\t Elapsed time: {end_time_year - start_time_year:.2f}')
            # Uncomment the following line if you want to extract only one full year
            #break
        else:
            print(f'Skipping year: {year}')