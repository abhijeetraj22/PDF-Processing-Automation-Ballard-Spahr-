# 🧾 PDF Processing & Automation Suite — Ballard Spahr

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![SQL Server](https://img.shields.io/badge/SQL--Server-ODBC--Integrated-brightgreen?logo=microsoftsqlserver)](https://www.microsoft.com/sql-server/)
[![PowerShell](https://img.shields.io/badge/PowerShell-Scripting-blue?logo=powershell)](https://learn.microsoft.com/powershell/)
[![Status](https://img.shields.io/badge/Project-Production--Ready-green)]()
[![Automation](https://img.shields.io/badge/Automation-End--to--End-orange)]()
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

> 🎯 **Real-world enterprise automation** for PDF processing, voucher management, secure token APIs, folder cleanup, database integration, email alerting, and batch scheduling.
> Built to support **accounting teams** with minimal manual intervention.

---

## 📌 Overview

This repository consists of **three production-grade sub-projects** built to automate document workflows for accounting teams, particularly those handling **voucher-based PDF processing**, **secure API integration**, and **folder management**. These scripts support high-volume workloads, secure operations, and minimal manual intervention.

| 📁 Folder                                                       | 🔍 Purpose                                                                                    |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [`PdfExtractProject`](PdfExtractProject)                       | Automates end-to-end voucher-based PDF processing, renaming, merging, and email notifications |
| [`AddedNewFeature`](AddedNewFeature)                           | Extended batch automation with OCR, secure credential storage, and 2-year archival            |
| [`JsonDataExtractionUsingToken`](JsonDataExtractionUsingToken) | Secure API token access, JSON parsing, SQL insert, and PowerShell folder automation           |

---

## 📁 PdfExtractProject

**Daily task automation for voucher-based PDF workflows**

### 🔑 Highlights:

* Copies source files using `VoucherID` and `PostDate` from SQL Server
* Merges and renames PDFs using PyPDF2, ReportLab, or fitz (PyMuPDF)
* Email alerting (Outlook or SMTP)
* Creates scheduled batch execution files
* Generates logs and handles runtime errors with notifications

📘 [Detailed README »](https://github.com/abhijeetraj22/PDF-Processing-Automation-Ballard-Spahr-/tree/main/PdfExtractProject)

---

## 📁 AddedNewFeature

**2-Year automation workflow across large date ranges**

### 🔑 Highlights:

* Full orchestrator for batch processing by date
* Renames files using SQL voucher metadata (`VchrIndex`)
* OCR-based extraction of `Proforma Index` using Tesseract
* Daily logging and secure credential handling via Windows Credential Manager
* Cleanup logic to remove processed/merged folders

📘 [Detailed README »](https://github.com/abhijeetraj22/PDF-Processing-Automation-Ballard-Spahr-/tree/main/AddedNewFeature)

---

## 📁 JsonDataExtractionUsingToken

**Secure API → Flattened JSON → SQL Insertion + Folder Automation**

### 🔑 Highlights:

* Uses client credentials to fetch bearer token via a proxy
* Calls a secured API and parses complex JSON into flat key-value form
* Creates SQL Server table dynamically and inserts rows
* PowerShell scripts to:

  * Create folders using database values
  * Clean/delete files or subfolders as needed

📘 [Detailed README »](https://github.com/abhijeetraj22/PDF-Processing-Automation-Ballard-Spahr-/tree/main/JsonDataExtractionUsingToken)

---

## 🧰 Tech Stack

| Area             | Technologies Used                                            |
| ---------------- | ------------------------------------------------------------ |
| Language         | Python 3.x, PowerShell                                       |
| PDF Libraries    | PyPDF2, fitz (PyMuPDF), ReportLab, Pillow                    |
| OCR              | pytesseract + Tesseract                                      |
| Database         | SQL Server, pyodbc                                           |
| API & Auth       | requests, proxies, bearer tokens, Windows Credential Manager |
| Email            | win32com (Outlook), smtplib, MIME                            |
| Scheduling       | Windows Task Scheduler, `.bat` files, `pythonw.exe`          |
| Automation Logic | os, shutil, datetime, logging, re, subprocess                |

---

## 💼 Real-World Use Cases

- 🧾 **Finance/Accounting Automation**: Remove manual PDF merging, renaming, and reporting.
- 🧠 **Smart Document Handling**: From OCR to index extraction and DB update.
- 🔐 **Secure Integrations**: Avoid hardcoding passwords; use Windows Credential Vault.
- 📁 **File/Folder Governance**: PowerShell automation for file cleanup based on DB metadata.
- 📣 **Email Notification Engine**: Realtime status updates to team inboxes.

---

## ⚙️ Setup Instructions

Each subfolder includes its own setup in `README.md`, but general setup includes:

```bash
pip install -r requirements.txt
```

Recommended dependencies:

```txt
pyodbc
PyPDF2
PyMuPDF
reportlab
pillow
pywin32
pytesseract
requests
```

PowerShell Setup (optional):

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📌 What Makes This Project Unique

✔️ **Enterprise-grade** document processing pipeline
✔️ Fully **modular and scalable**
✔️ Uses **secure credential storage** (no hardcoded passwords)
✔️ Demonstrates skills in **OCR, SQL, APIs, PowerShell, and Windows automation**
✔️ Designed for **real production use** in high-volume accounting scenarios

---

## 🔗 Repository

> 📂 Main Repo: [PDF-Processing-Automation-Ballard-Spahr-](https://github.com/abhijeetraj22/PDF-Processing-Automation-Ballard-Spahr-)

> 💼 Designed & developed by **Abhijeet Raj** to automate complex financial document workflows for enterprise systems.

---

Would you like this `README.md` provided as a downloadable file or directly inserted into your GitHub repo as Markdown?
