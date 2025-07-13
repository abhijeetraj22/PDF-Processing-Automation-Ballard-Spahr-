import smtplib
import win32cred
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_windows_credentials(target_name):
    try:
        # Attempt to retrieve the stored credentials for the specified target
        creds = win32cred.CredRead(target_name, win32cred.CRED_TYPE_GENERIC, 0)
        username = creds['UserName']
        password = creds['CredentialBlob'].decode('utf-16')
        return username, password
    except Exception as e:
        print(f"Error retrieving credentials: {e}")
        return None, None

def send_email(subject, body):
    try:
        # Replace 'your_target_name' with the name you used when storing the credentials in Credential Manager
        target_name = 'pythonCode'

        # Retrieve Windows credentials
        username, password = get_windows_credentials(target_name)

        if username and password:
            # Your SMTP server and port
            smtp_server = "smtp.office365.com"
            smtp_port = 587  # Update with the appropriate port
            #to_email = "rajabhijeet09@outlook.com"
            to_email = "abhijeetraj22@gmail.com"
            # Create the MIMEText object
            message = MIMEMultipart()
            message['From'] = username
            message['To'] = to_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # Setup the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Authenticate with the retrieved Windows credentials
            server.login(username, password)

            # Send the email
            server.sendmail(username, to_email, message.as_string())

            # Quit the server
            server.quit()
            print("Email sent successfully!")
        else:
            print("Failed to retrieve credentials. Please check the target name.")

    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_email("Test Subject", "This is a test email body.")
