import json
import json
import os
from openai import OpenAI

def truncate_query_to_fit_context(query, max_length=10000, enable_testing_output=False): #35k is ok for gpt-4-0125-preview #10k max for gpt-3.5-turbo-0125
    """
    Truncate a query to ensure it fits within the specified maximum length, preserving new lines and indentation.
    This version considers the query as a series of lines.
    
    Parameters:
    - query: The text query to be truncated.
    - max_length: The maximum allowed length in tokens. Defaults to 50000.
    
    Returns:
    - Truncated query with preserved formatting.
    """
    # Split the query into lines instead of words to preserve formatting
    lines = query.split('\n')
    truncated_query = ""
    token_count = 0
    total_token_count = sum(len(line.split()) for line in lines)  # Total tokens in the original query

    for line in lines:
        line_token_count = len(line.split())  # Estimate token count for the line
        if token_count + line_token_count > max_length:
            break  # Stop adding lines if the next line would exceed the limit
        truncated_query += line + "\n"  # Add the line back with its newline character
        token_count += line_token_count
    
    # Calculate and print the percentage of the query used
    percentage_used = (token_count / total_token_count) * 100 if total_token_count > 0 else 0
    print(f"Percentage of the document used: {percentage_used:.2f}%")
    
    save_txt_file("truncated_query.txt", truncated_query, enable_testing_output)
    return truncated_query.rstrip()  # Remove the last newline character to clean up

def construct_query(extracted_text, folder_structure_indented, enable_testing_output=False):
    """
    Constructs a detailed query for the OpenAI API based on extracted text and
    the folder structure of the documents.
    
    Parameters:
    - extracted_text: The text extracted from a document.
    - folder_structure_indented: A string representing the indented folder structure.
    - enable_testing_output: Flag to enable testing outputs.
    
    Returns:
    - A string representing the constructed query.
    """
    query = f"""
Extract the following fields from the document text provided and format the response as valid JSON:
- "Document_date" in the format '3 letter month name-DD, YYYY'.
- "Document_summary" limited to a maximum of 3 sentences, tailored for a solar M&A analyst. It should state what kind of document it is, but also what its implicatoins are or what state it is in. It should assume the analyst knows about the M&A process.
- "Suggested_title" in the format 'MM-DD-YYYY max 5 word document title'. Try your best to come up with a title that is useful if you quickly want to understand what kind of document it is
- "Suggested_title_v2" in same format as "suggested title" but with different wording
- "Suggested_title_v3" in same format as "suggested title" but with different wording
- "Document_folder_path": Select the most suitable folder or sub-folder from the list using "project_name/sub_folder...". If no match, use "project_name/Unclassified". No new folders. "Interconnection Agreement" for the agreement itself, related documents in "Interconnection Agreement Supplementary Documents". "PPA" for the agreement, related documents in "PPA Supplementary Documents".
{folder_structure_indented}

The provided document text is:
{extracted_text}
"""
    # Optionally, log the query for testing purposes
    if enable_testing_output:
        print("Query constructed for OpenAI API.")
    return query

def make_json_valid(response_content):
    """
    Ensures that the response content is a valid JSON object by removing any
    text outside the outermost JSON object braces.
    
    Parameters:
    - response_content: The potentially malformed JSON string.
    
    Returns:
    - A cleaned JSON string.
    """
    start_index = response_content.find('{')
    end_index = response_content.rfind('}')
    
    if start_index != -1 and end_index != -1 and end_index > start_index:
        valid_json = response_content[start_index:end_index+1]
    else:
        print("Valid JSON object not found in the response.")
        valid_json = "{}"

    try:
        # Attempt to load the JSON to ensure its validity
        json.loads(valid_json)
    except json.JSONDecodeError:
        print("Failed to parse JSON. Returning empty object.")
        return "{}"

    return valid_json

# Other functions like construct_query, truncate_query_to_fit_context, make_json_valid...

def make_openai_api_call(query, api_key):
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a solar M&A analyst..."},
                {"role": "user", "content": query}
            ],
            model="gpt-3.5-turbo-0125"
        )
        # Parse the response to extract the content generated by the model
        response_content = response.choices[0].message.content
    except Exception as e:
        print(f"Error making OpenAI API call: {e}")
        return "{}"  # Return a default empty JSON structure in case of error
    
    valid_json_string = make_json_valid(response_content)
    return valid_json_string


