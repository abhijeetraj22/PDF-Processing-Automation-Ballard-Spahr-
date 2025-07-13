import win32cred

def store_credentials(target_name, username, password):
    try:
        # Store credentials
        win32cred.CredWrite({
            'TargetName': target_name,
            'Type': win32cred.CRED_TYPE_GENERIC,
            'UserName': username,
            'CredentialBlob': password,
            'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE  # Adjust as needed
        })

        print("Credentials successfully stored.")
    except Exception as e:
        print(f"Error storing credentials: {e}")
        print(e.args)       
        
if __name__ == "__main__":
    target_name = 'pythonCode'
    username = 'abhijeetraj22@outlook.com'
    password = 'Raj@2209'

    store_credentials(target_name, username, password)




