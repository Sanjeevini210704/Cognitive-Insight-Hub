@echo off
REM ===== CogniScan Windows launcher =====

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing/updating dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Starting CogniScan on http://localhost:5000 ...
streamlit run app.py --server.port 5000

pause
