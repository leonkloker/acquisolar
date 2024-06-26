import fitz  # PyMuPDF
import os
from openai import OpenAI
import requests
import json
import tiktoken
import zipfile
import shutil
from tqdm import tqdm


"""Testing functionality"""
#save text file for testing
def save_txt_file(title, contents, enable_testing_output = False):
    # Create a directory if it doesn't exist
    if enable_testing_output == True:
        folder_name = "classification_testing(can_be_deleted)"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Write the response content to a file inside the folder
        file_path = os.path.join(folder_name, title)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(contents)

"""Initializing file paths"""
#set root directory
def set_root_directory():
    # Get the directory where the current script resides
    root_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_directory)
    print("Root directory set to:", root_directory)
    return root_directory
# Function to construct relative paths for input and output directories
def construct_relative_paths(root_directory):
    input_dir = os.path.join(root_directory, "documents")
    output_dir = os.path.join(root_directory, "structured_data")
    preferences_dir = os.path.join(root_directory, "preferences")
    return input_dir, output_dir, preferences_dir

"""Find folder structure from zip file and keep track of where documents are placed"""
#Extract file structure
def find_and_note_structure_from_json(preferences_dir, project_name):

    json_file_path = os.path.join(preferences_dir, "folder_structure.json")
    print(json_file_path)
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Assuming the top-level key always needs to be replaced with project_name
    if data:
        top_level_key = next(iter(data))  # Get the first key in the dictionary
        data[project_name] = data.pop(top_level_key)

    folder_structure_list = dict_to_nested_list(data)
    folder_structure_text_list = nested_list_to_text_list(folder_structure_list)
    folder_structure_indented = folder_structure_to_text(folder_structure_list)
    return folder_structure_list, folder_structure_indented, folder_structure_text_list

def dict_to_nested_list(d):
    """
    Convert a dictionary to a nested list representing folder structure.
    """
    result = []
    for key, value in d.items():
        if value:  # If there are subdirectories
            result.append([key, dict_to_nested_list(value)])
        else:
            result.append(key)
    return result

# not used in current config
def folder_structure_to_text(structure, level=0):
    """
    Convert a nested list representing folder structure into indented text.
    """
    text = ""
    indent = "  " * level
    for folder in structure:
        if isinstance(folder, list):
            text += f"{indent}- {folder[0]}\n" + folder_structure_to_text(folder[1], level + 1)
        else:
            text += f"{indent}- {folder}\n"
    return text
def nested_list_to_text_list(structure, level=0):
    """
    Convert a nested list representing folder structure into a structured list in text form.
    """
    text = "["
    for folder in structure:
        if isinstance(folder, list):
            sub_text = nested_list_to_text_list(folder[1], level + 1)
            text += f"['{folder[0]}', {sub_text}], "
        else:
            text += f"'{folder}', "
    text = text.rstrip(", ") + "]"
    return text if level > 0 else text.replace(", ]", "]")

# create folder structure (calls the extract file structure functions)
def create_folder_structure_from_list(folder_list, base_path):
    """
    Recursively create the folder structure from a nested list starting at base_path.
    """
    for item in folder_list:
        if isinstance(item, list):
            # It's a folder with possibly more nested folders
            new_base_path = os.path.join(base_path, item[0])
            if not os.path.exists(new_base_path):
                os.makedirs(new_base_path)
            create_folder_structure_from_list(item[1], new_base_path)
        else:
            # It's a top-level folder
            folder_path = os.path.join(base_path, item)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
def find_and_create_zip_structure(preferences_dir, output_dir,  project_name):
    """
    Find the first zip file in the specified input directory, analyze its folder structure,
    replace the top-level folder name with project_name, and create this folder structure
    in the output directory.
    """
    # The modified find_and_note_zip_structure function here
    # Assuming it sets folder_structure_list correctly

    folder_structure_list, folder_structure_indented, _ = find_and_note_structure_from_json(preferences_dir, project_name)

    if folder_structure_list is not None:
        # Create the folder structure starting at output_dir
        create_folder_structure_from_list(folder_structure_list, output_dir)
        print(f"Folder structure created under {output_dir}\n")
        print(folder_structure_indented)
        return folder_structure_indented
    else:
        print("No folder structure to create.\n")

