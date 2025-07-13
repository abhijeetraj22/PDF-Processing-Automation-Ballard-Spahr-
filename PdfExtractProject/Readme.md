# PdfExtractProject

A complete automation system for extracting, processing, renaming, merging, and managing accounting-related PDF files based on voucher records from SQL Server. The project includes logging, email alerts, error handling, scheduled execution, and integration with Microsoft Outlook and Credential Manager.

## 🔧 Features

### ✍️ PDF Automation Workflow

* **Voucher-based file copy**: Fetches `VoucherID` from SQL Server and copies related files from the source directory to a local workspace.
* **File renaming**: Cleans up filenames by removing defined prefixes and applies a randomized identifier to prevent name collisions.
* **PDF merging**: Merges multiple PDFs and image files in each folder using multiple fallback libraries:

  * PyPDF2
  * ReportLab
  * PyMuPDF (fitz)
* **Image-to-PDF conversion**: Converts `.jpg`, `.jpeg`, and `.png` images into PDF before merging.

### 🔄 File Management & Cleanup

* Organized folder creation by date
* Skips and retains merged folders during cleanup
* Deletes original folders only if their content is successfully merged

### ✉️ Email Notifications

* Sends a consolidated summary (success or errors) to recipients via Outlook using:

  * `win32com.client` (for corporate Outlook)
  * `smtplib` + `Credential Manager` (optional, secure SMTP-based fallback)

### 📅 Scheduling Support

* Includes script to generate a batch file to silently run the schedule script (`pythonw.exe`)
* Scheduled script (`3schedule.py`) can be set up in Task Scheduler for daily unattended execution

### 📂 Logging

* Generates logs daily in `distination/Log` folder
* Differentiates logs with codes (e.g., `Code 1`, `Code 2`, etc.) for tracing script components

### 📊 Database Integration

* Connects to Microsoft SQL Server using `pyodbc`
* Fetches:

  * `VoucherID`, `VchrIndex`, `PostDate` from `Voucher`
  * `DisplayName` from `Timekeeper` using `TKID` found in PDF

---

## 🌐 Folder Structure

```
PdfExtractProject/
├── copyFilesAndFolders.py            # Copy Voucher folders based on SQL PostDate
├── mergeMoveThreePack.py            # Renames, merges PDFs, cleans up
├── renameBasedOnDB.py               # Renames PDFs using VoucherID & VchrIndex
├── extractTKIDandRename.py          # Extracts TKID from PDFs, renames using Timekeeper
├── createBatch.py                   # Generates a .bat file to run scheduler silently
├── errormessagehandler.py           # Centralized error handler + email alert logic
├── email_outlook_com.py             # Sends email via Outlook
├── email_smtp_creds.py              # Sends email via SMTP using Windows Credential Manager
├── send_summary_email.py            # Reads all shared errors and sends summary on completion
├── shared_errors.txt                # Runtime-shared error collection file
└── README.md                        # This file
```

---

## 🚀 Technologies Used

| Component     | Tech                              |
| ------------- | --------------------------------- |
| Language      | Python 3.x                        |
| PDF Libraries | PyPDF2, fitz (PyMuPDF), ReportLab |
| DB Access     | pyodbc                            |
| Logging       | logging module                    |
| Email         | win32com, smtplib, MIME           |
| Scheduling    | pythonw + batch + Task Scheduler  |
| File Handling | shutil, os, datetime              |

---

## 🚮 Error Handling & Notification

* All scripts call `log_error()` which:

  * Logs to file
  * Appends error to `shared_errors.txt`
  * Sends error email via `error_mail()`
* `send_summary_email.py` reads `shared_errors.txt` at end of execution and sends a summary email

---

## 🎓 Use Cases

* Automating accounting file handling for **Voucher Processing**
* Ensuring no duplication or name collision with randomized renaming
* Scheduled daily execution for **unattended processing**
* Notifying finance or admin users of **success/failure logs**

---

## ✈️ How to Run

### Prerequisites

* Python 3.x
* Outlook (for COM-based email)
* SQL Server ODBC Driver 17
* Dependencies: `pip install -r requirements.txt`

  ```txt
  pyodbc
  PyPDF2
  PyMuPDF
  reportlab
  pillow
  pywin32
  ```

### Execution

1. Configure database connection strings and source/destination paths in each script.
2. Run in sequence:

   ```bash
   python copyFilesAndFolders.py
   python mergeMoveThreePack.py
   python renameBasedOnDB.py
   python extractTKIDandRename.py
   python send_summary_email.py
   ```
3. (Optional) Schedule using `createBatch.py` + Task Scheduler for daily automation

---

## 🚀 Future Enhancements

* Add PDF metadata tagging (voucher info as metadata)
* Web interface for job monitoring
* DB audit table logging instead of just `.log` files

---

## 👉 GitHub Repo

> [PdfExtractProject](https://github.com/abhijeetraj22/PDF-Processing-Automation-Ballard-Spahr-/new/main/PdfExtractProject))
> *Clone, configure, and automate your PDF accounting workflows.*

---

For inquiries, contributions, or deployment help, feel free to contact via

---

> ⚡ Built by Abhijeet Raj to streamline financial document handling in enterprise environments.
