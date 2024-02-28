import fitz  # PyMuPDF
import os
from openai import OpenAI
import json
import zipfile
import shutil
from tqdm import tqdm


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

#Extract text, name and page number from pdf
#@profile
def extract_pdf_info(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file {pdf_path}: {e}")
        return "", 0, ""  # Return empty values on error

    full_text = ""
    title = os.path.basename(pdf_path)
    num_pages = len(doc)
    try:
        for page_num in range(num_pages):
            page = doc.load_page(page_num)
            text = page.get_text()
            # The text processing logic remains the same
            lines = text.split('\n')
            new_text = ""
            for line in lines:
                stripped_line = line.strip()
                if stripped_line:
                    if stripped_line.endswith(('.', '?', '!', ':', ';', '-', '—')) or stripped_line[-1].isdigit():
                        new_text += stripped_line + "\n"
                    else:
                        new_text += stripped_line + " "
            full_text += new_text
    except Exception as e:
        print(f"Error processing PDF file {pdf_path}: {e}")
        # Optionally, return what was processed so far instead of empty values
    finally:
        doc.close()

    return full_text, num_pages, title


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

def construct_query(extracted_text,folder_structure_indented,enable_testing_output=False):
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
    # Write the query to a text file
    save_txt_file("query.txt", query, enable_testing_output)
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

def process_pdf(pdf_path, output_dir, folder_structure_indented, project_name, action="copy"):
    """
    Process a PDF file by moving or copying it to a designated folder.

    Parameters:
    - pdf_path: Path to the PDF file.
    - output_dir: The base output directory where the structured data folder is located.
    - folder_structure_indented: Indented string representation of the folder structure.
    - project_name: Name of the project, used in constructing the folder path.
    - action: Specifies the action to perform on the file: "move" or "copy".
    """
    print(f"Processing {os.path.basename(pdf_path)}...")
    
    extracted_text, num_pages, title = extract_pdf_info(pdf_path)
    if not extracted_text or num_pages == 0:
        print(f"Skipping {os.path.basename(pdf_path)} due to extraction error.")
        return  # Skip further processing for this PDF
    
    print("Document is", num_pages, "pages long")
    query = construct_query(extracted_text, folder_structure_indented)
    truncated_query = truncate_query_to_fit_context(query)
    output_json = make_openai_api_call(truncated_query)
    data = json.loads(output_json)  # Assuming output_json is a string; parse it to a dict

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
        print("checking the if not document_folder_path:")
        document_folder_path = os.path.join(project_name, "Unclassified")
    print('output_dir:', output_dir)
    print('document_folder_path:', document_folder_path)
    # Build the correct final path within the output directory
    final_path = os.path.join(output_dir, document_folder_path)
    os.makedirs(final_path, exist_ok=True)  # Ensure the folder exists

       # Determine action based on the 'action' parameter
    if action == "copy":
        shutil.copy(pdf_path, os.path.join(final_path, os.path.basename(pdf_path)))
        print(f"Copied {os.path.basename(pdf_path)} to {final_path}.")
    else:
        shutil.move(pdf_path, os.path.join(final_path, os.path.basename(pdf_path)))
        print(f"Moved {os.path.basename(pdf_path)} to {final_path}.")
    

    complete_metadata_file_path = os.path.join(output_dir, "complete_file_metadata.json")

    # Append metadata to the centralized JSON
    append_to_complete_metadata_file(data, complete_metadata_file_path)


    print(f"Finished processing {os.path.basename(pdf_path)}. File saved to {final_path}.")

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

    try:
        json_obj = json.loads(response_content)
        if "Document_summary" in json_obj and json_obj["Document_summary"]:
            return response_content
        else:
            print("\n###########ERROR###########\nGenerated JSON is empty or 'document_summary' entry is missing.\nMay need to truncate query \n###########ERROR###########\n")
    except json.JSONDecodeError:
        raise print("Failed to parse JSON.")


    return response_content

def make_openai_api_call(truncated_query):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a solar M&A analyst..."},
                {"role": "user", "content": truncated_query}
            ],
            temperature=0
        )
        response_content = completion.choices[0].message.content
    except Exception as e:
        print(f"Error making OpenAI API call: {e}")
        return "{}"  # Return a default empty JSON structure in case of error
    save_txt_file("raw_gpt_response.txt", response_content, enable_testing_output)
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
        print(f"Folder structure created under {output_dir}\n")
        return folder_structure_indented
    else:
        print("No folder structure to create.\n")


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

