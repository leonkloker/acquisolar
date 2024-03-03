import json
import os
import shutil
import openai

def process_json_add_extension(data):
    """
    Appends the appropriate file extension to the suggested titles in the JSON data,
    if they are missing.
    
    Parameters:
    - data: The JSON data containing the metadata and suggested titles.
    
    Returns:
    - The modified data with file extensions appended to suggested titles.
    """
    _, file_extension = os.path.splitext(data.get('original_title', ''))
    for key in ['Suggested_title', 'Suggested_title_v2', 'Suggested_title_v3']:
        if key in data and not data[key].endswith(file_extension):
            data[key] += file_extension
    return data




def make_openai_api_call(query, api_key):
    """
    Sends a query to the OpenAI API and returns the response.

    Parameters:
    - query: The query string to send to the OpenAI API.
    - api_key: The API key for authenticating with the OpenAI API.

    Returns:
    - The API response as a string.
    """
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
          engine="davinci",  # Or whichever engine you're using
          prompt=query,
          temperature=0.7,
          max_tokens=150,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error making OpenAI API call: {e}")
        return "{}"  # Return an empty JSON structure in case of error




def process_pdf(pdf_path, output_dir, folder_structure_indented, project_name, action="copy"):
    """
    Processes a PDF file by extracting its content, querying for metadata,
    and moving or copying it to the designated folder based on the classification.
    
    Parameters:
    - pdf_path: The path to the PDF file.
    - output_dir: The base output directory where the structured data folder is located.
    - folder_structure_indented: Indented string representation of the folder structure.
    - project_name: Name of the project, used in constructing the folder path.
    - action: Specifies whether to move or copy the file.
    """
    from pdf_processing import extract_pdf_info
    from query_processing import construct_query, truncate_query_to_fit_context, make_json_valid
    from file_ops import save_txt_file

    extracted_text, num_pages, title = extract_pdf_info(pdf_path)
    if not extracted_text or num_pages == 0:
        print(f"Skipping {os.path.basename(pdf_path)} due to extraction error.")
        return

    query = construct_query(extracted_text, folder_structure_indented)
    truncated_query = truncate_query_to_fit_context(query)
    output_json = make_openai_api_call(truncated_query, api_key)
    data = json.loads(output_json)

    data = process_json_add_extension(data)

    document_folder_path = data.get("Document_folder_path", project_name + "/Unclassified")
    if not document_folder_path.startswith(project_name):
        document_folder_path = os.path.join(project_name, "Unclassified")

    final_path = os.path.join(output_dir, document_folder_path)
    os.makedirs(final_path, exist_ok=True)

    if action == "copy":
        shutil.copy(pdf_path, os.path.join(final_path, os.path.basename(pdf_path)))
    else:
        shutil.move(pdf_path, os.path.join(final_path, os.path.basename(pdf_path)))

    append_to_complete_metadata_file(data, os.path.join(output_dir, "complete_file_metadata.json"))  # This function is defined in file_ops.py

def append_to_complete_metadata_file(data, file_path):
    """
    Appends a new entry to the complete metadata file or creates it if it doesn't exist.
    
    Parameters:
    - data: The new metadata entry to be added.
    - file_path: The path to the metadata file.
    """
    from file_ops import append_to_complete_metadata_file
    append_to_complete_metadata_file(data, file_path)
