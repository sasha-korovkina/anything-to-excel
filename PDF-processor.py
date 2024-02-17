import streamlit as st
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import io

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

def main():
    st.title("Simple Streamlit App")

    # Add a file uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Add a button widget
    button_clicked = st.button("Submit")

    # Check if the button is clicked
    if button_clicked:
        if uploaded_file is not None:
            # Display the extracted text
            st.subheader("Text Extracted from PDF")
            extracted_text = extract_text_from_pdf(uploaded_file)
            print(extracted_text)
            st.text(extracted_text)
        else:
            st.warning("Please upload a PDF file")

if __name__ == "__main__":
    main()
