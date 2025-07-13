import PyPDF2
import re
import os
import pyodbc
import warnings
from pdf2image import convert_from_path
import pytesseract

def extract_proforma_indices_from_pdf(pdf_path, pattern):
    # Use a set to store unique entries
    proforma_indices = set()  
    with open(pdf_path, 'rb') as file:
        # Create a PdfReader object to read the PDF file
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        # Iterate over each page in the PDF
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            # Extract text from the page
            text = page.extract_text()
            # Find all matches of the pattern in the extracted text
            matches = re.findall(pattern, text)
            # Iterate over each match found
            for match in matches:
                proforma_index = match
                # Add the match to the set of unique entries
                proforma_indices.add(proforma_index)
    # Convert the set back to a list before returning
    return list(proforma_indices)

def extract_proforma_indices_from_image(pdf_path, patterns):
    # Initialize set to store unique Proforma Index numbers
    proforma_set = set()

    print("Extracting information from PDF...")

    # Convert PDF pages to images
    pages = convert_from_path(pdf_path)

    # Initialize pytesseract OCR engine
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Extract text from each image
    for page in pages:
        # Convert image to grayscale
        grayscale_img = page.convert('L')

        # Perform OCR on the grayscale image
        extracted_text = pytesseract.image_to_string(grayscale_img)

        # Iterate over each pattern and try to find Proforma Index numbers
        for pattern in patterns:
            proforma_matches = re.findall(pattern, extracted_text)
            # Update the set of unique Proforma Index numbers
            proforma_set.update(proforma_matches)

    print("Extraction complete.")

    return list(proforma_set)

def save_proforma_indices_to_db(proforma_indices, pdf_filename):
    try:
        # Database connection parameters
        server = 'DESKTOP-GR6FEMK\\SQLEXPRESS'
        database = 'TE_3E_PROD'
        trusted_connection = 'yes'
        # Construct the connection string
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'
        
        # Connect to the database
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ProformaIndex')
            BEGIN
                CREATE TABLE ProformaIndex (
                    ProformaIndex VARCHAR(255),
                    FileName VARCHAR(255),
                    CONSTRAINT UC_ProformaIndex UNIQUE (ProformaIndex)
                );
            END
        """)

        for proforma_index in proforma_indices:
            # Check if the record already exists in the database
            cursor.execute("SELECT COUNT(*) FROM ProformaIndex WHERE ProformaIndex = ?", (proforma_index,))
            # If the record does not exist
            if cursor.fetchone()[0] == 0:  
                # Insert the record into the database
                cursor.execute("INSERT INTO ProformaIndex (ProformaIndex, FileName) VALUES (?, ?)", (proforma_index, pdf_filename))
                print('Proforma Index =', proforma_index, 'File Name =', pdf_filename)
        # Commit the transaction
        connection.commit()
        print("Proforma indices saved successfully to the database.")
    except Exception as e:
        print(f"Error occurred while saving proforma indices to the database: {str(e)}")
    finally:
        # Close the database connection
        if connection:
            connection.close()

def find_proforma_index_in_directory(directory, pdf_pattern, image_patterns):
    processed_files = set()  # Keep track of processed files
    for filename in os.listdir(directory):
        # Check if the file is a PDF file and not already processed
        if filename.endswith('.pdf') and filename not in processed_files:
            file_path = os.path.join(directory, filename)
            # Find proforma indices in the PDF file
            proforma_indices = extract_proforma_indices_from_pdf(file_path, pdf_pattern)
            # If no Proforma indices found in the PDF, try extracting from images
            if not proforma_indices:
                proforma_indices = extract_proforma_indices_from_image(file_path, image_patterns)
            # Save proforma indices to the database
            save_proforma_indices_to_db(proforma_indices, filename)
            # Add processed file to set
            processed_files.add(filename)

# Suppress PyPDF2 warning about advanced encoding
warnings.filterwarnings("ignore", category=UserWarning, message="Advanced encoding .* not implemented yet")

# Directory path containing the PDF files
directory_path = r'C:\Users\abhij\Desktop\destination\SerachProformaIndex'
# Define regex pattern for PDF and image extraction
pdf_pattern = r'Proforma\s+(\d+)'
image_patterns = [r'Proforma Index:\s+(\d+)', r'(\d+)\s*Invoice No\.']
# Find proforma indices in the PDF files in the directory
find_proforma_index_in_directory(directory_path, pdf_pattern, image_patterns)
