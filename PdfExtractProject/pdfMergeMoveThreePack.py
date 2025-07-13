# Import necessary libraries
import os
from datetime import datetime
from datetime import datetime, timedelta
import shutil
import random
import string
import fitz  # PyMuPDF
import PyPDF2
from PyPDF2 import PdfMerger
from reportlab.pdfgen import canvas
from PIL import Image
import io
import logging
from PyPDF2 import PdfMerger, PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from errormessagehandler import error_mail

# Constants
merge_folder_name = 'merge'
merge_folder = None  
destination_date_folder_path = None  

# Define the main function to copy and process files
def move_and_process_files(source_path, destination_path):
    #setup logging function
    setup_logging()
    
    # Create folder
    create_folder(source_path, destination_path)
    log_message("Create folder in destination_path")

    # Rename files in folders by removing specified prefixes
    rename_files_in_folders(source_path, prefix_to_remove)
    log_message("Change file name in source_path")

    # Move folders and files from source to destination
    move_all_folders_and_files(source_path, destination_path)
    log_message("All folders and files moved from source_path to destination_path")

    # Process files in the destination path by merging PDFs
    merge_pdfs_in_subfolders(destination_path)
    log_message("PDF merging completed successfully.")

    # Delete all folders and files from destination (Skip Merge Folder)
    clear_folders_and_delete_files(destination_path)
    log_message("Destination folders and files cleared successfully.")
    log_message("\n-------------------------------------------------------------------------------\n")

def setup_logging():
    # Specify the folder where log files will be stored
    log_folder = os.path.join('C:\\Users\\abhij\\Desktop\\distination', 'Log')

    # Check if the log folder exists, and create it if it doesn't
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Define the log file name based on the current date
    log_filename = os.path.join(log_folder, datetime.now().strftime("%Y%m%d.log"))

    # Configure the logging settings
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='Code 2 - %(levelname)s - %(message)s')

def log_message(message):
    # Log an informational message
    logging.info(message)

def log_error(error_message):
    # Log an error message
    logging.error(error_message)
    error_mail(error_message)

# Function to rename files in folders based on specified prefixes
def rename_files_in_folders(root_folder, prefixes_to_remove=None):
    # Traverse through the root folder and its subdirectories
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            for prefix_to_remove in prefixes_to_remove:
                if file.startswith(prefix_to_remove):
                    old_path = os.path.join(root, file)

                    # Modify the filename by removing or replacing the prefix
                    file_name, ext = os.path.splitext(file)
                    random_string = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 8)))
                    new_filename = f'{random_string}{ext}'
                    new_path = os.path.join(root, new_filename)

                    # Rename or move the file
                    try:
                        os.rename(old_path, new_path)
                        log_message(f"Renamed: {old_path} -> {new_path}")
                    except Exception as e:
                        log_error(f"Error renaming {old_path}: {e}")

# Function to move folders and files from source to destination
def move_all_folders_and_files(source_folder, destination_folder):
    # Iterate through all items in the source folder
    for item in os.listdir(source_folder):
        source_item_path = os.path.join(source_folder, item)
        destination_item_path = os.path.join(destination_folder, item)

        # Move the item to the destination folder
        try:
            # If the item already exists in the destination folder, replace it
            if os.path.exists(destination_item_path):
                if os.path.isdir(destination_item_path):
                    shutil.rmtree(destination_item_path)  # Replace folder
                else:
                    os.remove(destination_item_path)  # Replace file
            
            shutil.move(source_item_path, destination_folder)
            log_message(f"Moved '{item}' from {source_folder} to {destination_folder}.")
        except Exception as e:
            log_error(f"Error moving '{item}': {e}")

