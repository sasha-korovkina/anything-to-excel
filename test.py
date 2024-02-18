import PyPDF2
import os

pdf_file_path = "M:\\CDB\\Analyst\\Rhys\\Data\\(New) Goldman Sachs ND CMi2i responses (Germany).pdf"
directory_path = "M:\\CDB\\Analyst\\Rhys\\Data\\"
processed_files = 0  # Initialize counter

# Loop through the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".pdf") and processed_files < 5:  # Check if the file is a PDF and counter is less than 5
        pdf_file_path = os.path.join(directory_path, filename)
        print(f"Processing {pdf_file_path}...")

        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            metadata = pdf_reader.metadata

        # Access and print the /Producer parameter from metadata
        producer = metadata.get('/Producer', 'Producer not found')
        print(f"Producer: {producer}\n")

        processed_files += 1  # Increment the counter
    elif processed_files >= 5:
        break  # Exit loop after processing 5 files
