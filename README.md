# SUN-DOC

**Desktop application for automated document management and service documentation in PV plant operations.**

Built with Python and PyQt5, SUN-DOC was developed to streamline internal workflows at a solar energy service company — replacing manual document handling with an automated, database-backed GUI tool.

---

## What it does

SUN-DOC combines two core modules into a single desktop application:

### 📄 Article Fetcher
- Loads article/component lists from **CSV, Excel or ODS files**, or directly from a **MySQL database** via configurable SQL queries
- Matches articles against files in a source directory and **automatically copies matching documents** to a target folder
- Marks matched entries visually in the UI table
- Generates a **log file** summarizing results (matched, unmatched, copied count)

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
| GUI | PyQt5 + Qt Designer (`.ui` files) |
| Data processing | Pandas |
| ORM / local DB | SQLAlchemy (SQLite) |
| External DB | MySQL (via mysqlx) |
| Packaging | PyInstaller (`.exe` build included) |
| Styling | Custom QSS stylesheet |

---

## Project Structure

```
src/
├── main.py                  # Application entry point
├── database/                # SQLAlchemy models, queries, DB init
├── directories/             # Path management and document helpers
├── events/                  # Qt event filters
├── files/                   # File system operations, logging, config
├── save_file/               # Session save/load
├── source/                  # Data loading (file & DB)
├── styles/                  # QSS stylesheet and style handler
└── ui/
    ├── blacklists/          # Blacklist dialog logic
    ├── buttons/             # Button configuration and mapping
    ├── icons/               # UI icons (PNG)
    ├── menus/               # Menu bar setup
    ├── tables/              # Table population, search, sorting
    ├── text_edits/          # Form field logic and validation
    └── windows/             # Main window + settings dialogs (.ui + generated Python)
```

---

## Background

This tool was built independently during my time as a Service Project Manager for PV installations, to solve a concrete operational problem: matching hundreds of component documents to service orders efficiently. It replaced a fully manual process and was used productively in day-to-day operations.

---

## Requirements

```
Python 3.10+
PyQt5
pandas
sqlalchemy
mysqlx
```

Install dependencies:
```bash
pip install PyQt5 pandas sqlalchemy mysql-connector-python
```

Run the app:
```bash
cd src
python main.py
```

---

## Status

This project reflects a real-world internal tool developed without formal software engineering guidance. It is shared here as a portfolio project demonstrating practical Python, PyQt5, and database integration skills.