# Function to clear folders and delete files in the destination folder
def clear_folders_and_delete_files(destination_folder):
    for item in os.listdir(destination_folder):
        item_path = os.path.join(destination_folder, item)
        if os.path.isdir(item_path) and item != merge_folder_name:
            for date_folder in os.listdir(os.path.join(destination_folder, merge_folder_name)):
                date_folder_path = os.path.join(destination_folder, merge_folder_name, date_folder)
                for pdf_file in os.listdir(date_folder_path):
                    pdf_file_path = os.path.join(date_folder_path, pdf_file)
                    if os.path.isdir(pdf_file_path):
                        continue  # Skip subdirectories, we only want PDF files
                    if match_and_delete_files(item, pdf_file, destination_folder, os.path.join(pdf_file_path, f'{pdf_file}')):
                        log_message(f"Deleted destination folder: {item}")

# Function to match merged PDF to subdirectory folder name and delete folder files
def match_and_delete_files(destination_folder_name, pdf_file_name, destination_folder_path, merged_file_path):
    merged_file_base_name = os.path.splitext(os.path.basename(merged_file_path))[0]
    destination_folder_path_to_delete = os.path.join(destination_folder_path, destination_folder_name)

    if destination_folder_name == merged_file_base_name and os.path.exists(destination_folder_path_to_delete):
        shutil.rmtree(destination_folder_path_to_delete)
        return True
    else:
        #print(f"Merged PDF '{merged_file_base_name}.pdf' does not match destination folder '{destination_folder_name}'. Skipping folder deletion.")
        return False

