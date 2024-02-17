import os
import json

def set_root_directory():
    # Get the directory where the current script resides
    root_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_directory)
    print("Root directory set to:", root_directory)
    return root_directory

def load_json_data(file_path):
    # Load JSON data from a specified file path
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Return both data and the directory of the file path
    return data, os.path.dirname(file_path)

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

def save_json_data(output_data, output_directory):
    # Define the output file path
    output_file_path = os.path.join(output_directory, 'global_directory_frontend.json')
    # Write the converted data to a JSON file
    with open(output_file_path, 'w') as file:
        json.dump(output_data, file, indent=4)
    print(f"Output saved to: {output_file_path}")

def convert_directory_structure():
    set_root_directory()
    json_file_path = 'structured_data/global_directory.json'
    input_json, input_directory = load_json_data(json_file_path)
    converted_json_with_empty_folders = convert_structure(input_json)
    save_json_data(converted_json_with_empty_folders, input_directory)

convert_directory_structure()