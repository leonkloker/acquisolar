import fitz  # PyMuPDF
import os

def extract_pdf_info(pdf_path):
    """
    Extracts text, the document's name, and the number of pages from a PDF file.
    
    Parameters:
    - pdf_path: The file path to the PDF document.
    
    Returns:
    - full_text: All text extracted from the PDF.
    - num_pages: The number of pages in the PDF.
    - title: The name of the document, derived from the file name.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF file {pdf_path}: {e}")
        return "", 0, ""  # Return empty values on error

    full_text = ""
    title = os.path.basename(pdf_path)
    num_pages = len(doc)

    for page_num in range(num_pages):
        try:
            page = doc.load_page(page_num)
            text = page.get_text()
            # Process text line by line, maintaining structure while removing unnecessary whitespace
            lines = text.split('\n')
            new_text = process_text_lines(lines)
            full_text += new_text
        except Exception as e:
            print(f"Error processing page {page_num} of PDF file {pdf_path}: {e}")
            # Optionally, could break here to stop processing further pages on error

    doc.close()
    return full_text, num_pages, title

def process_text_lines(lines):
    """
    Processes lines of text extracted from a PDF page, cleaning and formatting.
    
    Parameters:
    - lines: A list of strings, each representing a line of text.
    
    Returns:
    - new_text: A single string with cleaned and concatenated lines.
    """
    new_text = ""
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            # Append the line with appropriate formatting based on its ending character
            if stripped_line.endswith(('.', '?', '!', ':', ';', '-', '—')) or stripped_line[-1].isdigit():
                new_text += stripped_line + "\n"
            else:
                new_text += stripped_line + " "
    return new_text
