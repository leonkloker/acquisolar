import json
import os
import shutil


# Set directories
def set_root_directory():
    # Get the directory where the current script resides
    root_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_directory)
    print("Root directory set to:", root_directory)
    return root_directory
def set_metadata_and_directory_file_path(root_directory):
    metadata_path = os.path.join(root_directory, "structured_data", "complete_file_metadata.json")
    directory_path = os.path.join(root_directory, "structured_data", "global_directory.json")
    return metadata_path, directory_path

# update document title (only updates in metadata, not in actual file)
import os
import json

def find_file_path(file_name, directory_data):
    """
    Find the path of a file given its name, using the global directory data.
    """
    for entry in directory_data:
        if entry["name"] == file_name and entry["type"] == "file":
            # Construct the path to this file
            path_components = [file_name]
            while entry["parent_id"] is not None:
                entry = next((e for e in directory_data if e["id"] == entry["parent_id"]), None)
                if entry:
                    path_components.insert(0, entry["name"])
            return os.path.join(*path_components)
    return None

def update_document_title(current_name, new_name):
    root_directory = set_root_directory()
    metadata_path, directory_path = set_metadata_and_directory_file_path(root_directory)

    # Load the global directory data to assist in finding the file's current path
    with open(directory_path, 'r', encoding='utf-8') as file:
        directory_data = json.load(file)

    # Find the current file's full path
    current_file_path = find_file_path(current_name, directory_data)
    if not current_file_path:
        print(f"File {current_name} not found in the global directory.")
        return

    # Construct the new file path
    new_file_path = os.path.join(os.path.dirname(current_file_path), new_name)

    # Physically rename the file
    try:
        os.rename(os.path.join(root_directory, "structured_data", current_file_path),
                  os.path.join(root_directory, "structured_data", new_file_path))
    except OSError as e:
        print(f"Error renaming file: {e}")
        return

    # Update the 'current_title' in metadata
    try:
        with open(metadata_path, 'r+', encoding='utf-8') as file:
            metadata_content = json.load(file)
            for entry in metadata_content:
                if entry.get("current_title") == current_name:
                    entry["current_title"] = new_name
                    break
            file.seek(0)
            file.truncate()
            json.dump(metadata_content, file, indent=4)
        print(f"Successfully updated the title from '{current_name}' to '{new_name}'.")
    except Exception as e:
        print(f"Failed to write updates to the metadata file. Error: {e}")

def update_document_title_(current_name, new_name):
    """
    Update the 'current_title' of a document in the metadata JSON file.
    Parameters:
    - current_name: The current title of the document to find.
    - new_name: The new title to update the document to.
    """
    # Set correct file location for metadata
    root_directory = set_root_directory()
    metadata_path, directory = set_metadata_and_directory_file_path(root_directory)

    # Ensure the metadata file exists
    if not os.path.exists(metadata_path):
        print(f"The file {metadata_path} does not exist.")
        return

    # Load the current metadata
    try:
        with open(metadata_path, 'r', encoding='utf-8') as file:
            metadata_content = json.load(file)
    except json.JSONDecodeError:
        print("Failed to decode JSON. The metadata file might be empty or corrupted.")
        return

    # Update the 'current_title' where it matches 'current_name'
    updated = False
    for entry in metadata_content:
        if entry.get("current_title") == current_name:
            entry["current_title"] = new_name
            updated = True
            break

    if not updated:
        print(f"No document found with the current title '{current_name}'.")
        return

    # Write the updated metadata back to the file
    try:
        with open(metadata_path, 'w', encoding='utf-8') as file:
            json.dump(metadata_content, file, indent=4)
        print(f"Successfully updated the title from '{current_name}' to '{new_name}'.")
    except Exception as e:
        print(f"Failed to write updates to the metadata file. Error: {e}")

# move files (moves the files but still needs to change the file metadata)
def get_directory_path_by_id(directory_id, directory_data):
    """
    Returns the directory path for a given directory_id from the directory_data.
    """
    for entry in directory_data:
        if entry["id"] == directory_id and entry["type"] == "directory":
            # Construct the directory path recursively if parent_id is not null
            if entry["parent_id"] is not None:
                parent_path = get_directory_path_by_id(entry["parent_id"], directory_data)
                return os.path.join(parent_path, entry["name"])
            return entry["name"]
    return None
def move_file(file_name, new_dir_id):
    root_directory = set_root_directory()
    _, directory_path = set_metadata_and_directory_file_path(root_directory)

    with open(directory_path, 'r', encoding='utf-8') as file:
        directory_data = json.load(file)

    # Convert new_dir_id to int if it's passed as a string
    new_dir_id = int(new_dir_id)

    # Updated to find the current and new directory paths
    new_dir_path = construct_path(new_dir_id, directory_data)
    new_dir_full_path = os.path.join(root_directory, "structured_data", new_dir_path)

    # Attempt to find the current directory ID and path for the file
    current_dir_id = next((entry["parent_id"] for entry in directory_data if entry["name"] == file_name and entry["type"] == "file"), None)
    if current_dir_id is None:
        print(f"File {file_name} not found in global_directory.json.")
        return

    current_dir_path = construct_path(current_dir_id, directory_data)
    current_dir_full_path = os.path.join(root_directory, "structured_data", current_dir_path)

    # Move the file
    src_path = os.path.join(current_dir_full_path, file_name)
    dest_path = os.path.join(new_dir_full_path, file_name)
    shutil.move(src_path, dest_path)
    print(f"Moved file {file_name} to {new_dir_full_path}")

    # Update the file's parent_id in global_directory.json
    for entry in directory_data:
        if entry["name"] == file_name and entry["type"] == "file":
            entry["parent_id"] = new_dir_id
            break

    with open(directory_path, 'w', encoding='utf-8') as file:
        json.dump(directory_data, file, indent=4)
    print(f"Updated {file_name} path in global_directory.json")
def construct_path(directory_id, directory_data):
    """
    Constructs the path for a given directory ID based on its dependencies.
    """
    current_path = []
    for entry in directory_data:
        if entry["id"] == directory_id:
            current_path.insert(0, entry["name"])
            while entry.get("parent_id"):
                entry = next((e for e in directory_data if e["id"] == entry["parent_id"]), None)
                if entry:
                    current_path.insert(0, entry["name"])
            break
    return os.path.join(*current_path)



new_name = "a2011-0051 (PPA on p66).pdf"
current_name = "2015-0389 (PPA on p114).pdf"
update_document_title(current_name, new_name)

"""
file_name = "2020-0137 (PPA on p41).pdf"
new_dir_id = 1  # Ensure this is an integer

# Call the function to move the file and update the JSON
move_file(file_name, new_dir_id)
"""


##### this is quite stupid. if you want to change the name of a file or move 
#it you have to first move it in the folder structure but then update both the metadata file and the directory
# should have it all in one file