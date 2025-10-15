#!/bin/bash
# Start the backend server

echo "🚀 Starting PDF Extractor Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please create a .env file from env.example"
    echo "   cp env.example .env"
    echo "   Then edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Start the server
echo "✅ Starting server on http://127.0.0.1:8000"
echo "📚 API docs available at http://127.0.0.1:8000/docs"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

