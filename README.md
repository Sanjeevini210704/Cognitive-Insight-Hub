# CogniScan — Cognitive Insight Hub

A pure-Python rebuild of CogniScan: a cognitive behavior analysis platform that
analyses social-media consumption and produces a clinical-style report.

- **Backend / UI:** Streamlit
- **Charts:** Plotly
- **Database:** MontyDB (a local, file-based database that speaks the MongoDB / PyMongo API — no MongoDB server required)
- **Auth:** bcrypt-hashed passwords

---

## Run on Windows — step by step

### 1. Install Python 3.11

1. Go to <https://www.python.org/downloads/windows/> and download **Python 3.11.x** (3.11.9 recommended).
2. Run the installer and **tick the box "Add python.exe to PATH"** on the very first screen.
3. Click *Install Now*.
4. Open **Command Prompt** (press `Win + R`, type `cmd`, hit Enter) and confirm:
   ```bat
   python --version
   ```
   You should see `Python 3.11.x`.

> Python 3.12 / 3.13 also work, but 3.11 is what the project was developed against.

### 2. Get the project files

You can either:

- **Download a ZIP** from Replit (three-dots menu → *Download as zip*), then unzip it somewhere like `C:\Users\<you>\cogniscan`, **or**
- **Clone with Git** if you have it:
  ```bat
  git clone <your-repo-url> cogniscan
  ```

Open Command Prompt and `cd` into the project folder:
```bat
cd C:\Users\<you>\cogniscan
```

### 3. One-click launch (easiest)

Just double-click **`run.bat`** in the project folder. It will:

1. Create a virtual environment in `.venv\` (first run only).
2. Install all required packages from `requirements.txt`.
3. Start the app at <http://localhost:5000>.

When you see `You can now view your Streamlit app...`, open
<http://localhost:5000> in your browser.

### 4. Manual setup (if you prefer)

```bat
:: 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

:: 2. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 3. Run the app
streamlit run app.py --server.port 5000
```

To stop the app, press `Ctrl + C` in the Command Prompt window.

To start it again later:
```bat
.venv\Scripts\activate.bat
streamlit run app.py --server.port 5000
```

---

## Default demo accounts

These are seeded automatically the first time the app runs:

| Role  | Email                   | Password    |
|-------|-------------------------|-------------|
| User  | `demo@cogniscan.ai`     | `demo1234`  |
| Admin | `admin@cogniscan.ai`    | `admin1234` |

You can also click **Register** on the patient login screen to make a new user account.

---

## Where data is stored

MontyDB writes a small local database file under `./montydb_store/` in the
project folder. To reset all users and analyses, simply delete that folder and
restart the app — the demo accounts will be re-seeded.

---

## Project layout

```
cogniscan/
├─ app.py                   # Streamlit entry point + routing
├─ cogni_scan/
│  ├─ db.py                 # MontyDB connection, collections (users, analyses)
│  ├─ auth.py               # bcrypt login / register / seed users
│  ├─ analyzer.py           # Rule-based NLP scoring engine
│  ├─ charts.py             # Plotly chart builders
│  └─ styles.py             # Custom CSS for the clinical dark theme
├─ .streamlit/config.toml   # Streamlit server config
├─ requirements.txt         # Python dependencies
├─ run.bat                  # One-click Windows launcher
└─ README.md
```

The `artifacts/`, `lib/`, `node_modules/`, `package.json`, `pnpm-*.yaml`,
`tsconfig*.json`, `pyproject.toml`, `uv.lock`, and `.replit` files are
Replit-specific scaffolding and are **not needed** to run the app on Windows.
You can safely delete them if you want a clean Python-only project.

---

## Troubleshooting

**`'python' is not recognized as an internal or external command`**
Re-install Python and tick *Add python.exe to PATH*, or use the full path
`C:\Users\<you>\AppData\Local\Programs\Python\Python311\python.exe`.

**`Port 5000 is not available`**
Another program is using port 5000. Either close it, or run on a different
port:
```bat
streamlit run app.py --server.port 8501
```

**`pip` install errors about `bcrypt` / build tools**
Run `python -m pip install --upgrade pip wheel setuptools` and try again.
Pre-built wheels exist for Python 3.10–3.13 on Windows, so no compiler is
needed.

**Browser shows a blank page or "WebSocket onclose" warnings**
Hard-refresh with `Ctrl + F5`, or try a different browser (Chrome / Edge).
