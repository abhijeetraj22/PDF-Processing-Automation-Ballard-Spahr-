# Import necessary libraries
import pyodbc
import os
import shutil
import logging
from datetime import datetime, timedelta
from errormessagehandler import error_mail

def setup_logging():
    # Specify the folder where log files will be stored
    log_folder = os.path.join('C:\\Users\\abhij\\Desktop\\distination', 'Log')

    # Check if the log folder exists, and create it if it doesn't
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Define the log file name based on the current date
    log_filename = os.path.join(log_folder, datetime.now().strftime("%Y%m%d.log"))

    # Configure the logging settings
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='Code 3 - %(levelname)s - %(message)s')

def log_message(message):
    # Log an informational message
    logging.info(message)

def log_error(error_message):
    # Log an error message
    logging.error(error_message)
    error_mail(error_message)


def rename_pdfs_based_on_database():
    # Database connection parameters
    server = 'DESKTOP-GR6FEMK\\SQLEXPRESS'
    database = 'TE_3E_PROD'
    trusted_connection = 'yes'  # Use Windows Authentication
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

    # Connect to the database
    try:
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        log_message("Connected to the database")

        # Get yesterday's date
        yesterday_date = (datetime.now() - timedelta(days=1)).date()

        # SQL query to get distinct VoucherID and VchrIndex from Voucher table for yesterday's date
        sql_query = f"""
        SELECT DISTINCT v.VoucherID, v.VchrIndex
        FROM Voucher v
        WHERE v.PostDate = CAST('{yesterday_date}' AS DATE)
        """
        cursor.execute(sql_query)

        # Fetch the results
        results = cursor.fetchall()

        # Specify the directory where PDF files are located on the virtual machine
        pdf_directory_root = r'C:\Users\abhij\Desktop\distination\merge'

        # Iterate over subdirectories (folders) in the root directory
        for folder_name in os.listdir(pdf_directory_root):
            folder_path = os.path.join(pdf_directory_root, folder_name)

            # Check if the folder name matches yesterday's date
            if os.path.isdir(folder_path) and folder_name == yesterday_date.strftime("%Y-%m-%d"):
                # Loop through all subdirectories and files in the specified directory
                for root, dirs, files in os.walk(folder_path):
                    for filename in files:
                        # Extract the file name without extension
                        file_name, file_extension = os.path.splitext(filename)

                        # Iterate through the database results
                        for row in results:
                            voucher_id = row.VoucherID
                            vchr_index = row.VchrIndex

                            # Perform a case-insensitive check if voucher_id is present in the filename and it's a PDF file
                            if voucher_id.lower() in file_name.lower() and file_extension.lower() == '.pdf':
                                # Build the new file name using only VchrIndex
                                new_filename = f"{vchr_index}{file_extension}"

                                # Print full file paths
                                old_filepath = os.path.join(root, filename)
                                new_filepath = os.path.join(root, new_filename)
                                log_message(f"Renaming: {old_filepath} -> {new_filepath}")

                                # Rename the PDF file using shutil.move
                                try:
                                    shutil.move(old_filepath, new_filepath)
                                    log_message(f"Renamed: {filename} -> {new_filename}")
                                except Exception as move_error:
                                    log_error(f"Error renaming {filename}: {move_error}")

    except Exception as e:
        log_error(f"Error: {str(e)}")
    finally:
        # Close the database connection
        if connection:
            connection.close()
            log_message("Connection closed.")
            log_message("\n-------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    setup_logging()
    rename_pdfs_based_on_database()
