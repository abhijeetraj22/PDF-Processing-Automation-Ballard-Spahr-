# 📁 Json Data Extraction Using Token

This project demonstrates a **complete Python + PowerShell solution** for securely accessing a protected API using **bearer token authentication**, extracting and flattening **nested JSON data**, and inserting the processed data into a **SQL Server** database. Additionally, PowerShell scripts are used to dynamically create or clean up local folders based on database values.

---

## 🔧 Features Implemented

### ✅ Python Scripts

#### 1. `GenerateAccessToken22122.py`

* Authenticates with a token endpoint using `client_id`, `client_secret`, and `grant_type`.
* Sends a POST request via **proxy** with custom headers.
* Extracts `access_token` from the response.
* Uses the token to query a **secured API endpoint** with JSON payload.
* Returns nested JSON response.

#### 2. `jsondataExtraxt2024.py`

* Reads nested JSON response from a file (or directly from an API).
* Uses recursive function `combine_keys()` to **flatten deeply nested JSON** objects.
* Dynamically creates SQL table using all flattened keys.
* Ensures primary keys like `client_artifactID`, `workspace_artifactID` are handled.
* Handles insertions with duplicate key checks and skips existing entries.

---

### ✅ PowerShell Scripts

#### 3. `createFolderUseSQLDelFilesOnly.ps1`

* Connects to SQL Server and runs query: `SELECT DISTINCT BC FROM DummyData`
* Deletes only files inside existing folders under a specified base path.
* Retains empty folder structure.
* Creates folders dynamically based on values in the `BC` column from the database.

#### 4. `createFolderUseSQL22.ps1`

* Fully deletes all subfolders and files recursively from the base path.
* Recreates the folder structure using values from the `BC` column in SQL Server.

---

## 🛠 Technologies Used

| Technology | Purpose                          |
| ---------- | -------------------------------- |
| Python 3.x | API communication & data parsing |
| `requests` | Making HTTP requests with proxy  |
| `pyodbc`   | SQL Server connectivity          |
| `json`     | JSON file manipulation           |
| PowerShell | File/folder automation           |
| SQL Server | Backend database                 |

---

## 📂 Project Structure

```
JsonDataExtractionUsingToken/
├── GenerateAccessToken22122.py      # Token generation and API call
├── jsondataExtraxt2024.py           # JSON flattening and SQL insert
├── createFolderUseSQLDelFilesOnly.ps1 # Folder creation, delete files only
├── createFolderUseSQL22.ps1         # Full folder deletion and recreation
```

---

## ⚙️ Setup & Execution

### 🐍 Python Setup

1. Install dependencies:

```bash
pip install requests pyodbc
```

2. Configure `client_id`, `client_secret`, and API endpoints in `GenerateAccessToken22122.py`.
3. Run the token + data flow:

```bash
python GenerateAccessToken22122.py
```

4. To process from saved JSON file:

```bash
python jsondataExtraxt2024.py
```

### 💻 PowerShell Usage

* Make sure you have permission to run scripts:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

* Run scripts:

```powershell
.\createFolderUseSQLDelFilesOnly.ps1
.\createFolderUseSQL22.ps1
```

---

## 📌 Highlights

* 🔐 Secure API access using token auth and proxy support.
* 🧩 Auto-detection and flattening of nested JSON keys.
* 🗃️ Auto-creation of SQL Server tables based on JSON.
* 📁 Smart folder automation based on SQL values.

---

## 📣 Notes

This project showcases:

* Enterprise-ready data automation.
* Secure API integration and dynamic table creation.
* Hybrid development across Python and PowerShell.
* Production-quality, modular and scalable approach.

---

## 🔗 GitHub Repository

> [JsonDataExtractionUsingToken](https://github.com/abhijeetraj22/PDF-Processing-Automation-Ballard-Spahr-/new/main/JsonDataExtractionUsingToken)
> *Clone and configure.*
---

