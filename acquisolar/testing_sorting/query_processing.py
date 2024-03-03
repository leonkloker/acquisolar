import json

def truncate_query_to_fit_context(query, max_length=10000, enable_testing_output=False):
    """
    Truncates a query to ensure it fits within the specified maximum length,
    preserving new lines and indentation to maintain formatting.
    
    Parameters:
    - query: The text query to be truncated.
    - max_length: The maximum allowed length in tokens.
    - enable_testing_output: Flag to enable testing outputs.
    
    Returns:
    - Truncated query with preserved formatting.
    """
    lines = query.split('\n')
    truncated_query = ""
    token_count = 0
    total_token_count = sum(len(line.split()) for line in lines)  # Total tokens in the original query

    for line in lines:
        line_token_count = len(line.split())
        if token_count + line_token_count > max_length:
            break  # Stop adding lines if the next line would exceed the limit
        truncated_query += line + "\n"
        token_count += line_token_count

    # Optionally, log the percentage of the document used for testing purposes
    if enable_testing_output:
        percentage_used = (token_count / total_token_count) * 100 if total_token_count > 0 else 0
        print(f"Percentage of the document used: {percentage_used:.2f}%")

    return truncated_query.rstrip()  # Clean up the last newline character

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
- "Document_summary" limited to a maximum of 3 sentences, tailored for a solar M&A analyst.
- "Suggested_title" in the format 'MM-DD-YYYY max 5 word document title'.
- "Document_folder_path", Choose the folder that makes most sense from the folders below.
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
