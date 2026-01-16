
# Define the functions to parse the XML files and scrape the data from them
# For XML Path synax see: https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax
import re
import xml.etree.ElementTree as ET


def parse_XML_file(file_path):
  '''The function read and parse .XML files. Then return its root.'''
  try:
    with open(file_path, 'r') as file:
      tree = ET.parse(file)
      root = tree.getroot()
      return root
  except Exception as e:
    print(f"Error processing PARSING {file_path}: {e}")
    return None


def get_title(file_path, root):
  try:
    node = root.find(".//invention-title")  
    invention_title = node.text
    invention_title = re.sub(r'\s+', ' ', invention_title).strip() # Clean the extracted text
    return invention_title
  except Exception as e:
    print(f"Error processing TITLE {file_path}: {e}")
    return None


def get_publication_numbers(file_path, root):
  try:
    target_tag = 'document-id' # Define the tag whose children's text you want to extract
    publication_numbers = [] # Initialize a empty list to store the publication numbers

    # Iterate through all elements in the XML tree matched by the target tag
    for element in root.iter(target_tag):
      children_text = "" # Initialize an empty list to store text for specific children

      # Iterate through the children of the target tag
      for child in element:
          # Check if the child's tag is in the list of tags to extract
          if child.tag in ['country', 'doc-number', 'kind']:
              children_text += child.text if child.text else None
      publication_numbers.append(children_text)

    return publication_numbers # retrun a list with all the PNs

  except Exception as e:
    print(f"Error processing PNs {file_path}: {e}")
    return None
  

def get_patent_class(file_path, root, classification_type):
  '''
  The function scrape all patnet classes from an XML file.
  the argument classification_type is a string, which selects the CPC or IPC classification.
  it takes the values: 'classification-ipcr' or 'classification-cpc'.
  '''
  try:
    target_tag =  classification_type  # Define the tag whose children's text you want to extract
    classes = [] # Initialize a empty list to store the IPCs (or CPCs classes)

    # Iterate through all elements in the XML tree matched by the target tag
    for element in root.iter(target_tag):
      children_text = "" # Initialize an empty list to store text for specific children

      # Iterate through the children of the target tag
      for child in element:
          # Check if the child's tag is in the list of tags to extract
          if child.tag in ['section', 'class', 'subclass', 'main-group', 'subgroup']:
              children_text += child.text if child.text else None
      classes.append(children_text)

    return classes # retrun a list with all the IPCs
  
  except Exception as e:
    print(f"Error processing PATENT CLASSES {classification_type} {file_path}: {e}")
    return None


def get_abstract(file_path, root):
  try:
    node = root.find(".//abstract")
    abstract_text = "".join(list(node.itertext())) # Get all the text of the sub-tree of the node
    abstract_text = re.sub(r'\s+', ' ', abstract_text).strip()  # Clean the extracted text
    return abstract_text
  except Exception as e:
    print(f"Error processing ABSTRACT {file_path}: {e}")
    return None
  

def get_first_claim(file_path, root):
  try:
    first_claim = root.find(".//claims/claim/[@num='00001']") # get the first claim the extracted text
    claim_text = "".join(list(first_claim.itertext()))
    claim_text = re.sub(r'\s+', ' ', claim_text).strip()  
    return claim_text
  except Exception as e:
    print(f"Error processing FIRST CLAIM {file_path}: {e}")
    return None


def get_description_of_drawings_paragraph_text(file_path, root):
    '''
    The function scrape the description of drawings section (i.e., <description-of-drawing> XML node) and return 
    a list of the paragraphs of the section which contain at least one figref node.
    '''
    try:
        # Initilize empy list to store scraped data
        paragphs_list = [] 

        # Iterate over the paragphs of the desription-of-drawing section
        paragphs = root.findall(".//description-of-drawings/p")  
        for paragph in paragphs:
            paragph_text = "".join(list(paragph.itertext()))  # get the text of the paragph and the number of the paragph

            # Chek if some <figref> nodes are present in the paragph 
            if paragph.findall(".//figref"):
              paragphs_list.append(paragph_text)

        return paragphs_list
    
    except Exception as e:
      print(f"Error processing DESCRIPTION OF DRAWINGS SECTION TEXT {file_path}: {e}")
      return None


def get_front_img_metdata(file_path, root):
    try:
        # Find the <img> node of the fron image using the attribute id
        front_img_node = root.find(".//drawings/figure/img[@id='EMI-D00000']")
        return front_img_node.attrib
    except Exception as e:
        #print(f"Error processing FRONT IMAGE METADATA {file_path}: {e}")
        return None

  
  
  