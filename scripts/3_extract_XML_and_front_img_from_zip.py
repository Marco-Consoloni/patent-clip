import os
import zipfile
import re
import argparse
import time

# reference: https://stackoverflow.com/questions/4917284/extract-files-from-zip-without-keeping-the-structure-using-python-zipfile
def extract_from_zip(zip_path, extract_to, endswith: str):
    """
    Extract files from a zip archive, ignoring subfolder structures,
    and only extracting files that end with specified extensions.

    Parameters:
    zip_path (str): Path to the zip archive.
    extract_to (str): Directory where files should be extracted.
    endswith (str): File extension to filter by. Must be either '.XML' (XML file) or '-D00000.TIF'(front_image).
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for zip_info in zip_ref.infolist(): 
                if zip_info.is_dir(): # Skip directories
                    continue
                zip_info.filename = os.path.basename(zip_info.filename) 
                
                # Check if the file has the specified extension
                if zip_info.filename.endswith(endswith):
                    try:
                        # Create the full path for the extracted file
                        file_path = os.path.join(extract_to, zip_info.filename) 
                        # Extract the file if it doesn't already exist
                        if not os.path.exists(file_path):
                            zip_ref.extract(zip_info, extract_to)
                            #print(f"{zip_info.filename} extracted to '{extract_to}'")
                        else:
                            print(f'{zip_info.filename} already extracted.')
                    
                    except KeyError:
                        print(f"{zip_info.filename} not found in the ZIP archive")
                    
                    except Exception as e:
                        print(f"An error occurred while extracting {zip_info.filename}: {e}")
    
    except zipfile.BadZipFile:
        print(f"Error: The file at {zip_path} is not a valid ZIP file.")



if __name__ == "__main__":

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Extract XML and fron images files from .ZIP file.')
    parser.add_argument('-z', '--zip_directory', type=str, default='/vast/marco/Data/zip/',
                        help='Directory containing ZIP files.')
    parser.add_argument('-x', '--xml_directory', type=str, default='/vast/marco/Data/XML/',
                        help='Directory to extract XML files to.')
    parser.add_argument('-i', '--image_directory', type=str, default='/vast/marco/Data/front_imgs/',
                        help='Directory to extract front image files to.')

    # Parse arguments
    args = parser.parse_args()
    zip_directory = args.zip_directory
    XML_directory = args.xml_directory
    front_imgs_directory = args.image_directory

    # Ensure the output directories exist: create the directory if it doesn't exist
    os.makedirs(XML_directory, exist_ok=True)
    os.makedirs(front_imgs_directory, exist_ok=True)

    # Iterate over the year subdirectories of the zip directory
    for year in os.listdir(zip_directory):

        # Skip years from which XML and front image files have already been extracted.
        if year not in ['2021', '2022', '2023', '2024']: # define the list manually
            year_path = os.path.join(zip_directory, year)
            start_time_year = time.time()

            # Iterate over the .tar archives
            for tar in os.listdir(year_path):
                start_time_tar = time.time()
                print(f"Extracting: {tar} ...")
                tar_path = os.path.join(year_path, tar)

                # Iterate over the zip files in the tar folder
                for zip_file in os.listdir(tar_path): 
                    zip_path = os.path.join(tar_path, zip_file) # create path to  the zip file
                    
                    # Extract only Utility Patents (Excluding Design patents ---> USD1010240-20240102.ZIP)
                    # skip file using: "and not re.match(r'^US10525031-20200107.ZIP', zip_file)"
                    if re.match(r'^US\d{8}-\d{8}.ZIP', zip_file):
                        XML_extract_to = os.path.join(XML_directory, year, tar)
                        front_img_extract_to = os.path.join(front_imgs_directory, year, tar)
                        extract_from_zip(zip_path, XML_extract_to, '.XML')
                        extract_from_zip(zip_path, front_img_extract_to, '-D00000.TIF')
                        # Uncomment the following line to extract XML and fron image of only one ZIP file
                        #break
                    else:
                        print(f"Not correct format for ZIP filename: {zip_file}")
                        continue
            
                end_time_tar = time.time()
                print(f'{tar} has been extracted.\t Elapsed time: {end_time_tar - start_time_tar:.2f}')
                # Uncomment the following line to extract XMLs and front images of only one tar (i.e., from all zip files in the tar)
                #break 

            end_time_year = time.time()
            print(f'Year: {year} has been extracted.\t Elapsed time: {end_time_year - start_time_year:.2f}')
            # Uncomment the following line to extract XMLs and front images of only one year (i.e., from all the tar archives of the year)
            #break 
        
        else:
            print(f'Skipping year: {year}')