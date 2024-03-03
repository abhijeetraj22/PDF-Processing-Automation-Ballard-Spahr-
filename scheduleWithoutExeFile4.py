import schedule
import threading
import subprocess
import time
import os
from errormessagehandler import error_mail

# Flag to indicate whether all tasks are completed
all_tasks_completed = False

# Function to set up the schedule for running scripts
def set_schedule():
    # Set up the schedule to run the first script every day at 8:00 AM
    schedule.every().day.at("00:08").do(run_script, script_path=script1_path)

# Function to start the scheduler in a separate thread
def start_schedule():
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.start()

# Function to continuously run the schedule and exit when all tasks are completed
def run_schedule():
    while True:
        # Run pending scheduled tasks
        schedule.run_pending()

        # Sleep for 1 second to avoid high CPU usage
        time.sleep(1)

        # If all tasks are completed, set the flag and exit the program
        if all_tasks_completed:
            os._exit(0)

# Function to run a specified script and trigger the second, third, and fourth scripts if applicable
def run_script(script_path):
    try:
        # Run the specified script
        subprocess.run(["python", script_path])

        # If this was the first script, run the second script
        if script_path == script1_path:
            run_second_script(script2_path)

    except subprocess.CalledProcessError as e:
        error_message = f"Error running script: {e}"
        error_mail(error_message)
        

# Function to run the second script and trigger the third script
def run_second_script(script_path):
    try:
        # Run the second script
        subprocess.run(["python", script_path])

        # If this was the second script, run the third script
        if script_path == script2_path:
            run_third_script(script3_path)

    except subprocess.CalledProcessError as e:
        error_message = f"Error running second script: {e}"
        error_mail(error_message)

# Function to run the third script and trigger the fourth script
def run_third_script(script_path):
    try:
        # Run the third script
        subprocess.run(["python", script_path])

        # If this was the third script, run the fourth script
        if script_path == script3_path:
            run_fourth_script(script4_path)

    except subprocess.CalledProcessError as e:
        error_message = f"Error running third script: {e}"
        error_mail(error_message)

# Function to run the fourth script and set the flag to indicate all tasks are completed
def run_fourth_script(script_path):
    global all_tasks_completed
    try:
        # Run the fourth script
        subprocess.run(["python", script_path])

    except subprocess.CalledProcessError as e:
        error_message = f"Error running fourth script: {e}"
        error_mail(error_message)

    # Set the flag to indicate all tasks are completed
    all_tasks_completed = True

if __name__ == "__main__":
    # Define paths for the scripts
    script1_path = os.path.abspath(r"C:\AutoWork\schedule2Tasks\NewWork\folderCopySql.py")
    script2_path = os.path.abspath(r"C:\AutoWork\schedule2Tasks\NewWork\pdfMergeMoveThreePack.py")
    script3_path = os.path.abspath(r"C:\AutoWork\schedule2Tasks\NewWork\renameFile2.py")
    script4_path = os.path.abspath(r"C:\AutoWork\schedule2Tasks\NewWork\errormessagehandlernew2.py")

    # Set up the schedule and start it in a separate thread
    set_schedule()
    start_schedule()

    # Keep the main thread running until all scheduled tasks are completed
    while True:
        time.sleep(1)
