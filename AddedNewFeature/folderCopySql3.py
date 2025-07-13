# Import necessary libraries
import pyodbc
import shutil
import os
import logging
from datetime import datetime, timedelta
#from errormessagehandler import error_mail

def setup_logging():
    # Specify the folder where log files will be stored
    log_folder = os.path.join('C:\\Users\\abhij\\Desktop\\distination', 'Log')

    # Check if the log folder exists, and create it if it doesn't
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Define the log file name based on the current date
    log_filename = os.path.join(log_folder, datetime.now().strftime("%Y%m%d.log"))

    # Configure the logging settings
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(levelname)s - %(message)s')

def log_message(message):
    # Log an informational message
    logging.info(message)

def log_error(error_message):
    # Log an error message
    logging.error(error_message)
    #error_mail(error_message)

def copy_files_and_folders(yesterday_date):
    setup_logging()
    print('---->',yesterday_date)
    # Database connection parameters
    server = 'DESKTOP-GR6FEMK\\SQLEXPRESS'
    database = 'TE_3E_PROD'
    trusted_connection = 'yes'  # Use Windows Authentication
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

    # Connect to the database
    try:
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        log_message("Connected to the database")

        # SQL query to get folder and file paths from SQL source based on the date column
        sql_query = f"""
        SELECT VoucherID
        FROM Voucher
        WHERE PostDate = '{yesterday_date}'
        """
        cursor.execute(sql_query)

        # Fetch the results
        results = cursor.fetchall()

        # Specify the source and destination base directories on the source
        source_directory = r'F:\dfs\Department\Accounting\AcctfinAdmins\CodeChanges_DevTest\Prophix - Voucher Image\PDFMerger\FolderName'
        destination_directory = r'F:\dfs\Department\Accounting\AcctfinAdmins\CodeChanges_DevTest\Prophix - Voucher Image\PDFMerger\Sample\source'

        # Loop through the results and copy each file or folder with its contents
        for row in results:
            source_relative_path = row.VoucherID
            source_path = os.path.join(source_directory, source_relative_path)
            destination_path = os.path.join(destination_directory, source_relative_path)

            # Ensure the destination directory exists
            os.makedirs(destination_path, exist_ok=True)

            try:
                # Check if the destination folder already exists
                if os.path.exists(destination_path):
                    # Merge the contents of the source folder with the existing destination folder
                    for item in os.listdir(source_path):
                        source_item = os.path.join(source_path, item)
                        destination_item = os.path.join(destination_path, item)
                        shutil.copy2(source_item, destination_item)
                        log_message(f"Copied: {source_item} -> {destination_item}")
                else:
                    # Use shutil.copytree for both folders and files
                    shutil.copytree(source_path, destination_path)
                    log_message(f"Copied: {source_path} -> {destination_path}")
            except Exception as copy_error:
                log_error(f"Error copying {source_path}: {copy_error}")

    except Exception as e:
        log_error(f"Error: {str(e)}")
    finally:
        # Close the database connection
        if connection:
            connection.close()
            log_message("Connection closed.")
            log_message("\n----------------------------------Code 1---------------------------------------------\n")

if __name__ == "__main__":
    #setup_logging()
    # Get yesterday's date
    yesterday_date = (datetime.now() - timedelta(days=1)).date()
    
    copy_files_and_folders(yesterday_date)
