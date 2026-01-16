import os
import json
import re
import time
import argparse
import scraping_functions_XML


def create_json_from_XML(XML_directory, front_imgs_directory, json_directory):

    # Iterate over the sub directories (tar) of the XML directory
    for year in os.listdir(XML_directory):
        
        # Skip years from which XML and front image files have already been extracted.
        if year not in ['2020','2021', '2022']: # define the list manually
            start_time_year = time.time()
            year_path = os.path.join(XML_directory, year)

            for tar in os.listdir(year_path):
                print(f"Creating JSON for tar: {tar} ...")
                tar_path = os.path.join(year_path, tar)
            
                start_time_tar = time.time()
                tar_dict = {}

                json_filename = tar + '.json'
                json_filepath = os.path.join(json_directory, year, json_filename)
                
                # Check if the json file already exists
                if os.path.exists(json_filepath):
                    print(f"File already exists: {json_filepath}\t Skipping tar: {tar}.")
                    continue
                
                # Iterate over the XML file of each tar archive
                for XML_file in os.listdir(tar_path): 
                    XML_path = os.path.join(tar_path, XML_file) # create path to the zip file
                    XML_file_root = os.path.splitext(XML_file)[0] # remove XML extension from XML file name

                    # Check the format of the XML filename
                    if re.match(r'^US\d{8}-\d{8}.XML$', XML_file):
                        
                        # Extract year from XML file name to create corresponding subdirectory
                        year = XML_file[11:15]

                        # Create the year directory for json files if it doesn't exist
                        json_year_directory = os.path.join(json_directory, str(year))
                        os.makedirs(json_year_directory, exist_ok=True)

                        # Dictionary initialization
                        xml_dict = {
                            'PNs': None,
                            'IPC_class': None,
                            'CPC_class': None,
                            'title': None,
                            'abstract': None,
                            'description_of_drawings': None,
                            'first_claim': None,
                            'front_img_metadata': None,
                            'front_img': None
                        }

                        # Parse the XML and get the root node
                        root = scraping_functions_XML.parse_XML_file(XML_path)  
                        if root:
                            xml_dict['PNs'] = scraping_functions_XML.get_publication_numbers(XML_path, root)
                            xml_dict['IPC_class'] = scraping_functions_XML.get_patent_class(XML_path, root, 'classification-ipcr')
                            xml_dict['CPC_class'] = scraping_functions_XML.get_patent_class(XML_path, root, 'classification-cpc')
                            xml_dict['title'] = scraping_functions_XML.get_title(XML_path, root)
                            xml_dict['abstract'] = scraping_functions_XML.get_abstract(XML_path, root)
                            xml_dict['description_of_drawings'] = scraping_functions_XML.get_description_of_drawings_paragraph_text(XML_path, root)
                            xml_dict['first_claim'] = scraping_functions_XML.get_first_claim(XML_path, root)
                            xml_dict['front_img_metadata'] = scraping_functions_XML.get_front_img_metdata(XML_path, root)

                            # Creating front image path
                            front_img_name = XML_file_root + "-D00000.TIF"
                            front_img_path = os.path.join(front_imgs_directory, year, tar, front_img_name)

                            # Check if the full path to the corresponding front image exists
                            if os.path.exists(front_img_path):
                                xml_dict['front_img'] = front_img_path

                                # Append the data extracted from the XML (xml_dict) to the dictionary of the tar file
                                tar_dict[XML_file_root] = xml_dict 
                            else:
                                #print(f"{front_img_path} not exist.") # do not store the data
                                continue

                    else:
                        #print(f"Not standard XML filename: {XML_file}")
                        continue
                
                # Creating json file for each tar file (i.e., dump the content of the dictionary created for tar)
                with open(json_filepath, 'w') as json_file:
                    json.dump(tar_dict, json_file, indent = 4) 
                
                end_time_tar = time.time()
                print(f"{json_filename} file created.\t Elapsed time: {end_time_tar - start_time_tar:.2f}") # Print the json file creation result and extraction time
                # Uncomment the following line to create a JSON file for only one tar
                #break 

            end_time_year = time.time()
            print(f'All JSON has been created for year: {year}.\t Elapsed time: {end_time_year - start_time_year:.2f}')
            # Uncomment the following line to create a JSON file for only one year (i.e., for all the tar archives contained in the year)
            #break 
        
        else:
            print(f'Skipping year: {year}')
        


if __name__ == "__main__":

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process XML files from zip files and generate JSON output.')
    parser.add_argument('-x', '--xml_directory', type=str, default='/vast/marco/Data/XML/',
                        help='Directory containing XML files.')
    parser.add_argument('-f', '--front_imgs_directory', type=str, default='/vast/marco/Data/front_imgs/',
                        help='Directory containing front images.')
    parser.add_argument('-j', '--json_directory', type=str, default='/vast/marco/Data/json',
                        help='Directory to store JSON output files.')

    # Parse arguments
    args = parser.parse_args()
    XML_directory = args.xml_directory
    front_imgs_directory = args.front_imgs_directory
    json_directory = args.json_directory

    # Ensure the output directories exist
    os.makedirs(json_directory, exist_ok=True)

    # Process the XML to create JSON file
    create_json_from_XML(XML_directory, front_imgs_directory, json_directory)