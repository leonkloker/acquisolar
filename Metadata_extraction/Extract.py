import fitz  # PyMuPDF
import os
from openai import OpenAI
import requests
import json
import tiktoken

client = OpenAI(api_key="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")  # Text completion

def set_directory_for_input_document():
    # Change the working directory my local one
    target_directory = r'C:\Users\MBAUser\AcquiSolar\Metadata_extraction'
    os.chdir(target_directory)
    print("Current working directory:", os.getcwd())
def extract_text_from_pdf(pdf_name):
    doc = fitz.open(pdf_name)
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        # Split text into lines
        lines = text.split('\n')
        # Reassemble text with conditional newlines
        new_text = ""
        for line in lines:
            # Strip leading and trailing whitespace
            stripped_line = line.strip()
            if stripped_line:  # Ensure line is not empty
                # Check if line ends with a sentence-ending punctuation or is likely a list item
                if stripped_line.endswith(('.', '?', '!', ':', ';', '-', '—')) or stripped_line[-1].isdigit():
                    new_text += stripped_line + "\n"
                else:
                    # Append a space to continue the sentence if it's broken up
                    new_text += stripped_line + " "
        full_text += new_text
    doc.close()
    return full_text
def truncate_query_to_fit_context(query, max_length=11000):
    """
    Truncate a query to ensure it fits within the specified maximum length.
    Parameters:
    - query: The text query to be truncated.
    - max_length: The maximum allowed length in tokens. Defaults to 2048.
    Returns:
    - Truncated query.
    """
    # Split the query into words
    words = query.split()
    
    # Simple approximation: assuming 1 word = 1 token
    # For more accuracy, especially with non-English text or technical content,
    # consider using a tokenizer from libraries like transformers to count tokens.
    if len(words) <= max_length:
        return query  # The query is short enough
    
    truncated_query = ""
    token_count = 0
    
    for word in words:
        if token_count + len(word.split()) > max_length:
            break  # Stop adding words if the next word would exceed the limit
        truncated_query += word + " "
        token_count += 1
    
    return truncated_query.strip()
def construct_query(extracted_text):
    return f"""
Extract the following fields from the document text provided and format the response as JSON:
- "Document date" in the format '3 letter month name-DD, YYYY'.
- "Document summary" limited to a maximum of 3 sentences, tailored for a solar M&A analyst. It should state what kind of document it is, but also what its implicatoins are or what state it is in. It should assume the analyst knows about the M&A process.
- "Document type", which should be either 'PPA' or 'Interconnection document' or 'email' or 'site control'.
- "Suggested title" in the format 'MM-DD-YYYY max 5 word document title (state)' the state field is optional. It can read "main" if it is said to be the main document of its type, it can read (redacted) if it is redacted.
- "Suggested title v2" in same format as "suggested title" but with different wording
- "Suggested title v3" in same format as "suggested title" but with different wording
- "suggested folder" from the selection: "PPA", "interconnection", "uncategorized", "site control"

The provided document text is:
{extracted_text}
"""
def output_extracted_text_to_file(extracted_text):
    with open("Extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
def save_json_with_pdf_name(json_str, pdf_name):
    """
    Saves a JSON string to a file with the same base name as the input PDF file but with a .json extension.

    Parameters:
    - json_str (str): The JSON string to save.
    - pdf_name (str): The filename of the PDF, used to derive the JSON filename.

    Returns:
    - None
    """
    # Extract the base filename without the extension
    base_name = os.path.splitext(pdf_name)[0]
    # Construct the JSON filename
    json_filename = f"{base_name}.json"
    
    try:
        # Convert the JSON string to a Python dictionary
        data = json.loads(json_str)
        # Open the file in write mode and save the JSON
        with open(json_filename, 'w') as file:
            json.dump(data, file, indent=4)  # Pretty print the JSON
        print(f"JSON data successfully saved to {json_filename}")
    except Exception as e:
        print(f"Error saving JSON to file: {e}")

set_directory_for_input_document()                      # Set directory of where to find pdf
pdf_name = 'PPA.pdf'                                    # Define the name of the file
extracted_text = extract_text_from_pdf(pdf_name)        # turn PDF into text
output_extracted_text_to_file(extracted_text)           # View result of PDF to txt conversion
query = construct_query(extracted_text)                 # Merge question with text for prompt
truncated_query = truncate_query_to_fit_context(query)  # truncate query to fit in context length. not optimal

# API call
completion = client.chat.completions.create(
  #model="gpt-3.5-turbo",
    #model="gpt-4-32k",
  model="gpt-3.5-turbo-0125", # longer context length than 3.5 turbo --- https://platform.openai.com/docs/models/gpt-3-5-turbo
  messages=[
    {"role": "system", "content": "You are a solar M&A analyst and great at extracting summaries and text from M&A documentation. Under no circumstances do you halucinate, instead you say that you leave a field blank if you cannot answer"},
    {"role": "user", "content": truncated_query}
  ]
)
output_json = completion.choices[0].message.content     # get message contents from api call

print(output_json)                                      # print results
save_json_with_pdf_name(output_json, pdf_name)          # save results to JSON file with same name as PDF
