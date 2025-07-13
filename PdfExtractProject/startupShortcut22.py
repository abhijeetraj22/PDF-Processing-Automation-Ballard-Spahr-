import os
import ctypes
import subprocess
import sys

# Function to check if the script is running with administrative privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to create a shortcut in the Startup folder
def create_startup_shortcut():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Create batch script content to run Python code in the background
    batch_script_content = f'@echo off\nstart /B pythonw.exe "{script_dir}\\schedule2Tasks.py"'
    batch_script_path = os.path.join(script_dir, "run_python_code22.bat")

    # Write the batch script to a file
    with open(batch_script_path, "w") as batch_script:
        batch_script.write(batch_script_content)

    # Define the path to the Startup folder
    startup_folder = os.path.join(os.path.expanduser("~"), "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    
    # Define the path for the shortcut in the Startup folder
    shortcut_path = os.path.join(startup_folder, "schedule2Tasks.lnk")

    # Create VBScript content to create a shortcut
    vbs_script_content = f'''
    set ws=createobject("wscript.shell")
    set shortcut = ws.CreateShortcut("{shortcut_path}")
    shortcut.TargetPath = "{batch_script_path}"
    shortcut.Save
    '''

    vbs_script_path = os.path.join(script_dir, "create_shortcut.vbs")

    # Write the VBScript content to a file
    with open(vbs_script_path, "w") as vbs_file:
        vbs_file.write(vbs_script_content)

    # Execute the VBScript to create the shortcut silently
    subprocess.Popen(['wscript.exe', vbs_script_path], creationflags=subprocess.CREATE_NO_WINDOW)

    # Print a message indicating the successful creation of the shortcut
    print(f"Shortcut created at {shortcut_path}")

if __name__ == "__main__":
    # Check if the script is run with administrative privileges
    if is_admin():
        # If yes, create the startup shortcut
        create_startup_shortcut()
    else:
        # If not, run the script with administrative privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
