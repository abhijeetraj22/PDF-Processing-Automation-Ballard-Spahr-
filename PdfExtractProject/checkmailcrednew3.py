import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import win32com.client
import pythoncom

def send_email(subject, body, recipients):
    try:
        # Initialize the COM library
        pythoncom.CoInitialize()

        # Join the recipients into a comma-separated string
        recipient_email = ', '.join(recipients)

        # Create the MIMEText object
        message = MIMEMultipart()
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, 'plain'))

        # Create Outlook application
        outlook_app = win32com.client.Dispatch("Outlook.Application")

        # Create a new mail item
        mail_item = outlook_app.CreateItem(0)
        mail_item.Subject = subject
        mail_item.Body = body
        mail_item.To = recipient_email

        # Send the email
        mail_item.Send()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        # Uninitialize the COM library to release resources
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    subject = "Test Subject"
    body = "This is a test email body.\n"
    body += "This is another line in the body.\n"
    body += "You can add more lines as needed."
    
    recipients = ["abhijeetraj22@gmail.com", "recipient2@example.com", "recipient3@example.com"]

    send_email(subject, body, recipients)
