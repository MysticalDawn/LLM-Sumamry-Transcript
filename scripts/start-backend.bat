@echo off
REM Start the backend server (Windows)

echo 🚀 Starting PDF Extractor Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo 📝 Please create a .env file from env.example
    echo    copy env.example .env
    echo    Then edit .env and add your OPENAI_API_KEY
    exit /b 1
)

REM Start the server
echo ✅ Starting server on http://127.0.0.1:8000
echo 📚 API docs available at http://127.0.0.1:8000/docs
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

