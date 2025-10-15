# 🏗️ Architecture Documentation

## System Overview

The PDF Applicant Info Extractor is a full-stack application built with a modern, modular architecture that separates concerns and follows best practices.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                     http://localhost:3000                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Next.js Frontend (Port 3000)                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  app/page.tsx - Upload Interface                           │ │
│  │  components/ui/ - shadcn/ui Components                     │ │
│  │  Tailwind CSS - Styling                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP POST /api/v1/process
                         │ multipart/form-data
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    backend/main.py                         │ │
│  │              FastAPI App + CORS Middleware                 │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                        │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │                   backend/api/routes.py                    │ │
│  │              POST /api/v1/process                          │ │
│  │              GET  /api/v1/health                           │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                        │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │               backend/utils/validators.py                  │ │
│  │          File Size, Type, MIME Validation                  │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                        │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │            backend/services/pdf_processor.py               │ │
│  │          Extract Text, Count Tokens, Decide Mode           │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                        │
│                    ┌────┴────┐                                  │
│                    │         │                                  │
│         ≤4000 tokens│         │>4000 tokens                     │
│                    │         │                                  │
│         ┌──────────▼─┐     ┌─▼──────────┐                      │
│         │   Direct   │     │    RAG     │                      │
│         │ Processing │     │ Processing │                      │
│         └──────┬─────┘     └─────┬──────┘                      │
│                │                 │                              │
│  ┌─────────────▼─────────────────▼──────────────────────────┐  │
│  │           backend/services/llm_service.py                │  │
│  │     extract_direct()    extract_with_rag()               │  │
│  └─────────────┬─────────────────┬──────────────────────────┘  │
│                │                 │                              │
│                │                 │ Chunk + Embed                │
│                │                 ▼                              │
│                │        ┌─────────────────┐                     │
│                │        │  FAISS Vector   │                     │
│                │        │    Database     │                     │
│                │        └────────┬────────┘                     │
│                │                 │ Retrieve                     │
│                │                 │                              │
│                └─────────┬───────┘                              │
│                          │                                      │
│                          ▼                                      │
│                 ┌─────────────────┐                             │
│                 │  OpenAI GPT-4   │                             │
│                 │   + Embeddings  │                             │
│                 └────────┬────────┘                             │
│                          │                                      │
│                          │ AI Response                          │
│                          ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          backend/services/pdf_generator.py                 │ │
│  │              Generate PDF Report                           │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                        │
│                         ▼                                        │
│                  outputs/output.pdf                              │
└─────────────────────────┬────────────────────────────────────────┘
                          │
                          │ JSON Response
                          ▼
                    ┌─────────────┐
                    │   Browser   │
                    │   Display   │
                    └─────────────┘
```

## Module Breakdown

### Backend Modules

#### 1. `backend/main.py` - Application Entry Point

```python
Responsibilities:
- Initialize FastAPI app
- Configure CORS middleware
- Include API routers
- Validate settings on startup
- Provide root endpoint

Dependencies:
- FastAPI framework
- backend.config.settings
- backend.api.router
```

#### 2. `backend/api/routes.py` - API Endpoints

```python
Responsibilities:
- Define REST API endpoints
- Handle HTTP requests/responses
- Orchestrate service calls
- Error handling

Endpoints:
- POST /api/v1/process - Process PDF file
- GET /api/v1/health - Health check

Dependencies:
- backend.utils.validators
- backend.services.*
```

#### 3. `backend/config/settings.py` - Configuration

```python
Responsibilities:
- Load environment variables
- Provide configuration object
- Validate required settings
- Set defaults

Configuration Areas:
- OpenAI API settings
- CORS settings
- File upload limits
- LLM parameters
- RAG parameters
```

#### 4. `backend/services/pdf_processor.py` - PDF Processing

```python
Responsibilities:
- Extract text from PDF bytes
- Count tokens in text
- Determine processing mode (direct vs RAG)