# old implementation - generates directory at the end
def generate_directory_json(output_dir, project_name, input_dir):
    project_path = os.path.join(output_dir, project_name)
    directory_tree = []
    next_id = 1  # Start IDs from 1
    dir_id_map = {}  # Maps directory path to ID
    
    # Root directory entry
    directory_tree.append({
        "id": next_id,
        "name": project_name,
        "type": "directory",
        "parent_id": None
    })
    dir_id_map[project_path] = next_id
    next_id += 1
    
    # Walk the directory structure for the project
    for root, dirs, files in os.walk(project_path):
        current_dir_id = dir_id_map[root]
        # Process directories
        for d in dirs:
            dir_path = os.path.join(root, d)
            directory_tree.append({
                "id": next_id,
                "name": d,
                "type": "directory",
                "parent_id": current_dir_id
            })
            dir_id_map[dir_path] = next_id
            next_id += 1
            
        # Process files, ignoring JSON files
        for f in files:
            if f.lower().endswith('.json'):  # Skip JSON files
                continue
            file_path = os.path.join(root, f)
            file_size = os.path.getsize(file_path)
            directory_tree.append({
                "id": next_id,
                "name": f,
                "type": "file",
                "size": file_size,
                "parent_id": current_dir_id
            })
            next_id += 1
    
    # Process files in the "documents" directory separately
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            directory_tree.append({
                "id": next_id,
                "name": file_name,
                "type": "file",
                "size": file_size,
                "parent_id": None  # Set parent_id to None for documents directory files
            })
            next_id += 1
    
    # Save the structure to a JSON file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, 'global_directory.json'), 'w', encoding='utf-8') as f:
        json.dump(directory_tree, f, indent=2)