def main(input_dir, output_dir, project_name, action="move"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract file structure from the zip. Save folder_structure_indented as the folder structure to be used in the query
    folder_structure_indented = find_and_create_zip_structure(input_dir, output_dir, project_name)

    # List all PDF files in the input directory - Only one enumeration needed
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    total_documents = len(pdf_files)
    print(f"{total_documents} documents found in input folder\n")
    
    # Process each PDF file and update progress - Main processing loop
    for idx, pdf_name in enumerate(tqdm(pdf_files), start=1):  # Use tqdm here for progress indication
        pdf_path = os.path.join(input_dir, pdf_name)
        process_pdf(pdf_path, output_dir, folder_structure_indented, project_name, action)
        
    generate_directory_json(output_dir, project_name)



client = OpenAI(api_key="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")
enable_testing_output = True
copy_or_move = "move" #better to chose move for testing complete functionality. and clearing output folders first
root_directory = set_root_directory()
input_dir, output_dir = construct_relative_paths(root_directory)
project_name = "MegaSolar"

if __name__ == "__main__":
    project_name = "MegaSolar"
    root_directory = set_root_directory()
    input_dir, output_dir = construct_relative_paths(root_directory)
    action = "copy"  # or "move", this could be determined by user input or another logic
    main(input_dir, output_dir, project_name, action)



### Convert_Directory.py

# New function definition
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"No such file: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
    return None


def convert_structure(input_json):
    # Your existing conversion logic
    directories_with_subfolders = set()
    directories = {}
    output = {}

    for item in input_json:
        if item['type'] == 'directory':
            directories[item['id']] = item['name']
            if item['parent_id'] is not None:
                directories_with_subfolders.add(item['parent_id'])

    lowest_level_directories = {id: name for id, name in directories.items() if id not in directories_with_subfolders}

    for name in lowest_level_directories.values():
        output[name] = []

    for item in input_json:
        if item['type'] == 'file':
            parent_id = item['parent_id']
            if parent_id in lowest_level_directories:
                directory_name = lowest_level_directories[parent_id]
                output[directory_name].append(item['name'])

    return output

def save_json_data(data, file_path, indent=4):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent)
        print(f"Data successfully saved to {file_path}")
    except IOError as e:
        print(f"Failed to save data to {file_path}: {e}")

def convert_directory_structure():
    set_root_directory()
    json_file_path = 'structured_data/global_directory.json'
    input_json = load_json_data(json_file_path)  # New load function usage
    input_directory = os.path.dirname(json_file_path)  # Manually getting directory
    converted_json_with_empty_folders = convert_structure(input_json)
    output_file_path = os.path.join(input_directory, 'global_directory_frontend.json')
    save_json_data(converted_json_with_empty_folders, output_file_path)
    print("directory structure converted")


if __name__ == "__main__":
    convert_directory_structure()


### Testing Structure

def load_expected_classifications(file_path='holdout.json'):
    """
    Load expected classifications from a JSON file.
    """
    with open(file_path, 'r') as file:
        expected_classifications = json.load(file)
    # Convert to a dict for easier lookup
    return {item['name']: item['classification'] for item in expected_classifications}

def calculate_accuracy(converted_json, expected_classifications):
    """
    Calculate the classification accuracy for each directory.
    """
    accuracy = {}
    for category, files in converted_json.items():
        if not files:  # Skip empty categories
            accuracy[category] = "N/A"
            continue
        correct_count = sum(1 for file_name in files if expected_classifications.get(file_name, None) == category)
        total_files = len(files)
        accuracy[category] = f"{correct_count / total_files * 100:.2f}%"
    return accuracy

def save_json_data_with_accuracy(output_data, accuracy, output_directory):
    """
    Save the output data along with accuracy information to a JSON file.
    """
    output_file_path = os.path.join(output_directory, 'global_directory_frontend.json')
    output_with_accuracy = {"categories": output_data, "accuracy": accuracy}
    with open(output_file_path, 'w') as file:
        json.dump(output_with_accuracy, file, indent=4)
    print(f"Output saved to: {output_file_path}")

def convert_directory_structure():
    set_root_directory()
    json_file_path = 'structured_data/global_directory.json'
    input_json = load_json_data(json_file_path)
    input_directory = os.path.dirname(json_file_path)
    converted_json = convert_structure(input_json)
    expected_classifications = load_expected_classifications()
    accuracy = calculate_accuracy(converted_json, expected_classifications)
    save_json_data_with_accuracy(converted_json, accuracy, input_directory)
    print("Directory structure converted with accuracy calculation.")

if __name__ == "__main__":
    convert_directory_structure()


#### Accuracy Tracker
import pandas as pd
import json
from datetime import datetime

def update_accuracy_tracker_v3(json_file_path, csv_file_path):
    # Load JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    accuracies = data['accuracy']
    
    # Load or initialize the CSV file
    try:
        df = pd.read_csv(csv_file_path)
        # Ensure test_id is treated as integer
        df['test_id'] = pd.to_numeric(df['test_id'], errors='coerce').fillna(0).astype(int)
        # Generate the next test_id by adding 1 to the maximum test_id found
        next_test_id = df['test_id'].max() + 1
    except (FileNotFoundError, ValueError):
        # Initialize with the new observation's keys if the file doesn't exist
        # Or handle ValueError if 'test_id' column is empty (max() on empty series)
        df = pd.DataFrame(columns=['test_id', 'date_time'] + [f'Accuracy_{category.replace(" ", "_")}' for category in accuracies.keys()])
        next_test_id = 1  # Start from 1 if file doesn't exist or is empty
    
    # Prepare the new observation
    new_observation = {
        'test_id': next_test_id,
        'date_time': datetime.now().strftime('%m/%d/%y %H:%M'),  # Adjusted format per your example
    }
    
    # Prefix category accuracies and add them to the observation
    for category, accuracy in accuracies.items():
        # Use a consistent naming convention for accuracy columns
        new_observation[f'Accuracy_{category.replace(" ", "_")}'] = accuracy if accuracy != "N/A" else ""
    
    # Append the new observation
    df = pd.concat([df, pd.DataFrame([new_observation])], ignore_index=True)
    
    # Save the updated DataFrame back to CSV
    df.to_csv(csv_file_path, index=False)
    print(f"CSV file has been updated with the new observation. Test ID: {next_test_id}")

# Example usage
json_file_path = 'structured_data/global_directory_frontend.json'  # Update with the actual path to your JSON file
csv_file_path = 'accuracy_tracker.csv'  # Update with the actual path to your CSV file
update_accuracy_tracker_v3(json_file_path, csv_file_path)
