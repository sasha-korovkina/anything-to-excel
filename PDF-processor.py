import streamlit as st
import pandas as pd
import tabula
import tempfile
import os
from openpyxl import load_workbook

# Set page title
st.set_page_config(page_title="PDF to Excel Converter")


def main():
    st.title("PDF to Excel Converter")

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Display file details
        st.write("### Uploaded file details:")
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)

        # Convert PDF to Excel
        st.write("### Convert PDF to Excel:")
        if st.button("Convert to Excel"):
            # Extract tables from PDF using tabula
            tables = tabula.read_pdf(uploaded_file, pages="all", multiple_tables=True)

            # Convert each table to a DataFrame
            excel_dataframes = [pd.DataFrame(table) for table in tables]

            # Create Excel file
            excel_file_path = "output.xlsx"

            # Display download link
            st.write("Download Excel file:")
            st.download_button(label="Download", data=open(excel_file_path, "rb"), file_name="output.xlsm")

if __name__ == "__main__":
    main()
