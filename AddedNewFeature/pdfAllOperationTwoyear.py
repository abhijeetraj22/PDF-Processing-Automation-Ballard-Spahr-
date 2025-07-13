import datetime
#import subprocess
from folderCopySql3 import copy_files_and_folders as folder_copy_process
from pdfMergeMoveThreePack33 import move_and_process_files as pdf_merge_process
from newRenameFile3 import rename_pdfs_based_on_database as rename_file_process

def run_python_script(script_function, date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        script_function(date_obj)
        print(f"Script '{script_function.__name__}' executed successfully for date {date_str}")
    except Exception as e:
        print(f"Error executing script '{script_function.__name__}' for date {date_str}: {e}")


def generate_date_range(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += datetime.timedelta(days=1)
    return dates

if __name__ == "__main__":
    # Define start and end dates for the two-year range
    start_date = datetime.datetime(2023, 4, 1)
    end_date = datetime.datetime(2024, 4, 24)

    # Generate the date range
    date_range = generate_date_range(start_date, end_date)

    # Iterate over the date range and execute each script for each date
    for date in date_range:
        date_str = date.strftime("%Y-%m-%d")
        print('1st')
        run_python_script(folder_copy_process, date_str)
        print('2nd')
        run_python_script(pdf_merge_process, date_str)
        print('3rd')
        run_python_script(rename_file_process, date_str)
