from file_ops import set_root_directory, construct_relative_paths
from folder_structure import find_and_note_zip_structure, create_folder_structure_from_list
from directory_json import generate_directory_json
from convert_directory import convert_and_save_directory_structure
from accuracy_tracking import load_expected_classifications, calculate_accuracy, update_accuracy_tracker
from pdf_processing import extract_pdf_info
# Assuming query_processing.py contains the required functions
from query_processing import construct_query, truncate_query_to_fit_context, make_json_valid, make_openai_api_call
# Assuming openai_integration.py or a similar file contains the make_openai_api_call function
import os
import json

# Adjust these paths and values according to your actual project configuration
project_name = 'MegaSolar'
api_key = "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"

def save_metadata(metadata, output_dir, pdf_file):
    """Saves extracted metadata to a JSON file."""
    filename = os.path.splitext(pdf_file)[0] + "_metadata.json"
    filepath = os.path.join(output_dir, 'metadata', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(metadata, f, indent=4)

def main():
    root_directory = set_root_directory()
    input_dir, output_dir = construct_relative_paths(root_directory)

    # Process the zip file to analyze and create the necessary folder structure
    folder_structure_info = find_and_note_zip_structure(input_dir, project_name)
    if folder_structure_info:
        base_output_dir = os.path.join(output_dir, project_name)
        folder_structure_list, folder_structure_indented, folder_structure_text_list = folder_structure_info
        create_folder_structure_from_list(folder_structure_list, base_output_dir)
        

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        full_text, num_pages, title = extract_pdf_info(pdf_path)
        if full_text:  # Ensuring text was extracted before proceeding
            folder_structure_indented = ""  # Define based on your actual folder structure
            query = construct_query(full_text, folder_structure_indented)
            truncated_query = truncate_query_to_fit_context(query)
            response_content = make_openai_api_call(truncated_query, api_key)
            valid_json_string = make_json_valid(response_content)
            # Process the valid_json_string to extract classification, metadata, etc.
            # Placeholder for processing the classification and updating metadata
            print(f"Processed {title} with classification and metadata extracted.")

    # Generate a JSON file that represents the directory structure
    generate_directory_json(output_dir, project_name)

    # Convert and save the directory structure for frontend usage
    input_json_path = os.path.join(output_dir, 'global_directory.json')
    output_json_path = os.path.join(output_dir, 'directory_for_frontend.json')
    convert_and_save_directory_structure(input_json_path, output_json_path)

    # Load expected classifications, calculate accuracy, and update the accuracy tracker
    expected_classifications = load_expected_classifications('acquisolar/testing_sorting/structured_data/directory_for_frontend.json')
    # Implement logic to generate predictions based on processed PDFs
    predictions = {}  # This should be replaced with actual prediction logic
    accuracy = calculate_accuracy(predictions, expected_classifications)
    print(f"Classification accuracy: {accuracy}%")

    update_accuracy_tracker('accuracy_tracker.csv', accuracy)

if __name__ == "__main__":
    main()
