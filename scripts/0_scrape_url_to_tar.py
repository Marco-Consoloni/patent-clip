import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def scrape_urls_to_tar_archives(urls, output_file):
    # Clear the output file content
    with open(output_file, 'w') as file:
        file.write('')  

    # Iterate over the URLs
    for url in urls: # Send a GET request to the webpage
        response = requests.get(url)
        if response.status_code == 200: # Check if the request was successful
            soup = BeautifulSoup(response.content, 'html.parser') # Parse the HTML content using BeautifulSoup
            links = soup.find_all('a') # Find all 'a' tags (which define hyperlinks) on the page

            # Open the output file in append mode
            with open(output_file, 'a') as file:
                # Extract and write the full URL of each link to the file
                for link in links:
                    href = link.get('href')
                    if href and re.search(r'\d{8}\.tar$', href): # serch for tar file formatted such as I20240312.tar
                        full_url = urljoin(url, href)
                        file.write(full_url + '\n')
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")



# Runs only if the script is executed directly, not when imported as a module
if __name__ == "__main__":

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Scrape URLS to .tar file from specified pages.')

    # Add argument for the list of URLs from which to extract .tar file URLs
    parser.add_argument('-u', '--urls', metavar='URL', type=str, nargs='+', default=[
        'https://bulkdata.uspto.gov/data/patent/grant/redbook/2024/',
        'https://bulkdata.uspto.gov/data/patent/grant/redbook/2023/',
        'https://bulkdata.uspto.gov/data/patent/grant/redbook/2022/',
        'https://bulkdata.uspto.gov/data/patent/grant/redbook/2021/',
        'https://bulkdata.uspto.gov/data/patent/grant/redbook/2020/'
        ],  help='A list of URLs to scrape.')
    
    # Add an optional argument for the output file path with a default value
    parser.add_argument('-o', '--output', type=str, default='/vast/marco/Data/urls_to_tar.txt', help='Output file path for the URLs. of .tar files')
    
    # Parse arguments
    args = parser.parse_args()
    urls = args.urls
    output_file = args.output

    # Call the scraping function with parsed arguments
    scrape_urls_to_tar_archives(urls, output_file)