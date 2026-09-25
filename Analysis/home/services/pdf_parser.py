import pymupdf


def extract_text_from_pdf(file):
    """
    Extract text from an uploaded PDF file.

    Args:
        file: Django UploadedFile object

    Returns:
        str: Extracted and cleaned text
    """

    try:
        pdf_bytes = file.read()

        document = pymupdf.open(
    stream=pdf_bytes,
    filetype="pdf"
)

        pages_text = []

        for page in document:
            text = page.get_text("text")
            if text:
                pages_text.append(text)

        document.close()

        extracted_text = "\n".join(pages_text)

        # Clean unnecessary whitespace
        cleaned_text = "\n".join(
            line.strip()
            for line in extracted_text.splitlines()
            if line.strip()
        )

        return cleaned_text

    except Exception as exc:
        raise ValueError(f"Unable to extract text from PDF: {exc}")