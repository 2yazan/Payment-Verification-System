# import pytesseract
# from PIL import Image
# import pymupdf as fitz  # PyMuPDF
# import re
# import spacy
# import io  # Import the io module

# def extract_text_from_file(file_obj):
#     file_obj.seek(0)  # Reset the file pointer
#     file_bytes = file_obj.read()

#     # Create a BytesIO object from the file content
#     file_stream = io.BytesIO(file_bytes)

#     # Open the file using PyMuPDF
#     doc = fitz.open("pdf", file_stream)  # Open the file as a PDF

#     text = ""
#     for page in doc:
#         # Check if the page is an image
#         if page.get_images():
#             # Extract text from the image using Tesseract OCR
#             image_stream = io.BytesIO(file_bytes)
#             image = fitz.Pixmap(doc, image_stream)
#             custom_config = r'--oem 3 --psm 6'
#             text += pytesseract.image_to_string(image.pil_tobytes(), lang='rus+eng', config=custom_config)
#         else:
#             # Extract text from the PDF page
#             text += page.get_text()

#     return text

# def extract_text_from_image(image_path):
#     # Load the image
#     image = Image.open(image_path)

#     # Define configurations for Tesseract OCR
#     custom_config = r'--oem 3 --psm 6'

#     # Extract text from the image
#     extracted_text = pytesseract.image_to_string(image, lang='rus+eng', config=custom_config)

#     return extracted_text

# def extract_sender_and_amount(text):
#     # Extract sender number using regular expressions
#     pattern = r"SENDER:\s*(\d+)"
#     match = re.search(pattern, text, re.MULTILINE)
#     if match:
#         sender = match.group(1)
#     else:
#         sender = None

#     # Extract amount using spaCy
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text)
#     amount = None
#     for ent in doc.ents:
#         if ent.label_ == "MONEY":
#             amount = ent.text

#     return sender, amount

# Example usage for image
# image_path = 'C:\\Users\\yazon\\Desktop\\test_ocr_ner\\ch1.png'
# check_text = extract_text_from_image(image_path)
# sender, amount = extract_sender_and_amount(check_text)
# print("Sender:", sender)
# print("Amount:", amount)



import tkinter as tk
from tkinter import filedialog
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import re
import spacy
import json

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        # Extract text from PDF
        with fitz.open(file_path) as pdf_file:
            text = ""
            for page in pdf_file:
                text += page.get_text()
    else:
        # Extract text from image
        image = Image.open(file_path)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, lang='rus+eng', config=custom_config)

    return text

def extract_sender_and_amount(text):
    # Extract sender number using regular expressions
    pattern = r"SENDER:\s*(\d+)"
    match = re.search(pattern, text, re.MULTILINE)
    if match:
        sender = match.group(1)
    else:
        sender = None

    # Extract amount using spaCy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    amount = None
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            amount = ent.text

    return sender, amount

# def open_file():
#     file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
#     if file_path:
#         text = extract_text_from_file(file_path)
#         sender, amount = extract_sender_and_amount(text)
#         result = {
#             "sender": sender,
#             "amount": amount
#         }
#         print(json.dumps(result, indent=2))

# root = tk.Tk()
# root.title("Extract Sender and Amount")

# open_button = tk.Button(root, text="Open File", command=open_file)
# open_button.pack(pady=10)

# root.mainloop()













# def extract_text_from_file(file_path):
#     if file_path.endswith(".pdf"):
#         # Extract text from PDF
#         with fitz.open(file_path) as pdf_file:
#             text = ""
#             for page in pdf_file:
#                 text += page.get_text()
#     else:
#         # Extract text from image
#         image = Image.open(file_path)
#         custom_config = r'--oem 3 --psm 6'
#         text = pytesseract.image_to_string(image, lang='rus+eng', config=custom_config)

#     return text

# def extract_sender_and_amount(text):
#     # Extract sender number using regular expressions
#     pattern = r"SENDER:\s*(\d+)"
#     match = re.search(pattern, text, re.MULTILINE)
#     if match:
#         sender = match.group(1)
#     else:
#         sender = None

#     # Extract amount using spaCy
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text)
#     amount = None
#     for ent in doc.ents:
#         if ent.label_ == "MONEY":
#             amount = ent.text

#     return sender, amount