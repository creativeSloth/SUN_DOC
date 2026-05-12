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
mysql-connector-python==8.0.32
psycopg2-binary==2.9.9
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

---

## Docker / PostgreSQL Setup

For local development a Docker-based PostgreSQL stack is provided under
`docker/`. It runs Postgres 16 + Adminer (web UI) and seeds the database
from `docker/initdb/01_schema.sql` on first start — after a fresh clone
the database is ready in under a minute, no manual schema needed.

### Files in the repository

```
docker/
├── docker-compose.yml          # postgres:16 + adminer (tracked)
├── .env.example                # template with default credentials (tracked)
├── .env                        # YOUR real credentials  — NOT tracked (.gitignore)
└── initdb/
    └── 01_schema.sql           # articles table + seed data (tracked)
```

`docker/.env` is intentionally gitignored so secrets never reach the
remote. `docker/.env.example` is whitelisted in `.gitignore` and ships
with the repo — every new contributor copies it to `.env` on first
checkout (see step 2 below).

---

### Step 1 — Install Docker (one-time, per machine)

Skip this section if `docker --version` already works.

#### Ubuntu 24.04 / Linux Mint 22

> ⚠️ On Linux Mint the kernel codename (`zena`, `wilma`, …) is **not**
> a valid Ubuntu codename. Use `noble` (or whatever `UBUNTU_CODENAME`
> shows in `/etc/os-release`).

Copy and run **one block at a time** in a real terminal. Pasting all
blocks at once can break the multi-line `tee` command in some shells.

**1a — Prerequisites and Docker GPG key**
```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

**1b — Register the Docker apt repository**

The line below MUST stay on a single line when pasted. If pasting
breaks it, open the file with `sudo nano /etc/apt/sources.list.d/docker.list`
and put exactly this single line inside:
```
deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable
```

Otherwise run as a single-line command:
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable" | sudo tee /etc/apt/sources.list.d/docker.list
```

**1c — Install Docker Engine + Compose plugin**
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**1d — Allow your user to run Docker without `sudo`**
```bash
sudo usermod -aG docker $USER
```
**Log out and back in** (or reboot) for the group change to take effect.
Until you do, prefix every `docker` command with `sudo`.

**1e — Verify**
```bash
docker run hello-world
```
Expected output ends with `Hello from Docker!`.

---

### Step 2 — First-time setup after a fresh clone

```bash
cd docker
cp .env.example .env
```

Open `docker/.env` and adjust the credentials if you want — the defaults
work out of the box but you should change the password before any
shared environment.

```dotenv
POSTGRES_USER=sundoc_user
POSTGRES_PASSWORD=sundoc123
POSTGRES_DB=sundoc_db
POSTGRES_PORT=5432
ADMINER_PORT=8080
```

If you change the user/password/DB here, also update them in the
SUN-DOC app's connection dialog (or `src/logs/config.ini` if it
already exists).

---

### Step 3 — Start the stack

From the `docker/` directory:

```bash
docker compose up -d
```

What this does:
- Pulls `postgres:16` and `adminer:latest` (~150 MB, only on first run)
- Creates the `pgdata` volume for persistence
- Runs `initdb/01_schema.sql` **once**, creating `articles` and inserting 50 rows
- Starts both containers in the background

Check status:
```bash
docker compose ps
```
Both services should be `running` and postgres `healthy`.

Sanity-check the seed:
```bash
docker compose exec postgres psql -U sundoc_user -d sundoc_db -c "SELECT COUNT(*) FROM articles;"
```
Expected: `50`.

---

### Step 4 — Access the database

| Service  | URL / Port             | How to log in                                          |
|----------|------------------------|--------------------------------------------------------|
| Postgres | `localhost:5432`       | psql / SQLAlchemy with credentials from `docker/.env`  |
| Adminer  | http://localhost:8080  | System=`PostgreSQL`, Server=`postgres`, rest from `.env` |

**Adminer (web UI):** open http://localhost:8080 and fill in:
- System: **PostgreSQL**
- Server: **postgres** (the container hostname — not `localhost`)
- User / Password / Database: from `docker/.env`

**psql in the container:**
```bash
docker compose exec postgres psql -U sundoc_user -d sundoc_db
```

---

### Step 5 — Connect the SUN-DOC app to Postgres

The fastest path is to copy the example config that ships with the repo
(one-time, after fresh clone):

