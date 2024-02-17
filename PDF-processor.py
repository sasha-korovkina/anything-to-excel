import streamlit as st
from PyPDF2 import PdfReader

def main():
    st.title("Simple Streamlit App")

    # Add a file uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Add a button widget
    button_clicked = st.button("Submit")

    # Check if the button is clicked
    if button_clicked:
        if uploaded_file is not None:
            # Read the uploaded PDF file
            pdf_reader = PdfReader(uploaded_file)
            num_pages = len(pdf_reader.pages)
            st.write(f"Number of pages in the PDF: {num_pages}")
        else:
            st.warning("Please upload a PDF file")

if __name__ == "__main__":
    main()
