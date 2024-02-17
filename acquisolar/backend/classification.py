import fitz  # PyMuPDF
import os
from openai import OpenAI
import requests
import json
import tiktoken
import zipfile
import shutil

client = OpenAI(api_key="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")  # Text completion
project_name = "SAMPLE_PROJECT"

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
    return input_dir, output_dir

#go from pdf to query
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
    print(title)
    return full_text, num_pages, title

def truncate_query_to_fit_context(query, max_length=10000):
    """
    Truncate a query to ensure it fits within the specified maximum length, preserving new lines and indentation.
    This version considers the query as a series of lines.
    
    Parameters:
    - query: The text query to be truncated.
    - max_length: The maximum allowed length in tokens. Defaults to 2048.
    
    Returns:
    - Truncated query with preserved formatting.
    """
    # Split the query into lines instead of words to preserve formatting
    lines = query.split('\n')
    
    truncated_query = ""
    token_count = 0
    
    for line in lines:
        line_token_count = len(line.split())  # Estimate token count for the line
        if token_count + line_token_count > max_length:
            break  # Stop adding lines if the next line would exceed the limit
        truncated_query += line + "\n"  # Add the line back with its newline character
        token_count += line_token_count
    
    return truncated_query.rstrip()  # Remove the last newline character to clean up
def construct_query(extracted_text,folder_structure_indented):
    query = f"""
Extract the following fields from the document text provided and format the response as valid JSON:
- "Document_date" in the format '3 letter month name-DD, YYYY'.
- "Document_summary" limited to a maximum of 3 sentences, tailored for a solar M&A analyst. It should state what kind of document it is, but also what its implicatoins are or what state it is in. It should assume the analyst knows about the M&A process.
- "Suggested_title" in the format 'MM-DD-YYYY max 5 word document title'. Try your best to come up with a title that is useful if you quickly want to understand what kind of document it is
- "Suggested_title_v2" in same format as "suggested title" but with different wording
- "Suggested_title_v3" in same format as "suggested title" but with different wording
- "Document_folder_path", Choose the the folder that makes most sense from the folders below. You should specify the path to the folder from the top level folder in the format "project_name/sub_folder..." where project name is the top folder. If you really cant find a folder that fits, put it in "project_name/Unclassified". Dont make up any new folders.
{folder_structure_indented}

The provided document text is:
{extracted_text}
"""
    return query
def output_extracted_text_to_file(extracted_text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

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

def process_pdf(pdf_path, output_dir, folder_structure_indented):
    """
    Adjusted to ensure the 'document_folder_path' uses the correct 'project_name/unclassified'.
    """
    print(f"Processing {os.path.basename(pdf_path)}...")
    
    extracted_text, num_pages, title = extract_pdf_info(pdf_path)
    query = construct_query(extracted_text, folder_structure_indented)
    truncated_query = truncate_query_to_fit_context(query)
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

    # Extract 'Document_folder_path' from the JSON response and ensure correct path formation
    document_folder_path = data.get("Document_folder_path", project_name + "/Unclassified")
    
    # Correctly handle the 'Unclassified' case and ensure the path starts with 'project_name/'
    if not document_folder_path.startswith(project_name):
        document_folder_path = os.path.join(project_name, "Unclassified")

    # Build the correct final path within the output directory
    final_path = os.path.join(output_dir, document_folder_path)
    os.makedirs(final_path, exist_ok=True)  # Ensure the folder exists
    
    # Move the PDF to the designated folder
    shutil.move(pdf_path, os.path.join(final_path, os.path.basename(pdf_path)))

    complete_metadata_file_path = os.path.join(output_dir, "complete_file_metadata.json")

    # Append metadata to the centralized JSON
    append_to_complete_metadata_file(data, complete_metadata_file_path)


    print(f"Finished processing {os.path.basename(pdf_path)}. JSON and PDF saved to {final_path}.")

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

    return response_content

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

    # Clean the response content to ensure it's a valid JSON string
    valid_json_string = make_json_valid(response_content)

    return valid_json_string

#Extract file structure
def find_and_note_zip_structure(input_dir, project_name):
    """
    Find the first zip file in the specified input directory, analyze its folder structure
    (excluding individual files), replace the top-level folder name with project_name,
    and returns both a nested list and an indented text representation of the folder structure.
    """
    zip_file = None
    for file in os.listdir(input_dir):
        if file.lower().endswith('.zip'):
            zip_file = os.path.join(input_dir, file)
            break

    if zip_file is None:
        print("No zip file found in the input directory.")
        return None, None, None  # Return None for all values if no zip file is found

    print(f"Analyzing folder structure of: {zip_file}")

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()

        # Initialize a dictionary to hold the folder structure
        folder_structure = {}

        for item in zip_contents:
            path_parts = item.split('/')
            # Replace top-level folder name with project_name
            if path_parts[0]:  # Check if the first part is not empty
                path_parts[0] = project_name
            current_level = folder_structure

            for part in path_parts[:-1]:  # Exclude the last part if it's a filename
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

    folder_structure_list = dict_to_nested_list(folder_structure)
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

def find_and_create_zip_structure(input_dir, output_dir, project_name):
    """
    Find the first zip file in the specified input directory, analyze its folder structure,
    replace the top-level folder name with project_name, and create this folder structure
    in the output directory.
    """
    # The modified find_and_note_zip_structure function here
    # Assuming it sets folder_structure_list correctly

    folder_structure_list, folder_structure_indented, _ = find_and_note_zip_structure(input_dir, project_name)

    if folder_structure_list is not None:
        # Create the folder structure starting at output_dir
        create_folder_structure_from_list(folder_structure_list, output_dir)
        print(f"Folder structure created under {output_dir}")
        return folder_structure_indented
    else:
        print("No folder structure to create.")


# outputing directory of all files
def generate_directory_json(output_dir, project_name):
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
    
    # Walk the directory structure
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
            
    # Save the structure to a JSON file
    with open(os.path.join(output_dir, 'global_directory.json'), 'w', encoding='utf-8') as f:
        json.dump(directory_tree, f, indent=2)

def main(input_dir, output_dir, project_name):
    """
    Main function to process all PDF files in the input directory.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # extract file structure from the zip. save folder_structure_indented as the folder structure to be used in the query
    folder_structure_indented = find_and_create_zip_structure(input_dir, output_dir, project_name)

    # List all PDF files in the input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    for pdf_name in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_name)
        process_pdf(pdf_path, output_dir, folder_structure_indented)
    
    generate_directory_json(output_dir, project_name)



if __name__ == "__main__":
    root_directory = set_root_directory()
    input_dir, output_dir = construct_relative_paths(root_directory)
    project_name = "MegaSolar"
    
    main(input_dir, output_dir, project_name)

"""
root_directory = set_root_directory()
input_dir, output_dir = construct_relative_paths(root_directory)
project_name = "MegaSolar"

main(input_dir, output_dir, project_name)
"""