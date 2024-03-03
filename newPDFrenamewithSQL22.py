import PyPDF2
import re
import pyodbc
import os
import shutil

# Function to connect to Microsoft SQL Server and retrieve DisplayName for a given TKID
def get_display_name(tkid):
    # Connection parameters
    server = 'DESKTOP-GR6FEMK\\SQLEXPRESS'  # Replace with your SQL Server instance name or IP address
    database = 'TE_3E_Prod'
    # Create a connection string using ODBC Driver 17 for SQL Server
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    # Connect to the SQL Server database
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    
    # SQL query to retrieve the DisplayName from the timekeeper table for the given TKID
    query = f"SELECT DisplayName FROM timekeeper WHERE Numer = ?"
    # Execute the query with the provided TKID
    cursor.execute(query, tkid)
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the database connection
    connection.close()
    
    # If result is found, return the DisplayName, otherwise return None
    if result:
        return result[0]
    else:
        return None

# Function to extract TKID and rename PDF files
def extract_tkid_and_rename_pdf(pdf_file_path, output_directory):
    # Regular expression pattern to match TKID in the PDF content
    tkid_pattern = re.compile(r'TKID:\s*(\d+)', re.IGNORECASE)

    with open(pdf_file_path, 'rb') as file:
        # Create a PdfReader object to read the PDF file
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from PDF content
        page_text = ""
        for page in pdf_reader.pages:
            page_text += page.extract_text()
        
        # Search for TKID in the extracted text
        tkid_match = tkid_pattern.search(page_text)
        
        # If TKID is found
        if tkid_match:
            tkid = tkid_match.group(1)  # Extract TKID from the match
            
            # Fetch DisplayName from the database using TKID
            display_name = get_display_name(tkid)
            
            # If DisplayName is found
            if display_name:
                # Generate new file name
                new_file_name = f"PartnerContribution_{tkid}_{display_name}.pdf"
                # Specify the output file path
                output_file_path = os.path.join(output_directory, new_file_name)
                
                try:
                    # Copy the original PDF file to the output directory with the new name
                    shutil.copy2(pdf_file_path, output_file_path)
                    print(f"Renamed and saved {pdf_file_path} to {output_file_path}")
                except PermissionError:
                    print(f"Error: Could not rename {pdf_file_path} due to permission error.")
            else:
                print(f"No DisplayName found for TKID: {tkid}")

# Replace 'pdf_files_directory' with the directory containing your PDF files
pdf_files_directory = 'E:/SQL ASSIGNMENT/python file/destination'
output_directory = 'E:/SQL ASSIGNMENT/python file/destination/Log'

# Iterate through the PDF files in the input directory
for file_name in os.listdir(pdf_files_directory):
    if file_name.endswith('.pdf'):  # Check if the file is a PDF file
        file_path = os.path.join(pdf_files_directory, file_name)  # Get the full path of the PDF file
        # Extract TKID and rename the PDF file, then save to the output directory
        extract_tkid_and_rename_pdf(file_path, output_directory)