"""Reading the pdf"""
#Extract text, name and page number from pdf
def extract_pdf_info(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    num_pages = len(doc)
    title = os.path.basename(pdf_path)

    for page_num in range(num_pages):
        page = doc.load_page(page_num)
        text = page.get_text()
        # Split text into lines
        lines = text.split('\n')
        # Reassemble text with conditional newlines
        new_text = ""
        for line in lines:
            # Strip leading and trailing whitespace
            stripped_line = line.strip()
            if stripped_line:  # Ensure line is not empty
                # Check if line ends with a sentence-ending punctuation or is likely a list item
                if stripped_line.endswith(('.', '?', '!', ':', ';', '-', '—')) or stripped_line[-1].isdigit():
                    new_text += stripped_line + "\n"
                else:
                    # Append a space to continue the sentence if it's broken up
                    new_text += stripped_line + " "
        full_text += new_text
    doc.close()
    return full_text, num_pages, title

def remove_first_line(text):
    lines = text.split('\n')  # Split the text into lines
    if len(lines) > 1:  # Check if there are at least two lines
        return '\n'.join(lines[1:])  # Join the lines excluding the first one
    else:
        return ''  # Return an empty string if there's only one line or less


"""Creating and truncating query"""
# create a query and combine with the text in the document
def construct_query(extracted_text,folder_structure_indented,enable_testing_output=False):
    query = f"""
You are a pragmatic Solar M&A Senior Analyst in the United States. You are about to get instructions to extract information from documents. This information will be used to add meta data, create a summary and sort the documents.

Extract the following fields from the document text provided and format the response as valid JSON:
- "Document_date" in the format '3 letter month name-DD, YYYY'.
- "Document_summary" limited to a maximum of 3 sentences, tailored for a solar M&A analyst. It should state what kind of document it is, but also what its implicatoins are or what state it is in. It should assume the analyst knows about the M&A process.
- "Suggested_title" in the format 'MM-DD-YYYY max 5 word document title'. Try your best to come up with a title that is useful if you quickly want to understand what kind of document it is
- "Suggested_title_v2" in same format as "suggested title" but with different wording
- "Suggested_title_v3" in same format as "suggested title" but with different wording
- "Document_folder_path": Select the most suitable folder from the folder list which will be given. Follow instructions below. 
- "Label": choose from following: "Communication", "Contract", "Amendment", "Technical Specification", "Application", "Exhibit", "LeonCV", "N/A"
- "Reasoning": Provide reasoning for every documents you classified. 

For "Document_folder_path", please follow these guidelines: 

    1. Do not create new folders. Documents must be classified based on existing categories, according to their primary content and purpose.

    2. Classify documents with precision, using these category definitions:

        "Interconnection": Contains contracts and agreements for connecting the solar project to the power grid. Look for phrases like "the interconnection customer agrees" and "interconnection requests".

        "Site Control": Includes legal documents that confirm the right to use, manage, and develop land for solar projects. This category is crucial for affirming legal authority over project sites and includes leases, purchase agreements, and easements.

        "PPA": Features power purchasing agreements between the project developer and an off-taker regarding the sale of generated solar power, detailing prices, terms, and standards, as well as supplementary documents.  

        "Environmental": Documents related to environmental impact assessments, permits, and compliance reports for the solar project. Includes studies on flora, fauna, water, soil, and air quality impacts, as well as mitigation strategies.

        "EPC": Contains contracts, plans, and documentation related to the engineering design, procurement of materials, and construction of the solar project. This includes agreements with contractors, project timelines, and construction permits.

    3. Prioritize document essence and main purpose for classification. In cases of uncertainty or documents that span multiple categories, classify according to the document's primary focus.
    4. Only classify documents as "Miscellaneous" if no other folder is likely. 
The list of to select folders from below:
{remove_first_line(folder_structure_indented)}

The provided document text is:
{extracted_text}
"""
    # Write the query to a text file
    save_txt_file("query.txt", query, enable_testing_output)
    return query
# Truncate query
def truncate_query_to_fit_context(query, max_length=10000, enable_testing_output=False): #35k is ok for gpt-4-0125-preview #10k max for gpt-3.5-turbo-0125
    """
    Truncate a query to ensure it fits within the specified maximum length, preserving new lines and indentation.
    This version considers the query as a series of lines.
    
    Parameters:
    - query: The text query to be truncated.
    - max_length: The maximum allowed length in tokens. Defaults to 50000.
    
    Returns:
    - Truncated query with preserved formatting.
    """
    # Split the query into lines instead of words to preserve formatting
    lines = query.split('\n')
    truncated_query = ""
    token_count = 0
    total_token_count = sum(len(line.split()) for line in lines)  # Total tokens in the original query

    for line in lines:
        line_token_count = len(line.split())  # Estimate token count for the line
        if token_count + line_token_count > max_length:
            break  # Stop adding lines if the next line would exceed the limit
        truncated_query += line + "\n"  # Add the line back with its newline character
        token_count += line_token_count
    
    # Calculate and print the percentage of the query used
    percentage_used = (token_count / total_token_count) * 100 if total_token_count > 0 else 0
    print(f"Percentage of the document used: {percentage_used:.2f}%")
    
    save_txt_file("truncated_query.txt", truncated_query, enable_testing_output)
    return truncated_query.rstrip()  # Remove the last newline character to clean up
# put query into chatgpt
def make_openai_api_call(truncated_query):
    """
    Make an API call to OpenAI with the given truncated query and return the JSON response.
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        #model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "You are a solar M&A analyst and great at extracting summaries and text from M&A documentation. Under no circumstances do you halucinate, instead you say that you leave a field blank if you cannot answer"},
            {"role": "user", "content": truncated_query}
        ],
        temperature=0
    )
    response_content = completion.choices[0].message.content
    save_txt_file("raw_gpt_response.txt", response_content, enable_testing_output)
    # Clean the response content to ensure it's a valid JSON string
    valid_json_string = make_json_valid(response_content)

    return valid_json_string

"""Clean data and add to metadata file"""
#query and output
def process_json_add_extension(data):
    # Extract the full file extension from 'original_title'
    _, file_extension = os.path.splitext(data.get('original_title', ''))
    
    # Append the file extension to the suggested titles if not already present
    for key in ['Suggested_title', 'Suggested_title_v2', 'Suggested_title_v3']:
        if key in data:
            # Check if the current value does not end with the file extension
            if not data[key].endswith(file_extension):
                # Append the file extension
                data[key] += file_extension

    return data

def make_json_valid(response_content):
    """
    Clean the response content by removing any text outside the outermost JSON object braces.
    
    Parameters:
    - response_content (str): The potentially malformed JSON string.
    
    Returns:
    - str: A cleaned JSON string.
    """
    start_index = response_content.find('{')
    end_index = response_content.rfind('}')
    
    if start_index != -1 and end_index != -1 and end_index > start_index:
        response_content = response_content[start_index:end_index+1]
    else:
        print("Valid JSON object not found in the response.")
        response_content = "{}"

    try:
        json_obj = json.loads(response_content)
        if "Document_summary" in json_obj and json_obj["Document_summary"]:
            return response_content
        else:
            print("\n###########ERROR###########\nGenerated JSON is empty or 'document_summary' entry is missing.\nMay need to truncate query \n###########ERROR###########\n")
    except json.JSONDecodeError:
        raise print("Failed to parse JSON.")


    return response_content

def correct_json_folder_path(json_file,project_name):

    # Update the 'Document_folder_path' in the JSON data
    document_folder_path = json_file.get("Document_folder_path", project_name + "/Unclassified")
    
    # Prepend "project/" to the 'Document_folder_path' field in the JSON data
    document_folder_path_with_project = project_name + "/" + document_folder_path
    json_file["Document_folder_path"] = document_folder_path_with_project
    return json_file

def append_to_complete_metadata_file(data, file_path):
    highest_id = 0  # Default to 0 if file is empty or does not exist
    new_data = data  # Assuming 'data' is the dictionary for the new entry

    # Check if the metadata file exists and is not empty
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r+', encoding='utf-8') as file:
                # Load the existing data
                try:
                    file_data = json.load(file)
                    if file_data:  # If there are existing entries
                        # Find the highest ID
                        highest_id = max(entry.get('id', 0) for entry in file_data)
                except json.JSONDecodeError:
                    file_data = []  # Reset to an empty list if there's a JSON decode error

                # Assign a new ID to the new entry
                new_data['id'] = highest_id + 1

                # Append the new entry
                file_data.append(new_data)

                # Rewrite the updated data back to the file
                file.seek(0)
                file.truncate()  # Clear the file before re-writing
                json.dump(file_data, file, indent=4)

        except IOError as e:
            print(f"Failed to open or read from {file_path}. Error: {e}")
    else:
        # If the file does not exist, start with the new entry as the first item
        new_data['id'] = 1  # Start IDs from 1
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([new_data], file, indent=4)

"""Process one PDF"""
def process_pdf(pdf_path, output_dir, folder_structure_indented, project_name, copy_or_move="move"):
    """
    Adjusted to ensure the 'document_folder_path' uses the correct 'project_name/unclassified'.
    """
    print(f"Processing {os.path.basename(pdf_path)}...")
    
    extracted_text, num_pages, title = extract_pdf_info(pdf_path)
    print("Document is", num_pages, "pages long")
    query = construct_query(extracted_text, folder_structure_indented)
    truncated_query = truncate_query_to_fit_context(query)
    name_of_testing_doc = "query_for_"+title+".txt"
    save_txt_file(name_of_testing_doc, truncated_query, enable_testing_output = False)
    output_json = make_openai_api_call(truncated_query)
    data = json.loads(output_json) # Assuming output_json is a string; parse it to a dict

    data.update({
        "number_of_pages": num_pages,
        "original_title": title,
        "current_title": title,
        "notes" : "",
        "questions" : "",
        "open_tasks" : "",

    })

    data = process_json_add_extension(data) # add extension to suggested titles
    data = correct_json_folder_path(data, project_name)


    # Extract 'Document_folder_path' from the JSON response and ensure correct path formation
    document_folder_path = data.get("Document_folder_path", project_name + "/Unclassified")

    # Correctly handle the 'Unclassified' case and ensure the path starts with 'project_name/'
    if not document_folder_path.startswith(project_name):
        print("checking the if not document_folder_path:")
        document_folder_path = os.path.join(project_name, "Unclassified")
    print('output_dir:', output_dir)
    print('document_folder_path:', document_folder_path)
    # Build the correct final path within the output directory
    final_path = os.path.join(output_dir, document_folder_path)
    os.makedirs(final_path, exist_ok=True)  # Ensure the folder exists
    
    # Move or copy the PDF to the designated folder
    if copy_or_move == "copy":
        print("copying file, not moving")
        shutil.copy(pdf_path, os.path.join(final_path, os.path.basename(pdf_path)))
    else:    
        shutil.move(pdf_path, os.path.join(final_path, os.path.basename(pdf_path)))

    complete_metadata_file_path = os.path.join(output_dir, "complete_file_metadata.json")

    # Append metadata to the centralized JSON
    append_to_complete_metadata_file(data, complete_metadata_file_path)

    print(f"Finished processing {os.path.basename(pdf_path)}. File saved to {final_path}.")




"""Main function"""
def main(input_dir, output_dir, preferences_dir, project_name, copy_or_move ="move"):
    """
    Main function to process all PDF files in the input directory.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # extract file structure from the zip. save folder_structure_indented as the folder structure to be used in the query
    folder_structure_indented = find_and_create_zip_structure(preferences_dir, output_dir, project_name)

    # List all PDF files in the input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    total_documents = len(pdf_files)
    print(total_documents, "documents found in input folder\n")

    generate_directory_json(output_dir, project_name, input_dir)
    print("directory generated")

    # Process each PDF file and update progress
    for idx, pdf_name in enumerate(pdf_files, start=1):
        pdf_path = os.path.join(input_dir, pdf_name)
        process_pdf(pdf_path, output_dir, folder_structure_indented, project_name, copy_or_move)
        
        generate_directory_json(output_dir, project_name, input_dir)

        # Print progress update
        print(f"{idx} out of {total_documents} documents processed\n")

    
    #generate_directory_json(output_dir, project_name)

def clear_directory_contents(output_dir):
    """
    Deletes all the contents of the specified directory without removing the directory itself.

    Args:
    - output_dir (str): The path to the directory whose contents are to be deleted.
    """
    # Check if the directory exists
    if not os.path.exists(output_dir):
        print(f"The directory {output_dir} does not exist.")
        return

    # Iterate through all items in the directory
    for item_name in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item_name)
        
        # Check if the item is a file or a directory
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove the file
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove the directory and all its contents
        
    print(f"All contents of {output_dir} have been deleted.")

"""Implementation"""

client = OpenAI(api_key="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")

enable_testing_output = False
copy_or_move = "move" #have to choose move for implementation. copy breaks the directory function
root_directory = set_root_directory()
input_dir, output_dir, preferences_dir = construct_relative_paths(root_directory)
project_name = "project"



if __name__ == "__main__":
    project_name = "project"
    root_directory = set_root_directory()
    input_dir, output_dir, preferences_dir = construct_relative_paths(root_directory)
    clear_directory_contents(output_dir) #use if you want to clear file structure before running
    main(input_dir, output_dir, preferences_dir, project_name, copy_or_move)
