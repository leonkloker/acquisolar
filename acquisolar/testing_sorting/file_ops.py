import os
import json

def save_txt_file(title, contents, folder_name="classification_testing(can_be_deleted)", enable_testing_output=False):
    """
    Saves a text file with given contents. Optionally, enables saving output for testing.
    """
    if enable_testing_output:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, title)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(contents)

def set_root_directory():
    """
    Sets the root directory to the directory where the current script resides.
    """
    root_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_directory)
    print("Root directory set to:", root_directory)
    return root_directory

def construct_relative_paths(root_directory):
    """
    Constructs relative paths for input and output directories based on the root directory.
    """
    input_dir = os.path.join(root_directory, "documents")
    output_dir = os.path.join(root_directory, "structured_data")
    return input_dir, output_dir

def output_extracted_text_to_file(extracted_text, output_path):
    """
    Outputs the extracted text to a file at the specified path.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

def append_to_complete_metadata_file(data, file_path):
    """
    Appends metadata to a centralized JSON file, creating the file if it does not exist.
    """
    highest_id = 0  # Default to 0 if file is empty or does not exist
    new_data = data  # Assuming 'data' is the dictionary for the new entry

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r+', encoding='utf-8') as file:
                try:
                    file_data = json.load(file)
                    highest_id = max(entry.get('id', 0) for entry in file_data) if file_data else 0
                except json.JSONDecodeError:
                    file_data = []

                new_data['id'] = highest_id + 1
                file_data.append(new_data)
                file.seek(0)
                file.truncate()
                json.dump(file_data, file, indent=4)
        except IOError as e:
            print(f"Failed to open or read from {file_path}. Error: {e}")
    else:
        new_data['id'] = 1
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([new_data], file, indent=4)

def load_json_data(file_path):
    """
    Loads JSON data from a file.
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

def save_json_data(data, file_path, indent=4):
    """
    Saves data as JSON to a file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent)
        print(f"Data successfully saved to {file_path}")
    except IOError as e:
        print(f"Failed to save data to {file_path}: {e}")
