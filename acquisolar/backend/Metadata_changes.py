import json
import os
import shutil
import zipfile


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
def load_directory_data(directory_path):
    with open(directory_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Find file path for a given name
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
def find_current_file_directory(file_name, directory_data):
    """
    Finds the current directory ID and path for the specified file.
    """
    for entry in directory_data:
        if entry["name"] == file_name and entry["type"] == "file":
            # Construct the path to this file
            current_dir_id = entry["parent_id"]
            current_dir_path = construct_path(current_dir_id, directory_data)
            return current_dir_id, current_dir_path
    return None, None

# Rename files
def rename_file_physical(current_path, new_name):
    new_path = os.path.join(os.path.dirname(current_path), new_name)
    shutil.move(current_path, new_path)
    print(f"File renamed to {new_path}")
    return new_path
def rename_file_metadata(file_name, new_name, metadata_path):
    # Update in `complete_file_metadata.json`
    with open(metadata_path, 'r+', encoding='utf-8') as file:
        metadata = json.load(file)
        updated = False
        for file_metadata in metadata:
            # Assuming "current_title" is the key used for matching
            if file_metadata.get("current_title") == file_name:
                file_metadata["current_title"] = new_name  # Update "current_title" to the new name
                updated = True
                break
        if updated:
            file.seek(0)
            file.truncate()
            json.dump(metadata, file, indent=4)
            print(f"Metadata updated for {new_name}.")
def rename_file_directory(file_name, new_name, directory_path):
    # Update in `global_directory.json`
    with open(directory_path, 'r+', encoding='utf-8') as file:
        directory_data = json.load(file)
        updated = False
        for entry in directory_data:
            if entry["name"] == file_name and entry["type"] == "file":
                entry["name"] = new_name  # Update the file name in the directory data
                updated = True
                break
        if updated:
            file.seek(0)
            file.truncate()
            json.dump(directory_data, file, indent=4)
            print(f"Directory entry updated for {new_name}.")
def rename_file(file_name, new_name):
    root_directory = set_root_directory()
    metadata_path, directory_path = set_metadata_and_directory_file_path(root_directory)
    directory_data = load_directory_data(directory_path)
    
    # Find the current file path
    current_path = find_file_path(file_name, directory_data)
    if not current_path:
        print(f"File {file_name} not found.")
        return
    full_current_path = os.path.join(root_directory, "structured_data", current_path)

    # Rename the physical file
    full_new_path = rename_file_physical(full_current_path, new_name)

    # Update metadata and directory entries
    rename_file_metadata(file_name, new_name, metadata_path)
    rename_file_directory(file_name, new_name, directory_path)

    print(f"File {file_name} successfully renamed to {new_name} in filesystem, metadata, and directory data.")

# Move files
def move_file_physical(src_path, dest_path):
    shutil.move(src_path, dest_path)
    print(f"Physically moved file to {dest_path}")
def move_file_directory(directory_path, file_name, new_dir_id, directory_data):
    updated = False
    for entry in directory_data:
        if entry["name"] == file_name and entry["type"] == "file":
            entry["parent_id"] = new_dir_id
            updated = True
            break
    if updated:
        with open(directory_path, 'w', encoding='utf-8') as file:
            json.dump(directory_data, file, indent=4)
            print(f"Updated {file_name} directory in global_directory.json")
def move_file_metadata(metadata_path, file_name, new_folder_path):
    with open(metadata_path, 'r+', encoding='utf-8') as file:
        metadata = json.load(file)
        updated = False
        new_folder_path = os.path.normpath(new_folder_path)  # Normalize the new folder path
        for file_metadata in metadata:
            if file_metadata.get("current_title") == file_name or file_metadata.get("original_title") == file_name:
                file_metadata["Document_folder_path"] = new_folder_path.replace('\\', '/')  # Normalize to use forward slashes
                updated = True
                break
        if updated:
            file.seek(0)
            file.truncate()
            json.dump(metadata, file, indent=4)
            print(f"Updated Document_folder_path for {file_name} in metadata.")
def move_file(file_name, new_dir_id):
    root_directory = set_root_directory()
    metadata_path, directory_path = set_metadata_and_directory_file_path(root_directory)
    directory_data = load_directory_data(directory_path)

    # Determine the new directory path
    new_dir_path = construct_path(new_dir_id, directory_data)
    new_folder_path = new_dir_path  # Assuming this is the format for Document_folder_path

    # Find the current directory ID and path for the file
    current_dir_id, current_dir_path = find_current_file_directory(file_name, directory_data)
    if current_dir_id is None:
        print(f"File {file_name} not found in global_directory.json.")
        return
    
    current_dir_full_path = os.path.join(root_directory, "structured_data", current_dir_path)
    new_dir_full_path = os.path.join(root_directory, "structured_data", new_folder_path)
    
    # Move the file physically
    src_path = os.path.join(current_dir_full_path, file_name)
    dest_path = os.path.join(new_dir_full_path, file_name)
    move_file_physical(src_path, dest_path)

    # Update directory and metadata
    move_file_directory(directory_path, file_name, new_dir_id, directory_data)
    move_file_metadata(metadata_path, file_name, new_folder_path)

    print(f"File {file_name} successfully moved to {new_folder_path} in filesystem, metadata, and directory data.")

# Take notes
def take_notes(file_name, input_text):
    root_directory = set_root_directory()
    metadata_path, _ = set_metadata_and_directory_file_path(root_directory)

    updated = False
    with open(metadata_path, 'r+', encoding='utf-8') as file:
        metadata = json.load(file)
        for file_metadata in metadata:
            # Check if the file name matches
            if file_metadata.get("current_title") == file_name or file_metadata.get("original_title") == file_name:
                # Update the notes field
                file_metadata["notes"] = input_text
                updated = True
                break
        
        if updated:
            # Go back to the start of the file and truncate to overwrite with updated data
            file.seek(0)
            file.truncate()
            # Write the updated metadata back to the file
            json.dump(metadata, file, indent=4)
            print(f"Notes updated for {file_name}.")
        else:
            print(f"File {file_name} not found in metadata.")

def retrieve_original_file_name(current_file_name):
    """
    Retrieves the original file name based on the current file name.
    
    Parameters:
    - current_file_name: The current name of the file.
    - metadata_path: The path to the file containing the metadata.
    
    Returns:
    The original file name if found, else None.
    """
    root_directory = set_root_directory()
    metadata_path, _ = set_metadata_and_directory_file_path(root_directory)
    with open(metadata_path, 'r', encoding='utf-8') as file:
        metadata = json.load(file)
        for entry in metadata:
            if entry.get("current_title") == current_file_name:
                # Assuming "original_title" is the key for the original file name
                return entry.get("original_title")
    return None

def zip_directory(project_name = "project"):
    root_directory = set_root_directory()
    zip_dir_path = os.path.join(root_directory, "zip_output", f"{project_name}.zip")
    print(zip_dir_path)
    project_path = os.path.join(root_directory, "structured_data", project_name)
    # Ensure the ZIP file's directory exists
    os.makedirs(os.path.dirname(zip_dir_path), exist_ok=True)
    # Create a ZIP file
    with zipfile.ZipFile(zip_dir_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                # Create the full path to the file
                file_path = os.path.join(root, file)
                # Calculate the relative path to maintain the directory structure
                rel_path = os.path.relpath(file_path, os.path.commonpath([project_path, file_path]))
                # Add the file to the ZIP archive
                zipf.write(file_path, rel_path)

    print(f"ZIP file created at: {zip_dir_path}")
    return True


""" Example use: change name"""
#file_name = "LOI2.pdf"
#new_name = "LOI.pdf"

#rename_file(file_name, new_name)

""" Example use: move file"""
#file_name = "PPA_new_name.pdf"
#new_dir_id = 2

#move_file(file_name, new_dir_id)

""" Example use: add text"""
#file_name = "PPA_new_name.pdf"
input_text = f"""
HEllo 
here are some notes
that i want to store
"""
#take_notes(file_name, input_text)


""" Example use """

#original_file_name = retrieve_original_file_name(current_file_name)



""" Example use: Zip folder structure"""
zip_directory("project")