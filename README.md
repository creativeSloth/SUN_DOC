# SUN-DOC

**Desktop application for automated document management and service documentation in PV plant operations.**

Built with Python and PyQt5, SUN-DOC was developed to streamline internal workflows at a solar energy service company — replacing manual document handling with an automated, database-backed GUI tool.

---

## Status

⚠️ This project is currently under active development.
The codebase is still evolving, and functionality, structure, and dependencies may change at any time. This repository is not yet intended for production use.

This project reflects a real-world internal tool developed without formal software engineering guidance. It is shared here as a portfolio project demonstrating practical Python, PyQt5, and database integration skills.

---

## System Requirements
Python 3.8.x (mandatory; the project is not compatible with Python versions >3.8)
Virtual environment recommended
All dependencies listed in requirements.txt

⚠️ Make sure to create a Python 3.8 virtual environment before installing dependencies.

---

## What it does

SUN-DOC combines two core modules into a single desktop application:

### 📄 Article Fetcher
- Loads article/component lists from **CSV, Excel or ODS files**, or directly from a **MySQL database** via configurable SQL queries
- Matches articles against files in a source directory and **automatically copies matching documents** to a target folder
- Marks matched entries visually in the UI table
- Generates a **log file** summarising results (matched, unmatched, copied count)

### 🛠️ Documentation Module
- Loads device-specific data (PV modules, inverters, batteries, charge points) from a database
- Fills **Word document templates** automatically with device specifications pulled from the database
- Supports two parallel document workflows (Doc 1 / Doc 2) with separate templates and target paths
- Allows manual entry and persistent storage of device specs (power, capacity, coupling type, battery technology)

### 🗃️ Local Database (SQLite via SQLAlchemy)
- Stores articles, device specifications, and **blacklists** per component category (modules, PV inverters, battery inverters, batteries, charge points)
- Blacklist entries track which articles are excluded from which workflows, with timestamps

### ⚙️ Settings & Persistence
- All paths (source, target, templates) configurable via settings dialogs
- SQL queries configurable per module
- Session state saved and restored via save/load functionality

---

## Tech Stack

| Layer | Technology |
|---|---|
| GUI | PyQt5 5.15 + Qt Designer (`.ui` files) |
| Data processing | Pandas 2.0 |
| ORM / local DB | SQLAlchemy 2.0 (SQLite) |
| External DB | MySQL (via mysql-connector-python) |
| File handling | odfpy (ODS / LibreOffice Calc) |
| Packaging | PyInstaller (`.exe` build included) |
| Styling | Custom QSS stylesheet |

---

## Project Structure

```
src/
├── main.py                  # Application entry point
├── build.py                 # PyInstaller build script
│
├── database/                # SQLAlchemy models, queries, DB init
│   ├── classes.py           # ORM models (Article, Blacklists, ArticleSpecifications)
│   ├── constants.py         # DB table and column name constants
│   ├── queries.py           # All DB query and update functions
│   └── utils.py             # Session and engine helpers
│
├── directories/             # Path management and document helpers
│   ├── constants.py         # Static path constants
│   ├── directories_handler.py
│   ├── dirs_decorators.py   # Path validation decorators
│   └── document_helpers.py  # Document path helpers
│
├── events/                  # Qt event filters
│   ├── filter.py
│   └── utils.py
│
├── files/                   # File system operations, logging, config
│   ├── logs_and_config.py   # Config file and log management
│   └── sys_files.py         # File matching, copying, path resolution
│
├── save_file/               # Session save/load
│   ├── load.py
│   └── save.py
│
├── source/                  # Data loading (file & DB)
│   └── data_origins.py      # Read from CSV/Excel/ODS or MySQL
│
├── styles/                  # QSS stylesheet and style handler
│   ├── styles_Handler.py
│   └── stylesheet.qss
│
└── ui/
    ├── blacklists/          # Blacklist dialog logic and storage
    ├── buttons/             # Button configuration and mapping
    ├── icons/               # UI icons (PNG)
    ├── menus/               # Menu bar setup
    ├── tables/              # Table population, search, sorting
    ├── text_edits/          # Form field logic and validation
    └── windows/             # Main window + settings dialogs (.ui + generated Python)
        ├── mainwindow.py
        ├── blacklistWindow.py
        ├── settingsConnectionWindow.py
        └── settingsPathsWindow.py
```

---

## Background

This tool was built independently during my time as a Service Project Manager for PV installations, to solve a concrete operational problem: matching hundreds of component documents to service orders efficiently. It replaced a fully manual process and was used productively in day-to-day operations.

---

## Requirements

```
# Must be run on Python 3.8.x
PyQt5==5.15.11
pandas==2.0.3
SQLAlchemy==2.0.32
psycopg2-binary==2.9.9
mysql-connector-python==8.0.32
odfpy==1.4.1
```

Install dependencies:
```bash
python3.8 -m venv .venv38
source .venv38/bin/activate
pip install -r requirements.txt
```

Run the app:
```bash
cd src
python main.py
```
