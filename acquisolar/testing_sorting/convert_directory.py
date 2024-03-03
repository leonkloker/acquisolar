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

    Parameters:
    - input_json: The loaded JSON data representing the directory structure.

    Returns:
    - A list of dictionaries, each containing 'name' (file name) and 'classification' (directory name).
    """
    # Map directory IDs to names
    directory_names = {item['id']: item['name'] for item in input_json if item['type'] == 'directory'}
    
    # Initialize output list
    output = []
    
    # Iterate over items in input_json
    for item in input_json:
        if item['type'] == 'file':
            # For each file, find its parent directory's name to use as classification
            classification = directory_names.get(item['parent_id'], 'Unclassified')
            output.append({
                "name": item['name'],
                "classification": classification
            })

    return output


def save_json_data(data, file_path, indent=4):
    """
    Saves data as JSON to a specified file path.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=indent)

def convert_and_save_directory_structure(input_json_path, output_json_path):
    """
    Loads the directory structure from a JSON file, converts it to a simplified format,
    and saves the converted data to another JSON file.
    """
    input_json = load_json_data(input_json_path)
    if input_json is not None:
        converted_structure = convert_structure(input_json)
        save_json_data(converted_structure, output_json_path)
    else:
        print("Failed to load input JSON data.")

# Optionally, add a conditional block for direct execution
if __name__ == "__main__":
    convert_and_save_directory_structure('structured_data/global_directory.json', 'structured_data/directory_for_frontend.json')
