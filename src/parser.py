import PyPDF2

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted text
    """
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "

    except Exception as e:
        raise Exception(f"Error reading PDF file: {e}")

    # Basic cleanup
    text = text.strip()

    if not text:
        raise ValueError("No text could be extracted from the PDF.")

    return text

