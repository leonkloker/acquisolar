import os
import json

def generate_directory_json(output_dir, project_name):
    """
    Generates a JSON file that represents the directory structure of the project,
    including directories and files, starting from the specified output directory.

    Parameters:
    - output_dir: The base output directory for the project.
    - project_name: The name of the project, used to identify the root directory.
    """
    project_path = os.path.join(output_dir, project_name)
    directory_tree = []
    next_id = 1  # Start IDs from 1 for identifying directories and files
    dir_id_map = {}  # Maps directory path to ID for setting parent-child relationships

    # Add the root project directory
    directory_tree.append({
        "id": next_id,
        "name": project_name,
        "type": "directory",
        "parent_id": None
    })
    dir_id_map[project_path] = next_id
    next_id += 1

    # Walk through the directory structure
    for root, dirs, files in os.walk(project_path):
        current_dir_id = dir_id_map[root]
        
        # Process each directory within the current root
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
            
        # Process each file within the current root, skipping JSON files
        for f in files:
            if not f.lower().endswith('.json'):  # Include non-JSON files only
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

    # Save the directory structure to a JSON file
    with open(os.path.join(output_dir, 'global_directory.json'), 'w', encoding='utf-8') as f:
        json.dump(directory_tree, f, indent=4)

