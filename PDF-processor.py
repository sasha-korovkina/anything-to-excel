from PyPDF2 import PdfReader
import io
import PyPDF2
from pdfminer.high_level import extract_text
import xml.etree.ElementTree as ET
from streamlit_drawable_canvas import st_canvas
import streamlit as st
import fitz
import tempfile
from PIL import Image

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
            paragraphs = page_text.split('\n\n')
            for paragraph in paragraphs:
                json_structure.append({"text": paragraph.strip(), "page": page_num + 1})
    return json_structure

def extract_text_from_selection(pdf_bytes, selection_bbox):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc.load_page(0)  # Assuming first page, change index if needed
    selected_area = fitz.Rect(selection_bbox)
    selected_text = page.get_text("text", clip=selected_area)
    return selected_text

def convert_pdf_to_xml(pdf_file):
    root = ET.Element("document")
    text = extract_text(pdf_file)
    pages = text.split('\x0c')  # Split by page break character
    for i, page in enumerate(pages, 1):
        page_element = ET.SubElement(root, "page", number=str(i))
        page_element.text = page.strip()
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    return xml_str

def get_pdf_creation_software(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        metadata = reader.getDocumentInfo()
        if '/Producer' in metadata:
            return metadata['/Producer']
        else:
            return "Unknown"

def main():
    st.title("CMI2I PDF Reader")

    # Add a file uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    txt_btn = st.button("Convert PDF to Plain Text")
    json_btn = st.button("Convert PDF to JSON")
    xml_btn = st.button("Convert PDF to XML")

    if uploaded_file is not None:
        pdf_file_path = uploaded_file # Replace with your PDF file path
        creation_software = get_pdf_creation_software(pdf_file_path)
        print(f"The PDF was created with: {creation_software}")
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        pdf_doc = fitz.open(temp_file_path)
        # Check if PDF document is not empty
        if pdf_doc.page_count > 0:
            # Select page
            page_number = st.number_input("Enter page number", value=1, min_value=1, max_value=len(pdf_doc), step=1)

            # Display PDF
            page = pdf_doc.load_page(page_number - 1)
            pixmap = page.get_pixmap()
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            #st.image(img_bytes, use_column_width=True)

            # Create drawing canvas for selecting area
            drawing_area = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=5,
                drawing_mode="rect",
                height=pixmap.height,
                width=pixmap.width,
                background_image=img,
                key="drawing_canvas"
            )

            # Optional: Save selected area
            if st.button("Save Selected Area"):
                # Get drawn shapes
                drawn_shapes = drawing_area.json_data["objects"]

                # Find the rectangle drawn by the user
                selected_rectangle = None
                for shape in drawn_shapes:
                    if shape["type"] == "rect":
                        selected_rectangle = shape
                        break

                if selected_rectangle:
                    # Get coordinates of the selected rectangle
                    x0 = selected_rectangle["left"]
                    y0 = selected_rectangle["top"]
                    x1 = selected_rectangle["left"] + selected_rectangle["width"]
                    y1 = selected_rectangle["top"] + selected_rectangle["height"]

                    # Crop selected area from the PDF image
                    selected_area_img = img.crop((x0, y0, x1, y1))

                    # Save selected area as a separate image
                    st.image(selected_area_img, caption="Selected Area", use_column_width=True)
                    st.write("Selected area saved.")
                else:
                    st.write("No rectangle drawn. Please draw a rectangle to select an area.")

    # Check if the button is clicked
    if txt_btn:
        if uploaded_file is not None:
            # Display the extracted text
            st.subheader("PDF Text")
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.text(extracted_text)

    if json_btn:
        json_structure = convert_pdf_to_json(uploaded_file)
        st.subheader("PDF JSON Structure")
        st.json(json_structure)

    if xml_btn:
        xml_content = convert_pdf_to_xml(uploaded_file)
        st.subheader("PDF XML Structure")
        st.text_area("XML Content", xml_content, height=400)


if __name__ == "__main__":
    main()