Dependencies:
- PyMuPDF (fitz)
- tiktoken
```

#### 5. `backend/services/llm_service.py` - LLM Interactions

```python
Responsibilities:
- Direct GPT-4 processing
- RAG-based processing
- Manage LangChain components

Components:
- ChatOpenAI (GPT-4)
- OpenAIEmbeddings
- RecursiveCharacterTextSplitter
- FAISS vector store
- RetrievalQA chain
```

#### 6. `backend/services/pdf_generator.py` - Report Generation

```python
Responsibilities:
- Generate PDF reports from text
- Handle word wrapping
- Manage output directory

Dependencies:
- FPDF library
```

#### 7. `backend/utils/validators.py` - Validation

```python
Responsibilities:
- Validate file size
- Validate file extension
- Validate MIME type
- Comprehensive file validation

Dependencies:
- python-magic
```

### Frontend Structure

#### 1. `app/page.tsx` - Main Interface

```typescript
Responsibilities:
- File upload interface
- Progress tracking
- Result display
- Error handling

State Management:
- File selection
- Upload progress
- Processing status
- Results data
```

#### 2. `components/ui/*` - UI Components

```typescript
Components:
- Button, Card, Alert
- Progress, Input, Label
- Dialog, Toast, etc.

Framework:
- Radix UI primitives
- Tailwind CSS styling
- shadcn/ui patterns
```

## Data Flow

### Upload and Processing Flow

```
1. User Action
   └─> Select PDF file in browser

2. Frontend Validation
   └─> Check file type (.pdf)
   └─> Create FormData

3. HTTP Request
   └─> POST to /api/v1/process
   └─> multipart/form-data

4. Backend Validation
   └─> File size check (≤10MB)
   └─> Extension check (.pdf)
   └─> MIME type check (application/pdf)

5. PDF Processing
   └─> Extract text with PyMuPDF
   └─> Count tokens with tiktoken

6. Mode Selection
   └─> If ≤4000 tokens: Direct Processing
   └─> If >4000 tokens: RAG Processing

7a. Direct Processing
    └─> Create prompt with full text
    └─> Send to GPT-4
    └─> Get response

7b. RAG Processing
    └─> Split text into chunks
    └─> Generate embeddings
    └─> Store in FAISS
    └─> Create retrieval chain
    └─> Query with specific questions
    └─> Get response

8. Report Generation
   └─> Create PDF with FPDF
   └─> Save to outputs/

9. Response
   └─> Return JSON with:
       - token_count
       - mode (direct/RAG)
       - response text
       - output_file path

10. Frontend Display
    └─> Show results to user
```

## Security Architecture

### Defense in Depth

```
Layer 1: Frontend Validation
├─> File type check
└─> User feedback

Layer 2: Network Security
├─> CORS configuration
└─> HTTPS (production)

Layer 3: API Gateway (FastAPI)
├─> Request validation
└─> Rate limiting (optional)

Layer 4: File Validation
├─> Size limits
├─> Extension check
└─> MIME type verification

Layer 5: Input Sanitization
├─> Error handling
└─> Safe file processing

Layer 6: Environment Security
├─> API key in .env
├─> No secrets in code
└─> Validated configuration
```

## Deployment Architecture

### Development

```
┌─────────────────┐     ┌─────────────────┐
│   Frontend      │     │    Backend      │
│   localhost:3000│────▶│ 127.0.0.1:8000  │
│   (pnpm dev)    │     │ (uvicorn reload)│
└─────────────────┘     └─────────────────┘
```

### Docker Deployment

```
┌──────────────────────────────────────┐
│         Docker Compose               │
│  ┌────────────┐    ┌──────────────┐ │
│  │  Frontend  │    │   Backend    │ │
│  │ Container  │───▶│  Container   │ │
│  │  Port 3000 │    │  Port 8000   │ │
│  └────────────┘    └──────────────┘ │
│                                      │
│  Volumes:                            │
│  - ./backend → /app/backend          │
│  - ./outputs → /app/outputs          │
└──────────────────────────────────────┘
```

### Production (Recommended)

```
                    ┌──────────────┐
                    │   Nginx      │
                    │  (Reverse    │
                    │   Proxy)     │
                    └───┬──────┬───┘
                        │      │
         ┌──────────────┘      └──────────────┐
         │                                    │
    ┌────▼─────┐                      ┌──────▼────┐
    │ Frontend │                      │  Backend  │
    │  (Next)  │                      │ (Gunicorn)│
    │  Static  │                      │  Workers  │
    └──────────┘                      └───────────┘
                                            │
                                      ┌─────▼─────┐
                                      │  OpenAI   │
                                      │    API    │
                                      └───────────┘
```

## Configuration Management

### Environment Variables Flow

```
env.example
    │
    ├─> Copy to .env (user action)
    │
    └─> .env (gitignored)
         │
         ├─> Loaded by python-dotenv
         │
         └─> backend/config/settings.py
              │
              ├─> Settings validation
              │
              └─> Used throughout backend
```

## Error Handling Flow

```
Error Occurs
    │
    ├─> ValueError (validation error)
    │   └─> HTTPException(400)
    │
    ├─> HTTPException (already handled)
    │   └─> Return as-is
    │
    └─> Exception (unexpected)
        └─> HTTPException(500)
            └─> Generic error message
                └─> JSON response to frontend
                    └─> Display to user
```

## Scalability Considerations

### Current Architecture

- Single server deployment
- Synchronous processing
- In-memory FAISS

### Future Scalability Options

```
Load Balancer
    │
    ├─> Backend Instance 1
    ├─> Backend Instance 2
    └─> Backend Instance 3
         │
         ├─> Shared Redis Cache
         ├─> Persistent Vector DB (Pinecone/Weaviate)
         └─> Queue System (Celery/RabbitMQ)
```

## Technology Decisions

### Why FastAPI?

- ✅ High performance (async support)
- ✅ Automatic API documentation
- ✅ Type hints and validation
- ✅ Modern Python features

### Why Next.js?

- ✅ React with server-side rendering
- ✅ Great developer experience
- ✅ Built-in optimization
- ✅ TypeScript support

### Why LangChain?

- ✅ LLM orchestration
- ✅ RAG support out of the box
- ✅ Multiple LLM providers
- ✅ Active community

### Why FAISS?

- ✅ Fast similarity search
- ✅ No external dependencies
- ✅ Good for prototyping
- ✅ Can scale to production

## Performance Characteristics

### Time Complexity

- File validation: O(1)
- Text extraction: O(n) where n = pages
- Token counting: O(m) where m = characters
- Direct processing: O(1) API call
- RAG processing: O(k log n) where k = chunks, n = vector size

### Space Complexity

- File upload: O(file_size) - max 10MB
- Text storage: O(text_length)
- Vector embeddings: O(chunks × embedding_dim)
- FAISS index: O(chunks × embedding_dim)

## Monitoring Points

### Key Metrics to Track

1. Request rate (requests/minute)
2. Processing time (seconds/request)
3. Error rate (errors/requests)
4. Token usage (tokens/request)
5. OpenAI API costs ($/request)
6. File sizes (MB/request)

### Health Checks

- `/api/v1/health` - Backend availability
- OpenAI API connectivity
- File system write access
- Memory usage

---

## Quick Reference

### Key Files

- `backend/main.py` - App entry point
- `backend/api/routes.py` - API endpoints
- `backend/config/settings.py` - Configuration
- `app/page.tsx` - Frontend UI

### Key Endpoints

- `POST /api/v1/process` - Main processing
- `GET /api/v1/health` - Health check
- `GET /docs` - API documentation

### Key Services

- `PDFProcessor` - PDF handling
- `LLMService` - AI processing
- `PDFGenerator` - Report creation

---

**Last Updated**: October 15, 2025  
**Version**: 2.0.0
