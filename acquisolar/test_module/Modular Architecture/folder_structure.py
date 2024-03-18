import os
import zipfile

def find_and_note_zip_structure(input_dir, project_name):
    """
    Finds the first zip file in the input directory, analyzes its folder structure,
    and replaces the top-level folder name with the project name.

    Parameters:
    - input_dir: The directory to search for the zip file.
    - project_name: The project name to use in place of the top-level folder name.

    Returns:
    - A tuple containing a list representation of the folder structure,
      an indented string representation, and a list in text form suitable for JSON.
    """
    zip_file = None
    for file in os.listdir(input_dir):
        if file.lower().endswith('.zip'):
            zip_file = os.path.join(input_dir, file)
            break

    if not zip_file:
        print("No zip file found in the input directory.")
        return None, None, None

    folder_structure = analyze_zip_structure(zip_file, project_name)
    folder_structure_list = dict_to_nested_list(folder_structure)
    folder_structure_indented = folder_structure_to_text(folder_structure_list)
    folder_structure_text_list = nested_list_to_text_list(folder_structure_list)

    return folder_structure_list, folder_structure_indented, folder_structure_text_list

def analyze_zip_structure(zip_file, project_name):
    """
    Analyzes the folder structure within a zip file.

    Parameters:
    - zip_file: The path to the zip file.
    - project_name: The project name to use in place of the top-level folder name.

    Returns:
    - A dictionary representing the folder structure.
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()

        folder_structure = {}
        for item in zip_contents:
            path_parts = item.split('/')
            if path_parts[0]:  # Replace top-level folder name with project_name
                path_parts[0] = project_name
            current_level = folder_structure
            for part in path_parts[:-1]:  # Exclude file names
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
    return folder_structure

def dict_to_nested_list(d):
    """
    Converts a dictionary representing folder structure to a nested list.

    Parameters:
    - d: The dictionary to convert.

    Returns:
    - A nested list representing the folder structure.
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
    Converts a nested list representing folder structure into indented text.

    Parameters:
    - structure: The nested list to convert.
    - level: The current indentation level.

    Returns:
    - A string representing the folder structure with indentation.
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
    Converts a nested list representing folder structure into a structured list in text form.

    Parameters:
    - structure: The nested list to convert.
    - level: The current level of nesting.

    Returns:
    - A text representation of the structured list, suitable for JSON.
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


def create_folder_structure_from_list(folder_structure, base_path):
    """
    Recursively creates folders based on the nested list structure representing the folder hierarchy.
    
    Parameters:
    - folder_structure: A nested list representing the folder structure.
    - base_path: The base path where the folder structure should be created.
    """
    for item in folder_structure:
        if isinstance(item, list):
            # If the item is a list, the first element is the folder name,
            # and the second element is a nested list representing subfolders.
            folder_name = item[0]
            subfolders = item[1]
            folder_path = os.path.join(base_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            create_folder_structure_from_list(subfolders, folder_path)
        else:
            # If the item is not a list, it's a folder name at the current level.
            folder_path = os.path.join(base_path, item)
            os.makedirs(folder_path, exist_ok=True)

