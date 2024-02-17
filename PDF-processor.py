import streamlit as st
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import io
import json
import PyPDF2

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        # Read the uploaded PDF file
        pdf_reader = PdfReader(uploaded_file)
        # Extract text from each page
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        st.error(f"An error occurred while extracting text: {str(e)}")
    return text


def convert_pdf_to_json(pdf_file):
    json_structure = []

    with pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text()

            # Split the text into paragraphs
            paragraphs = page_text.split('\n\n')

            # Create a JSON object for each paragraph
            for paragraph in paragraphs:
                json_structure.append({"text": paragraph.strip(), "page": page_num + 1})

    return json_structure
def main():
    st.title("CMI2I PDF Reader")

    # Add a file uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    button_clicked = st.button("Submit")
    json_btn = st.button("Convert Text to JSON")

    # Check if the button is clicked
    if button_clicked:
        if uploaded_file is not None:
            # Display the extracted text
            st.subheader("Text Extracted from PDF")
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.text(extracted_text)

    if json_btn:
        json_structure = convert_pdf_to_json(uploaded_file)
        st.subheader("JSON Structure of Text")
        st.json(json_structure)


if __name__ == "__main__":
    main()
