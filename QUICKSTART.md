# 🚀 Quick Start Guide

Get the PDF Applicant Info Extractor running in under 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd LLM-Sumamry-Transcript
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp env.example .env

# Open .env in your favorite editor and add your OpenAI API key
# Replace 'your_openai_api_key_here' with your actual key
```

Your `.env` should look like:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Choose Your Method

#### Option A: Automated Scripts (Easiest) 🎯

**macOS/Linux:**

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Start everything at once
./scripts/start-all.sh
```

This will open two terminal windows:

- One for the backend (API server)
- One for the frontend (web interface)

**Windows:**

```bash
# Terminal 1 - Backend
scripts\start-backend.bat

# Terminal 2 - Frontend (in a new terminal)
pnpm install
pnpm dev
```

#### Option B: Docker (For Production) 🐳

```bash
# Start everything with Docker Compose
docker-compose up
```

That's it! Docker will handle all dependencies.

#### Option C: Manual Setup (Most Control) 🔧

**Terminal 1 - Backend:**

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend:**

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev
```

### 4. Access the Application

Once both services are running:

- **Web Interface**: http://localhost:3000
- **API Documentation**: http://127.0.0.1:8000/docs
- **API Endpoint**: http://127.0.0.1:8000/api/v1/process

### 5. Test It Out

1. Open http://localhost:3000 in your browser
2. Click the upload area or drag a PDF file
3. Click "Upload Documents"
4. Watch the AI extract information!

## Troubleshooting

### "Command not found: uvicorn"

**Solution:** Install Python dependencies

```bash
pip install -r requirements.txt
```

### "Command not found: pnpm"

**Solution:** Install pnpm

```bash
npm install -g pnpm
```

Or use npm instead:

```bash
npm install
npm run dev
```

### "OPENAI_API_KEY environment variable is required"

**Solution:** Make sure you:

1. Created the `.env` file: `cp env.example .env`
2. Added your actual API key to `.env`
3. Restarted the backend server

### Port Already in Use

**Backend (port 8000):**

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9  # macOS/Linux
```

**Frontend (port 3000):**

```bash
# Find and kill the process
lsof -ti:3000 | xargs kill -9  # macOS/Linux
```

### Import Errors in Python

**Solution:** Make sure you're in the project root directory and the virtual environment is activated:

```bash
# Should show (venv) at the start of your prompt
source venv/bin/activate

# Reinstall if needed
pip install -r requirements.txt
```

### Docker Issues

**Solution:** Make sure Docker is running and try:

```bash
# Rebuild containers
docker-compose up --build

# Clean start
docker-compose down
docker-compose up
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [SECURITY.md](SECURITY.md) before deploying to production
- Explore the API at http://127.0.0.1:8000/docs
- Customize settings in `.env`

## Common Commands

```bash
# Start backend only
./scripts/start-backend.sh

# Start frontend only
./scripts/start-frontend.sh

# Start with Docker
docker-compose up

# Stop Docker services
docker-compose down

# View logs
docker-compose logs -f

# Update dependencies
pip install -r requirements.txt
pnpm install
```

## Getting Help

- 📚 Full documentation: [README.md](README.md)
- 🔒 Security guide: [SECURITY.md](SECURITY.md)
- 🐛 Found a bug? Open an issue on GitHub
- 💡 Have a question? Check the API docs at `/docs`

---

**Happy extracting! 🎉**
