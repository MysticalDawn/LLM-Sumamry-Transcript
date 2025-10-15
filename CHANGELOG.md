# Changelog

All notable changes to the PDF Applicant Info Extractor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-15

### 🎉 Major Refactor - Complete Architecture Overhaul

This release represents a complete restructuring of the codebase with improved organization, security, and maintainability.

### Added

#### Backend Structure

- ✨ **Modular Architecture**: Organized backend into logical modules
  - `backend/api/` - API route definitions
  - `backend/config/` - Centralized configuration management
  - `backend/services/` - Business logic services
  - `backend/utils/` - Utility functions and validators
- 🔧 **Configuration Management**

  - Centralized settings in `backend/config/settings.py`
  - Environment-based configuration
  - Settings validation on startup
  - Comprehensive `.env` support

- 🛠️ **Service Layer**
  - `PDFProcessor` - PDF text extraction and token counting
  - `LLMService` - LLM interactions (direct and RAG)
  - `PDFGenerator` - PDF report generation
- 🔒 **Enhanced Security**
  - File validation utilities
  - MIME type checking with python-magic
  - Configurable file size limits
  - Proper error handling

#### Developer Experience

- 📜 **Startup Scripts**

  - `scripts/start-backend.sh` - Backend startup (Unix/Mac)
  - `scripts/start-backend.bat` - Backend startup (Windows)
  - `scripts/start-frontend.sh` - Frontend startup
  - `scripts/start-all.sh` - Start both services

- 🐳 **Docker Support**
  - `Dockerfile` - Production-ready container
  - `docker-compose.yml` - Full stack deployment
  - `.dockerignore` - Optimized build context

#### Documentation

- 📚 **Comprehensive Docs**
  - Enhanced `README.md` with new structure
  - `QUICKSTART.md` - 5-minute setup guide
  - `SECURITY.md` - Security best practices
  - `MIGRATION.md` - Migration guide from v1.0
  - `CHANGELOG.md` - This file
- 📖 **API Documentation**
  - Versioned API endpoints (`/api/v1/`)
  - Enhanced OpenAPI documentation
  - Root endpoint with API information

#### Configuration

- ⚙️ **Environment Variables**
  - Comprehensive `env.example` with all options
  - Configurable model parameters
  - RAG configuration options
  - Rate limiting settings (optional)
  - Output directory configuration

### Changed

#### Breaking Changes

- 🔄 **API Endpoints**: All endpoints now use `/api/v1/` prefix
  - `/process` → `/api/v1/process`
  - `/health` → `/api/v1/health`
- 🔄 **Server Startup**: New module path
  - Old: `uvicorn llm_report:app`
  - New: `uvicorn backend.main:app`

#### Improvements

- 🎯 **Code Organization**: Separated concerns for better maintainability
- 🚀 **Performance**: Optimized imports and service initialization
- 📦 **Dependencies**: Updated and organized `requirements.txt`
- 🎨 **Frontend**: Updated API endpoint in `app/page.tsx`
- 📝 **Logging**: Better error messages and status codes

### Fixed

- 🐛 Fixed missing `python-dotenv` in requirements
- 🐛 Fixed missing `fpdf` in requirements
- 🐛 Fixed deprecated langchain imports
- 🐛 Improved error handling for empty PDFs
- 🐛 Better validation for file uploads

### Security

- 🔒 Enhanced `.gitignore` to prevent sensitive file commits
- 🔒 Added file type validation beyond extensions
- 🔒 Implemented proper CORS configuration
- 🔒 Added comprehensive security documentation
- 🔒 Created secure configuration management

### Deprecated

- ⚠️ `llm_report.py` - Use new modular structure
- ⚠️ `llm_report_secure.py` - Functionality integrated into new structure
- ⚠️ `requirements-secure.txt` - Merged into main `requirements.txt`

## [1.0.0] - 2024-XX-XX

### Initial Release

#### Added

- Basic PDF text extraction
- OpenAI GPT-4 integration
- RAG support for large documents
- FastAPI backend
- Next.js frontend
- Basic file upload interface
- PDF report generation

#### Features

- Direct processing for small documents
- RAG processing for large documents
- Token counting
- CORS support
- Basic error handling

---

## Migration Guide

See [MIGRATION.md](MIGRATION.md) for detailed migration instructions from v1.0 to v2.0.

## Upgrade Instructions

### From v1.0 to v2.0

1. **Update API calls** to use new endpoint structure
2. **Update startup commands** to use new module path
3. **Create `.env` file** from `env.example`
4. **Update any custom integrations** to use new import paths
5. **Test thoroughly** before deploying to production

See [MIGRATION.md](MIGRATION.md) for complete details.

---

## Support

For questions or issues:

- 📚 Read the [README.md](README.md)
- 🚀 Check [QUICKSTART.md](QUICKSTART.md)
- 🔒 Review [SECURITY.md](SECURITY.md)
- 🐛 Open an issue on GitHub
