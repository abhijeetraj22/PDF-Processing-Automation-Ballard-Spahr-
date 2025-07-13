# 📁 PdfExtractProject

A complete automation system for extracting, processing, renaming, merging, and managing accounting-related PDF files based on voucher records from SQL Server. The project includes logging, email alerts, error handling, scheduled execution, and integration with Microsoft Outlook and Credential Manager.

---

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
* Scheduled script can be set up in Task Scheduler for daily unattended execution

### 📂 Logging

* Generates logs daily in `distination/Log` folder
* Differentiates logs with codes (e.g., `Code 1`, `Code 2`, etc.) for tracing script components

### 📊 Database Integration

* Connects to Microsoft SQL Server using `pyodbc`
* Fetches:

  * `VoucherID`, `VchrIndex`, `PostDate` from `Voucher`
  * `DisplayName` from `Timekeeper` using `TKID` found in PDF

---

## 📂 Folder Structure

```
PdfExtractProject/
├── checkmailcrednew3.py             # Stores email credentials securely
├── email_sender_new.py             # Sends summary email via Outlook
├── errormessagehandlernew2.py      # Logs & sends error mail alerts
├── folderCopySql.py                # Copies voucher folders based on SQL PostDate
├── newPDFrenamewithSQL22.py        # Renames PDFs using DB voucher info
├── onlyBatchfile.py                # Generates a batch file to run scripts silently
├── pdfMergeMoveThreePack.py        # Merges PDFs/images, applies cleanup
├── renameFile2.py                  # Renames files using sanitized logic
├── scheduleWithoutExeFile4.py      # Scheduler script runner (pythonw)
├── startupShortcut22.py            # Creates desktop/startup shortcut for automation
```

---

## 🚀 Technologies Used

| Component     | Tech                              |
| ------------- | --------------------------------- |
| Language      | Python 3.x                        |
| PDF Libraries | PyPDF2, fitz (PyMuPDF), ReportLab |
| DB Access     | pyodbc                            |
| Logging       | logging module                    |
| Email         | win32com, smtplib, MIME, creds    |
| Scheduling    | pythonw + batch + Task Scheduler  |
| File Handling | shutil, os, datetime              |

---

## 🚮 Error Handling & Notification

* All scripts call `log_error()` which:

  * Logs to file
  * Sends error email via `error_mail()` from `errormessagehandlernew2.py`
* Email credentials stored securely using Windows Credential Manager (`checkmailcrednew3.py`)

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

1. Configure database strings, paths, and email addresses in scripts.
2. Run in sequence:

```bash
python folderCopySql.py
python pdfMergeMoveThreePack.py
python renameFile2.py
python newPDFrenamewithSQL22.py
python email_sender_new.py
```

3. (Optional) Auto-run setup:

```bash
python onlyBatchfile.py
python scheduleWithoutExeFile4.py
```

---

## 🔗 GitHub Repository

> Folder: `PdfExtractProject`

---

> ⚡ Built by Abhijeet Raj to streamline PDF and document automation for financial workflows.