```bash
cp src/logs/config.example.ini src/logs/config.ini
```

This pre-fills the connection settings, the demo SQL query, and points
the source / target paths at `example_data/` (see *Quick start with
example data* below).

Otherwise, configure manually:
1. Start the app (`cd src && python main.py`)
2. Open the connection settings dialog
3. Enter the values from `docker/.env`:
   - **DB type**: `PostgreSQL` (already the default, no need to change)
   - **Server**: `localhost` (or `localhost:5432`)
   - **User**: `sundoc_user`
   - **Password**: `sundoc123`
   - **DB name**: `sundoc_db`
   - **SQL query**: `SELECT article_no, article_name, amount FROM articles;`
4. Click the **load-from-DB** icon button (the database icon next to the
   article list) — 50 rows should appear.

The existing code in `src/source/data_origins.py` already builds the
`postgresql+psycopg2://…` SQLAlchemy URL based on the `DB type`
dropdown, so no code changes are needed.

---

### Daily lifecycle commands

All commands run from `docker/`:

| Goal                                         | Command                              |
|----------------------------------------------|--------------------------------------|
| Start in background                          | `docker compose up -d`               |
| Stop (keep data)                             | `docker compose down`                |
| Stop AND wipe data volume (re-seed on next up) | `docker compose down -v`           |
| Show status                                  | `docker compose ps`                  |
| Tail Postgres logs                           | `docker compose logs -f postgres`    |
| Tail Adminer logs                            | `docker compose logs -f adminer`     |
| Open a psql shell                            | `docker compose exec postgres psql -U sundoc_user -d sundoc_db` |
| Restart only Postgres                        | `docker compose restart postgres`    |
| Update image versions                        | `docker compose pull && docker compose up -d` |

> The seed script in `initdb/` runs **only on an empty data volume**.
> If you change `01_schema.sql` after the first start, the changes are
> NOT picked up automatically — run `docker compose down -v` to wipe
> the volume and re-seed on the next `up`.

---

### Troubleshooting

**Port 5432 already in use** — you probably have a local Postgres
running. Either stop it (`sudo systemctl stop postgresql`) or change
`POSTGRES_PORT` in `docker/.env` to e.g. `5433` and update the app's
connection settings accordingly.

**`permission denied while trying to connect to the Docker daemon socket`** —
you haven't logged out/in after `usermod -aG docker $USER`. Either do
that, or prefix every command with `sudo`.

**App says "Verbindungsfehler"** — verify Postgres is healthy with
`docker compose ps`, then double-check `DB type` is set to
`PostgreSQL` (not `MySQL`) in the connection dialog.

---

## Quick start with example data

The repo ships with a small set of dummy documents under `example_data/`
so a fresh clone can run the full Article Fetcher pipeline end-to-end
without any manual file preparation:

```
example_data/
├── source/
│   ├── inverters_and_modules/   # 5 PDFs / DOCX named with article_no
│   └── cables_and_misc/         # 5 PDFs / DOCX named with article_no
└── target/                      # empty — receives copies on demo run
```

End-to-end run after a fresh clone:

```bash
# 1. Postgres up
cd docker && docker compose up -d && cd ..

# 2. Python deps
python3.8 -m venv .venv38 && source .venv38/bin/activate
pip install -r requirements.txt

# 3. Pre-fill the app config (connection + example paths + demo query)
cp src/logs/config.example.ini src/logs/config.ini

# 4. Start the app
cd src && python main.py
```

In the app:
1. The connection settings, source path (`../example_data/source`) and
   target path (`../example_data/target`) are already populated from
   `config.example.ini`.
2. Click the **load-from-DB** icon button — 50 articles load from
   Postgres.
3. Bold rows indicate articles for which the fetcher found a matching
   file in `example_data/source/` (10 of the 50 articles).
4. Tick the checkboxes for the rows you want to copy.
5. Type a project number into the **Project** field at the top.
6. Click the **copy / paste-docs** icon button — files are copied to
   `example_data/target/<project>/<timestamp>/.../`.
7. A log file lands under `src/logs/hist/`.

> **Path note**: `config.example.ini` uses paths relative to the `src/`
> directory (because the README tells you to start with
> `cd src && python main.py`). If you start the app from a different
> working directory, re-pick the paths via *Settings → Pfade*.
