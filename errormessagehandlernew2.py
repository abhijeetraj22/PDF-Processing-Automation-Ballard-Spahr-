import os # Import the send_email function from your email-related script
import logging
import os
from datetime import datetime
import win32com.client
import pythoncom

# Path to the shared errors file
shared_errors_path = os.path.abspath("shared_errors.txt")

# List to collect error messages
error_messages = []

def setup_logging():
    # Specify the folder where log files will be stored
    log_folder = os.path.join('C:\\Users\\abhij\\Desktop\\distination', 'Log')

    # Check if the log folder exists, and create it if it doesn't
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Define the log file name based on the current date
    log_filename = os.path.join(log_folder, datetime.now().strftime("%Y%m%d.log"))

    # Configure the logging settings
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='Code 4 - %(levelname)s - %(message)s')

def log_message(message):
    # Log an informational message
    logging.info(message)

def log_error(error_message):
    # Log an error message
    logging.error(error_message)

def send_email(subject, body):
    try:
        # Initialize the COM library
        pythoncom.CoInitialize()
        recipients = ["abhijeetraj22@gmail.com", "abhijeetrajpryj@gmail.com", "rmysticannu22@gmail.com"]
        # Create Outlook application
        outlook_app = win32com.client.Dispatch("Outlook.Application")

        # Create a new mail item
        mail_item = outlook_app.CreateItem(0)
        mail_item.Subject = subject
        mail_item.Body = body

        # Add recipients using Recipients.Add method
        for recipient in recipients:
            mail_item.Recipients.Add(recipient)

        # Resolve recipients
        mail_item.Recipients.ResolveAll()

        # Send the email
        mail_item.Send()

        log_message("Email sent successfully!")
        print("Email sent successfully!")
    except Exception as e:
        log_error(f"Error sending email: {e}")
        print(f"Error sending email: {e}")
    finally:
        # Uninitialize the COM library to release resources
        pythoncom.CoUninitialize()
        
# Function to add an error message to the list and write to the shared errors file
def error_mail(error_message):
    #error_messages.append(error_message)
    with open(shared_errors_path, 'a') as error_file:
        error_file.write(error_message + '\n')

# Function to send a consolidated email on completion or when errors occur
def send_email_on_completion():
    # Read error messages from the shared file
    with open('shared_errors.txt', 'r') as error_file:
        error_messages = error_file.readlines()
    
    if error_messages:
        subject = "Script Execution Errors"
        body = "\n".join(error_messages)
    else:
        subject = "All Tasks Completed"
        body = "All scheduled tasks have been completed successfully."

    # Send the email using the imported send_email function
    send_email(subject, body)

    # Clear the shared errors file after sending the email
    clear_shared_errors()

# Function to clear the shared errors file
def clear_shared_errors():
    with open(shared_errors_path, 'w') as error_file:
        pass  # This truncates the file, effectively clearing its content

if __name__ == "__main__":
    setup_logging()
    send_email_on_completion()
    