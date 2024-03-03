from file_ops import set_root_directory, construct_relative_paths
from folder_structure import find_and_note_zip_structure, create_folder_structure_from_list
from directory_json import generate_directory_json
from convert_directory import convert_and_save_directory_structure
from accuracy_tracking import load_expected_classifications, calculate_accuracy, update_accuracy_tracker
import os

# Adjust these paths and values according to your actual project configuration
project_name = 'MegaSolar'
api_key = "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"  

def main():
    # Initialize the environment by setting the root directory
    root_directory = set_root_directory()

    # Automatically construct paths for input and output directories
    input_dir, output_dir = construct_relative_paths(root_directory)

    # Process the zip file to analyze and create the necessary folder structure
    folder_structure_info = find_and_note_zip_structure(input_dir, project_name)
    folder_structure_list, folder_structure_indented, folder_structure_text_list = folder_structure_info
    if folder_structure_list is not None:
        base_output_dir = os.path.join(output_dir, project_name)  # Ensure this is your desired base output directory
        create_folder_structure_from_list(folder_structure_list, base_output_dir)

    # Here, add your logic to process PDFs, such as iterating over files in `input_dir`
    # For example:
    # for pdf_file in os.listdir(input_dir):
    #     if pdf_file.lower().endswith('.pdf'):
    #         pdf_path = os.path.join(input_dir, pdf_file)
    #         process_pdf(pdf_path, output_dir, folder_structure_indented, project_name, action="copy")

    # Generate a JSON file that represents the directory structure
    generate_directory_json(output_dir, project_name)

    # Convert and save the directory structure for frontend usage
    input_json_path = os.path.join(output_dir, 'global_directory.json')
    output_json_path = os.path.join(output_dir, 'directory_for_frontend.json')
    convert_and_save_directory_structure(input_json_path, output_json_path)

    # Load expected classifications, calculate accuracy, and update the accuracy tracker
    # This section assumes you have a JSON file with expected classifications and a mechanism to generate predictions
    expected_classifications = load_expected_classifications('structured_data/directory_for_frontend.json')
    # Replace this with your actual logic to generate predictions based on processed PDFs
    predictions = {}  # Dummy placeholder
    accuracy = calculate_accuracy(predictions, expected_classifications)
    print(f"Classification accuracy: {accuracy}%")

    update_accuracy_tracker('accuracy_tracker.csv', accuracy)

if __name__ == "__main__":
    main()