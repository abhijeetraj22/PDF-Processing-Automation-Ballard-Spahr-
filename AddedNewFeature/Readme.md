# 📁 Added New Feature

This folder contains advanced automation scripts for PDF processing, file management, database interaction, and secure credential storage. These scripts were developed to support high-volume accounting workflows, specifically targeting voucher image management, secure file handling, metadata extraction, and PDF enhancement operations in enterprise environments.

---

## 📌 Project Objective

Automate the full pipeline of:

* Copying accounting files and folders from source to destination.
* Merging and renaming PDFs based on SQL voucher metadata.
* Extracting invoice identifiers (Proforma Index) using OCR and text parsing.
* Cleaning up old PDF files.
* Logging and exception handling.
* Securely managing credentials for future authentication extensions.

---

## 🛠️ Technologies Used

* **Python 3.x**
* **Libraries**:

  * `os`, `shutil`, `logging`, `datetime`, `re`
  * `pyodbc` (SQL Server connection)
  * `PyPDF2`, `fitz` (PyMuPDF), `pdf2image`, `PIL`, `reportlab`
  * `pytesseract` (OCR)
  * `win32cred` (Windows Credential Manager)

---

## 📂 Folder Structure (Key Files)

```
AddedNewFeature/
├── folderCopySql3.py              # Step 1: Copy folders/files based on SQL voucher IDs
├── pdfMergeMoveThreePack33.py     # Step 2: Merge PDF/image files from destination, cleanup originals
├── newRenameFile3.py              # Step 3: Rename merged PDFs based on Voucher Index from SQL DB
├── pdfAllOperationTwoyear.py      # Orchestrator script: Runs all 3 scripts for a 2-year date range
├── img_pdf_read32.py              # Extracts 'Proforma Index' from PDF using text and OCR
├── controlPanelStoreCred.py       # Stores credentials securely using Windows Credential Manager
```

---

## 🔄 Process Workflow

### 🧩 Step 1: `folderCopySql3.py`

* Fetches Voucher IDs from SQL where `PostDate = yesterday`
* Copies folders/files from a structured `source_directory`
* Merges contents into destination `Sample/source/`
* Logs all actions to a timestamped log file

### 📑 Step 2: `pdfMergeMoveThreePack33.py`

* Renames source files to random string
* Moves folders/files into destination path
* Merges:

  * Multiple PDFs (via PyPDF2, ReportLab, or PyMuPDF)
  * JPG/PNG images (converted using ReportLab)
* Merged files are saved in `/merge/yyyy-mm-dd/`
* Deletes matched subfolders after successful merge

### 📝 Step 3: `newRenameFile3.py`

* Queries Voucher Table for `PostDate = yesterday`
* Renames PDFs in `/merge/yyyy-mm-dd/` using `VchrIndex`
* Final PDFs saved to `/allMergePdf/`
* Removes empty folders

### 🧠 `img_pdf_read32.py`

* Scans PDFs for `Proforma Index` using:

  * Regex extraction from text (via PyPDF2)
  * OCR fallback via Tesseract if needed
* Saves results to `ProformaIndex` SQL table

### ⚙️ `pdfAllOperationTwoyear.py`

* Iterates from `2023-04-01` to `2024-04-24`
* Sequentially runs: copy → merge → rename
* Prints and logs success/error for each date

### 🔐 `controlPanelStoreCred.py`

* Saves credentials (`TargetName`, `Username`, `Password`) in Windows Credential Manager
* Can be used for future email or DB authentication

---

## ✅ Features

* SQL-integrated dynamic folder handling
* Robust PDF merge engine (supports multiple libraries)
* Image-to-PDF support
* Logging to daily log files
* Secure password storage (no hardcoding in scripts)
* Batch cleanup of PDFs older than 2 years

---

## 🧪 Sample Execution Flow

```bash
# One-time credential storage (optional)
python store_credentials.py

# Daily use case
python folderCopySql3.py
python pdfMergeMoveThreePack33.py
python newRenameFile3.py

# Full automation over historical range
python runner_for_all_script.py
```

---

## 🔐 Credentials Handling

Stored via `win32cred` and retrieved securely. Avoids plain-text passwords in source files. Useful for Outlook login, SMTP, or secure API calls in future development.

---

## 📊 Database Tables Used

* `Voucher` — contains `VoucherID`, `VchrIndex`, `PostDate`
* `ProformaIndex` — stores extracted Proforma Index and file references

---

## 📎 Future Enhancements

* Email error alerts (currently commented `error_mail()`)
* GUI dashboard or job monitor
* Upload final PDFs to SharePoint or S3 bucket
* Unit tests and CI/CD pipeline

---

## 🧠 Notes

* Real-world implementation with logging, batch processing, and SQL integration.
* Shows ability to work on file systems, OCR, automation pipelines, and exception handling.
* Demonstrates advanced PDF handling and Windows Credential usage.

---


> GitHub Repo: [Added New Feature](https://github.com/abhijeetraj22/PDF-Processing-Automation-Ballard-Spahr-/new/main/AddedNewFeature)

