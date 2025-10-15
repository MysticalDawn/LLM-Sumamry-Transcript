# 📄 LLM PDF Applicant Info Extractor

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-15.2.4-black.svg)

A modern, full-stack application that intelligently extracts applicant information from PDF documents using OpenAI's GPT-4 and advanced RAG (Retrieval Augmented Generation) techniques.

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security) • [API Documentation](#-api-documentation)

</div>

---

## ✨ Features

- 🤖 **AI-Powered Extraction**: Leverages GPT-4 to intelligently extract applicant information
- 📊 **Smart Processing**: Automatically chooses between direct processing and RAG based on document size
- 🎨 **Modern UI**: Beautiful, responsive Next.js frontend with Tailwind CSS and shadcn/ui components
- ⚡ **Fast & Efficient**: Optimized token usage with intelligent chunking for large documents
- 🔒 **Security First**: Built with security best practices (see [Security](#-security) section)
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🎯 **Type-Safe**: Full TypeScript support on the frontend
- 🐳 **Docker Ready**: Easy deployment with Docker and Docker Compose
- 📦 **Modular Architecture**: Clean, maintainable code structure

## 🎯 What It Extracts

The application can extract various applicant information including:

- 📚 GPA (Grade Point Average)
- 🎓 Intended Major
- 📝 Test Scores (SAT, ACT, etc.)
- 👤 Personal Information
- And more...

## 🚀 Quick Start

### Option 1: Using Scripts (Recommended)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd LLM-Sumamry-Transcript

# 2. Set up environment variables
cp env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Make scripts executable (Unix/Mac)
chmod +x scripts/*.sh

# 4. Start everything
./scripts/start-all.sh
```

### Option 2: Using Docker

```bash
# 1. Clone and configure
git clone <your-repo-url>
cd LLM-Sumamry-Transcript
cp env.example .env
# Edit .env and add your OPENAI_API_KEY

# 2. Start with Docker Compose
docker-compose up
```

### Option 3: Manual Start

```bash
# Terminal 1 - Backend
./scripts/start-backend.sh

# Terminal 2 - Frontend
./scripts/start-frontend.sh
```

**Access the application:**

- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Next.js UI    │────────▶│  FastAPI Backend │────────▶│   OpenAI GPT-4  │
│  (TypeScript)   │  HTTP   │     (Python)     │   API   │   + Embeddings  │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  FAISS Vector DB │
                            │   (for RAG)      │
                            └──────────────────┘
```

### Processing Flow

1. **Small Documents** (≤4000 tokens): Direct GPT-4 processing
2. **Large Documents** (>4000 tokens): RAG with FAISS vector store
   - Document is split into chunks
   - Chunks are embedded and stored in FAISS
   - Relevant chunks are retrieved for context
   - GPT-4 processes with retrieved context

## 📁 Project Structure

```
LLM-Sumamry-Transcript/
├── backend/                 # Python FastAPI backend
│   ├── api/                # API routes
│   │   ├── __init__.py
│   │   └── routes.py       # Endpoint definitions
│   ├── config/             # Configuration
│   │   ├── __init__.py
│   │   └── settings.py     # Environment settings
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── pdf_processor.py   # PDF text extraction
│   │   ├── llm_service.py     # LLM interactions
│   │   └── pdf_generator.py   # PDF report generation
│   ├── utils/              # Utilities
│   │   ├── __init__.py
│   │   └── validators.py   # File validation
│   ├── __init__.py
│   └── main.py             # FastAPI app entry point
│
├── app/                    # Next.js app directory
│   ├── page.tsx           # Main upload page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
│
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   └── theme-provider.tsx
│
├── scripts/              # Startup scripts
│   ├── start-backend.sh  # Start backend (Unix/Mac)
│   ├── start-backend.bat # Start backend (Windows)
│   ├── start-frontend.sh # Start frontend
│   └── start-all.sh      # Start both services
│
├── outputs/              # Generated PDF reports
├── public/               # Static assets
├── lib/                  # Frontend utilities
├── hooks/                # React hooks
│
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .dockerignore         # Docker ignore rules
│
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
├── env.example          # Environment variables template
├── .gitignore           # Git ignore rules
│
├── README.md            # This file
└── SECURITY.md          # Security documentation
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- pnpm (or npm/yarn)
- OpenAI API key

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd LLM-Sumamry-Transcript
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp env.example .env
   ```

   Edit `.env` and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_actual_api_key_here
   ALLOWED_ORIGINS=http://localhost:3000
   ```

5. **Start the FastAPI server**

   ```bash
   # Using the script (recommended)
   ./scripts/start-backend.sh

   # Or manually
   uvicorn backend.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Install Node.js dependencies**

   ```bash
   pnpm install
   # or: npm install
   # or: yarn install
   ```

2. **Start the development server**

   ```bash
   # Using the script (recommended)
   ./scripts/start-frontend.sh

   # Or manually
   pnpm dev
   # or: npm run dev
   # or: yarn dev
   ```

   The frontend will be available at `http://localhost:3000`

## 📖 Usage

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:3000`
2. Click the upload area or drag and drop a PDF file
3. Click "Upload Documents" to process
4. Wait for the AI to extract the information
5. View the extracted results on the page

### Using the API Directly

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

Response:

```json
{
  "tokens": 1234,
  "mode": "direct",
  "response": "Extracted information here...",
  "output_file": "outputs/output.pdf"
}
```

## 🔒 Security

This project takes security seriously. Here are the security measures implemented:

### ✅ Implemented Security Features

- ✅ **Environment Variables**: API keys stored securely in `.env` (not committed to git)
- ✅ **CORS Protection**: Configurable allowed origins (no wildcard `*` in production)
- ✅ **File Size Limits**: Maximum 10MB file size to prevent DoS attacks
- ✅ **File Type Validation**: Validates actual file content, not just extensions
- ✅ **Input Sanitization**: Proper error handling and validation
- ✅ **Modular Architecture**: Separation of concerns for better security
- ✅ **Secure Dependencies**: Using specific version pins in `requirements.txt`

### 🔐 Security Best Practices for Production

See [SECURITY.md](SECURITY.md) for detailed security information.

Quick checklist:

- [ ] Set proper CORS origins in `.env`
- [ ] Use HTTPS in production
- [ ] Add rate limiting
- [ ] Implement authentication if needed
- [ ] Set up monitoring and logging
- [ ] Review and limit API permissions
- [ ] Keep dependencies updated

## 📚 API Documentation

### Endpoints

#### `POST /api/v1/process`

Process a PDF file and extract applicant information.

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: PDF file

**Response:**

```typescript
{
  tokens: number; // Number of tokens in the document
  mode: "direct" | "RAG"; // Processing mode used
  response: string; // Extracted information
  output_file: string; // Path to generated PDF report
}
```

**Status Codes:**

- `200`: Success
- `400`: Invalid file or bad request
- `413`: File too large
- `500`: Server error

#### `GET /api/v1/health`

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "service": "pdf-extractor"
}
```

### Interactive API Docs

When the server is running, visit:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🛠️ Technology Stack

### Backend

- **FastAPI**: Modern, fast web framework for building APIs
- **PyMuPDF (fitz)**: PDF text extraction
- **LangChain**: LLM orchestration and RAG implementation
- **FAISS**: Vector similarity search for RAG
- **OpenAI**: GPT-4 and embeddings
- **tiktoken**: Token counting
- **FPDF**: PDF generation
- **python-magic**: File type validation

### Frontend

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Beautiful, accessible component library
- **Lucide React**: Icon library

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Using Docker Directly

```bash
# Build the image
docker build -t pdf-extractor .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/outputs:/app/outputs \
  pdf-extractor
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🧪 Testing

```bash
# Backend tests (coming soon)
pytest

# Frontend tests (coming soon)
pnpm test
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and embeddings API
- LangChain for the excellent LLM framework
- FastAPI for the amazing web framework
- shadcn for the beautiful UI components

## 📧 Support

If you have any questions or run into issues, please:

1. Check the [API Documentation](#-api-documentation)
2. Review the [Security](#-security) section
3. Read [SECURITY.md](SECURITY.md) for detailed security information
4. Open an issue on GitHub

## 🗺️ Roadmap

- [ ] Add support for more document formats (DOCX, TXT)
- [ ] Implement user authentication
- [ ] Add batch processing capabilities
- [ ] Add comprehensive test suite
- [ ] Implement caching for faster repeated queries
- [ ] Add support for custom extraction templates
- [ ] Create admin dashboard for monitoring
- [ ] Add rate limiting middleware
- [ ] Implement request logging
- [ ] Add API key rotation

## 📊 Performance

- **Small documents** (<4000 tokens): ~2-5 seconds
- **Large documents** (>4000 tokens): ~10-30 seconds (depends on size)
- **Concurrent requests**: Supports multiple simultaneous uploads
- **Token efficiency**: Optimized chunking reduces API costs

## 🌍 Environment Variables

All configurable options are available in `env.example`. Copy it to `.env` and customize:

```bash
cp env.example .env
```

Key variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `ALLOWED_ORIGINS`: CORS allowed origins
- `MAX_FILE_SIZE`: Maximum upload size in bytes
- `MODEL_NAME`: OpenAI model to use (default: gpt-4)
- `MAX_TOKENS`: Token threshold for RAG mode
- `OUTPUT_DIR`: Directory for generated reports

---

<div align="center">

Made with ❤️ using FastAPI and Next.js

**Version 2.0.0** - Refactored with improved architecture and security

</div>
