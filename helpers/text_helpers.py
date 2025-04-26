"""Functions related to the extraction of text."""

from PyPDF2 import PdfReader


def extract_text_from_pdf(dir_path: str, file_name: str):
    """
    Uses reader object to read in first page of pdf in dir_path, under assumption all important will be on the first page
    """
    reader = PdfReader(dir_path + file_name)
    page = reader.pages[0]
    return page.extract_text()
