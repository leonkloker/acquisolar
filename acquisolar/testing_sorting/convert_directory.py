import json
import os

def load_json_data(file_path):
    """
    Loads JSON data from a specified file path.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"No such file: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return None

def convert_structure(input_json):
    """
    Converts the directory structure from the JSON format into a format that
    lists each file along with its directory (classification).
    """
    # Initialize empty dictionary to hold the converted structure
    converted_structure = {}
    
    # Iterate through the input JSON to build a mapping of directory IDs to names
    for item in input_json:
        if item['type'] == 'directory':
            # Create a new list in the converted structure for each directory
            converted_structure[item['name']] = []
    
    # Second pass to assign files to their directories
    for item in input_json:
        if item['type'] == 'file':
            # Assuming file items have 'parent_id' that matches directory 'id'
            # Find parent directory name using 'parent_id'
            parent_directory = next((dir_item['name'] for dir_item in input_json if dir_item['type'] == 'directory' and dir_item['id'] == item['parent_id']), None)
            if parent_directory:
                converted_structure[parent_directory].append(item['name'])
    
    return converted_structure

def save_json_data(data, file_path, indent=4):
    """
    Saves data as JSON to a specified file path.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent)
        print(f"Data successfully saved to {file_path}")
    except IOError as e:
        print(f"Failed to save data to {file_path}: {e}")

def convert_and_save_directory_structure(input_json_path, output_json_path):
    """
    Loads the directory structure from a JSON file, converts it to a simplified format,
    and saves the converted data to another JSON file.
    """
    input_json = load_json_data(input_json_path)
    if input_json is not None:
        converted_structure = convert_structure(input_json)
        if converted_structure:
            save_json_data(converted_structure, output_json_path)
        else:
            print("Converted structure is empty. Nothing to save.")
    else:
        print("Failed to load input JSON data.")




# Optionally, add a conditional block for direct execution
if __name__ == "__main__":
    convert_and_save_directory_structure('acquisolar/testing_sorting/structured_data/global_directory.json', 'acquisolar/testing_sorting/structured_data/directory_for_frontend.json')
