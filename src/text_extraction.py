import os
import easyocr
from PIL import Image
import pdfplumber

class FileTextExtractor:
    """
    A class to extract text from different file types, including images (JPEG, JPG, PNG), PDFs, and TXT files.

    Methods
    -------
    extract_text(file_path):
        Extracts text from the given file based on its format.
    """
    
    def __init__(self):
        # Initialize the EasyOCR reader for English language
        self.ocr_reader = easyocr.Reader(['en'])
    
    def extract_text(self, file_path: str) -> str:
        """
        Extracts text from the given file based on its format.

        Parameters
        ----------
        file_path : str
            The path of the file from which to extract text.

        Returns
        -------
        str
            Extracted text from the file.
        """
        # Check the file extension
        ext = file_path.lower().split('.')[-1]

        if ext in ['jpeg', 'jpg', 'png']:
            return self.extract_text_from_image(file_path)
        elif ext == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext == 'txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError('Unsupported file format: {}'.format(ext))

    def extract_text_from_image(self, image_path: str) -> str:
        '''
        Extracts text from an image using EasyOCR.

        Parameters
        ----------
        image_path : str
            The path of the image file.

        Returns
        -------
        str
            Extracted text from the image.
        '''
        try:
            result = self.ocr_reader.readtext(image_path, detail=0)  # Extract text without bounding box details
            return '\n'.join(result)  # Combine all lines of text into one string
        except Exception as e:
            return 'Error extracting text from image: {}'.format(str(e))

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        '''
        Extracts text from a PDF file.

        Parameters
        ----------
        pdf_path : str
            The path of the PDF file.

        Returns
        -------
        str
            Extracted text from the PDF.
        '''
        try:
            text = ''
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + '\n'
            return text if text.strip() else 'No text found in PDF.'
        except Exception as e:
            return 'Error extracting text from PDF: {}'.format(str(e))

    def extract_text_from_txt(self, txt_path: str) -> str:
        '''
        Extracts text from a plain text file.

        Parameters
        ----------
        txt_path : str
            The path of the text file.

        Returns
        -------
        str
            Extracted text from the text file.
        '''
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return 'Error reading text file: {}'.format(str(e))