# Function to merge PDFs in subfolders of the provided root folder
def merge_pdfs_in_subfolders(root_folder):
    global sub_dir_path

    # Check if the provided root folder exists and is a directory
    if os.path.exists(root_folder) and os.path.isdir(root_folder):

        # Traverse through the root folder and its subdirectories
        for root, dirs, files in os.walk(root_folder):
            for sub_dir in dirs:
                sub_dir_path = os.path.join(root, sub_dir)
                try:
                # Check if the subdirectory is not 'merge' and doesn't have a date-month-year format
                    if (sub_dir != os.path.basename(merge_folder) and
                            not any(part.isdigit() for part in os.path.basename(sub_dir_path).replace('-', '').split())):

                        # Find all PDF files in the subdirectory
                        pdf_files = [f for f in os.listdir(sub_dir_path) if f.endswith('.pdf')]

                        # Find all JPG or PNG files in the subdirectory
                        image_files = [f for f in os.listdir(sub_dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

                        # If no PDF or image files found in the subdirectory
                        if len(pdf_files) == 0 and len(image_files) == 0:
                            log_message("No PDF or image files found in the directory. Please select a directory containing PDF or image files.")

                        # If only one PDF file found in the subdirectory
                        elif len(pdf_files) == 1:
                            log_message("Only one PDF file found. No merge performed.")

                            # Rename and copy the PDF file to match subfolder name
                            first_pdf = os.path.join(sub_dir_path, pdf_files[0])
                            pdf_path = os.path.join(destination_date_folder_path, f'{sub_dir}.pdf')
                            shutil.copy(first_pdf, pdf_path)
                            new_first_pdf = os.path.join(destination_date_folder_path, f'{sub_dir}.pdf')
                            os.rename(pdf_path, new_first_pdf)

                        # Attempt to merge PDFs using different packages
                        elif len(pdf_files) > 1:
                            merged_file_path = attempt_merge_pdf_files(pdf_files, sub_dir, sub_dir_path)

                            if merged_file_path:
                                # Move merged PDF to date-month-year folder
                                new_file_path = os.path.join(destination_date_folder_path, f'{sub_dir}.pdf')
                                os.replace(merged_file_path, new_file_path)

                                # Display a message showing the number of PDF files merged and the file path
                                log_message(f"{len(pdf_files)} PDF files merged into {new_file_path}.")
                            else:
                                log_message("Failed to merge PDFs. Skipping.")

                        # Convert JPG or PNG files to PDF and merge with existing PDFs
                        if image_files:
                            convert_images_and_merge(image_files, sub_dir, destination_date_folder_path)
                except Exception as ex:
                    log_error(f"Error processing subdirectory {sub_dir}: {ex}")
    else:
        # If the provided directory path is invalid
        log_message("Invalid directory path.")

# Attempt to merge PDF files using different packages
def attempt_merge_pdf_files(pdf_files, sub_dir, sub_dir_path):
    merged_file_path = None

    try:
        if merge_pdfs_with_pypdf2(pdf_files, sub_dir, sub_dir_path):
            merged_file_path = os.path.join(sub_dir_path, f'{sub_dir}_merged_pypdf2.pdf')
        elif merge_pdfs_with_reportlab(pdf_files, sub_dir, sub_dir_path):
            merged_file_path = os.path.join(sub_dir_path, f'{sub_dir}_merged_reportlab.pdf')
        elif merge_pdfs_with_pymupdf(pdf_files, sub_dir, sub_dir_path):
            merged_file_path = os.path.join(sub_dir_path, f'{sub_dir}_merged_pymupdf.pdf')
        

        return merged_file_path

    except Exception as e:
        log_error(f"Error during PDF merging attempt: {e}")
        return None
    
# Function to merge PDFs using PyPDF2
def merge_pdfs_with_pypdf2(pdf_files, sub_dir, sub_dir_path):
    # Initialize a PdfMerger object
    merger = PyPDF2.PdfMerger()

    # Loop through each PDF file in the subdirectory
    for file in pdf_files:
        try:
            merger.append(os.path.join(sub_dir_path, file))
        except Exception as e:
            log_error(f"Error appending PDF file {file} to the merger: {e}")
            continue  # Skip to the next file in case of an error

    # Check if there are no valid PDF files to merge
    if not merger.pages:
        log_message(f"No valid PDF files to merge for {sub_dir}")
        return None

    # Define the path for the merged PDF file
    merged_file_path = os.path.join(sub_dir_path, f'{sub_dir}_merged_pypdf2.pdf')

    try:
        # Write the merged PDF file and close the PdfMerger
        merger.write(merged_file_path)
    except Exception as e:
        log_error(f"Error writing merged PDF file: {e}")
        merged_file_path = None
    finally:
        merger.close()

    if merged_file_path:
        log_message(f'{sub_dir}_merged_pypdf2.pdf')
    return merged_file_path

# Function to merge PDFs using PyMuPDF (fitz)
def merge_pdfs_with_pymupdf(pdf_files, sub_dir, sub_dir_path):
    # Initialize a PDF document
    pdf_document = fitz.open()

    # Loop through each PDF file in the subdirectory
    for file in pdf_files:
        try:
            pdf_document.insert_pdf(fitz.open(os.path.join(sub_dir_path, file)))
        except fitz.errors.DocumentError as e:
            log_error(f"Error inserting PDF file {file} into the document: {e}")
        except Exception as e:
            log_error(f"Unexpected error inserting PDF file {file} into the document: {e}")

    # Define the path for the merged PDF file
    merged_file_path = os.path.join(sub_dir_path, f'{sub_dir}_merged_pymupdf.pdf')

    try:
        # Write the merged PDF file and close the PDF document
        pdf_document.save(merged_file_path)
    except Exception as e:
        log_error(f"Error saving merged PDF file: {e}")
        merged_file_path = None
    finally:
        pdf_document.close()

    log_message(f'{sub_dir}_merged_pymupdf.pdf')
    return merged_file_path

# Function to merge PDFs using ReportLab
def merge_pdfs_with_reportlab(pdf_files, sub_dir, sub_dir_path):
    # Initialize the output PDF writer
    output = PdfWriter()

    # Loop through each PDF file in the subdirectory
    for file in pdf_files:
        try:
            # Read the existing PDF
            existing_pdf = PdfReader(os.path.join(sub_dir_path, file))

            # Merge the existing PDF with the output PDF
            for page in existing_pdf.pages:
                output.add_page(page)
        except Exception as e:
            log_error(f"Error merging PDF file {file}: {e}")
            continue  # Skip to the next file in case of an error

    # Check if there are no valid PDF files to merge
    if not output.pages:
        log_message(f"No valid PDF files to merge for {sub_dir}")
        return None

    # Define the path for the merged PDF file
    merged_file_path = os.path.join(sub_dir_path, f'{sub_dir}_merged_reportlab.pdf')

    try:
        # Write the merged PDF file and close the PdfWriter
        with open(merged_file_path, 'wb') as merged_file:
            output.write(merged_file)
    except Exception as e:
        log_error(f"Error writing merged PDF file: {e}")
        merged_file_path = None

    if merged_file_path:
        log_message(f'{sub_dir}_merged_reportlab.pdf')
    return merged_file_path


# Function to Create folder
def create_folder(source_folder, destination_folder):
    global merge_folder , destination_date_folder_path
    for item_name in os.listdir(source_folder):
        source_item_path = os.path.join(source_folder, item_name)
        
        # Create 'merge' folder in the root folder
        merge_folder = os.path.join(destination_folder, 'merge')
        if not os.path.exists(merge_folder):
            os.makedirs(merge_folder)
        # Check if the item is a directory
        if os.path.isdir(source_item_path) or os.path.isfile(source_item_path):
            # Get the modified date of the item
            modified_date = get_item_modified_date(source_item_path)

            if modified_date:
                # Create a folder based on the modified date in the destination path
                destination_date_folder_name = modified_date.strftime('%Y-%m-%d')
                destination_date_folder_path = os.path.join(merge_folder, destination_date_folder_name)
                
                # Ensure the date folder exists or create it in the destination path
                if not os.path.exists(destination_date_folder_path):
                    os.makedirs(destination_date_folder_path)
                    log_message(f"Created folder '{destination_date_folder_path}'.")

# Function to get the modified date of a folder or file
def get_item_modified_date(item_path):
    try:
        # # Get the last modified time in seconds since the epoch
        # mtime = os.path.getmtime(item_path)

        # # Convert the timestamp to a datetime object
        # modified_date = datetime.fromtimestamp(mtime)
        # Get yesterday's date
        yesterday_date = datetime.now() - timedelta(days=1)

        return yesterday_date
    except OSError as e:
        log_error(f"Error getting modified date for {item_path}: {e}")
        return None

# Function to convert images to PDF and merge with existing PDFs
def convert_images_and_merge(image_files, sub_dir, date_folder_path):
    # Initialize a PdfMerger object
    merger = PdfMerger()

    # Loop through each image file in the subdirectory
    for file in image_files:
        image_path = os.path.join(sub_dir_path, file)

        # Convert image to PDF using reportlab and append to the PdfMerger
        pdf_data = convert_image_to_pdf(image_path)
        merger.append(pdf_data)

    # Define the path for the merged PDF file
    merged_file_path = os.path.join(sub_dir_path, f'{sub_dir}.pdf')

    # Write the merged PDF file and close the PdfMerger
    merger.write(merged_file_path)
    merger.close()

    # Move merged PDF to date-month-year folder
    new_file_path = os.path.join(date_folder_path, f'{sub_dir}.pdf')
    os.replace(merged_file_path, new_file_path)

    # Display a message showing the number of image files converted and the file path
    log_message(f"{len(image_files)} image files converted and merged into {new_file_path}.")

# Function to convert an image to PDF using reportlab
def convert_image_to_pdf(image_path):
    # Create a PDF document
    pdf_buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer)

    # Open the image using PIL
    img = Image.open(image_path)

    # Set the size of the PDF document to match the image
    pdf_canvas.setPageSize((img.width, img.height))

    # Draw the image onto the PDF using drawInlineImage to maintain original resolution
    pdf_canvas.drawInlineImage(img, 0, 0, width=img.width, height=img.height)

    # Close the PDF canvas
    pdf_canvas.showPage()
    pdf_canvas.save()

    # Reset the buffer position and return the PDF content
    pdf_buffer.seek(0)
    return pdf_buffer

# Example usage:
source_path = r"F:\dfs\Department\Accounting\AcctfinAdmins\CodeChanges_DevTest\Prophix - Voucher Image\PDFMerger\Sample\source"
destination_path = r"C:\Users\abhij\Desktop\distination"


prefix_to_remove = ['_ADDITIONAL_DOCUMENT_File_', '__ADDITIONAL_DOCUMENT__File_']

# Call the main function
move_and_process_files(source_path, destination_path)