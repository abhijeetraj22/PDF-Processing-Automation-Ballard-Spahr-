import os
import ctypes
import sys

# Function to check if the script is running with administrative privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to create a batch file to run Python code in the background
def create_batch_file():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Create batch script content to run Python code in the background
    batch_script_content = f'@echo off\nstart /B pythonw.exe "{script_dir}\\3schedule.py"'
    batch_script_path = os.path.join(script_dir, "run_python_code22.bat")

    # Write the batch script to a file
    with open(batch_script_path, "w") as batch_script:
        batch_script.write(batch_script_content)

    # Print a message indicating the successful creation of the batch file
    print(f"Batch file created at {batch_script_path}")

if __name__ == "__main__":
    # Check if the script is run with administrative privileges
    if is_admin():
        # If yes, create the batch file
        create_batch_file()
    else:
        # If not, run the script with administrative privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
