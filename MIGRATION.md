# 🔄 Migration Guide

## Migrating from Old Structure to New Structure

This document helps you transition from the old flat file structure to the new modular architecture.

## What Changed?

### Old Structure (v1.0)

```
LLM-Sumamry-Transcript/
├── llm_report.py          # All code in one file
├── llm_report_secure.py   # Secure version in one file
├── requirements.txt
└── ...
```

### New Structure (v2.0)

```
LLM-Sumamry-Transcript/
├── backend/               # Organized backend
│   ├── api/              # API routes
│   ├── config/           # Configuration
│   ├── services/         # Business logic
│   ├── utils/            # Utilities
│   └── main.py           # Entry point
├── scripts/              # Startup scripts
└── ...
```

## Key Changes

### 1. API Endpoint URLs

**Old:**

```
POST http://127.0.0.1:8000/process
GET  http://127.0.0.1:8000/health  (secure version only)
```

**New:**

```
POST http://127.0.0.1:8000/api/v1/process
GET  http://127.0.0.1:8000/api/v1/health
GET  http://127.0.0.1:8000/  (root info)
```

### 2. Starting the Server

**Old:**

```bash
uvicorn llm_report:app --reload
# or
uvicorn llm_report_secure:app --reload
```

**New:**

```bash
uvicorn backend.main:app --reload
# or use the script
./scripts/start-backend.sh
```

### 3. Environment Configuration

**Old:**

- Manual environment variable setup
- Hardcoded values in code

**New:**

- Centralized configuration in `backend/config/settings.py`
- All settings configurable via `.env`
- Validation on startup

### 4. Code Organization

**Old:**

- All code in single file
- Mixed concerns (validation, processing, API)

**New:**

- Modular architecture
- Separated concerns:
  - `api/routes.py` - API endpoints
  - `services/` - Business logic
  - `utils/` - Helper functions
  - `config/` - Configuration

## Migration Steps

### For Developers

1. **Update your imports** (if you were importing from the old files):

   ```python
   # Old
   from llm_report import process_pdf

   # New
   from backend.api.routes import process_pdf
   ```

2. **Update API calls** in your frontend or client code:

   ```javascript
   // Old
   fetch('http://127.0.0.1:8000/process', ...)

   // New
   fetch('http://127.0.0.1:8000/api/v1/process', ...)
   ```

3. **Update startup commands**:

   ```bash
   # Old
   uvicorn llm_report:app --reload

   # New
   uvicorn backend.main:app --reload
   # or
   ./scripts/start-backend.sh
   ```

### For Deployment

1. **Update your Dockerfile** (if you had a custom one):

   ```dockerfile
   # Old
   CMD ["uvicorn", "llm_report:app", "--host", "0.0.0.0"]

   # New
   CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
   ```

2. **Update environment variables**:

   - Copy `env.example` to `.env`
   - Add all required variables
   - Remove old environment setup

3. **Update CI/CD pipelines**:

   ```yaml
   # Old
   run: uvicorn llm_report:app

   # New
   run: uvicorn backend.main:app
   ```

## Benefits of New Structure

### ✅ Better Organization

- Clear separation of concerns
- Easier to navigate codebase
- Logical grouping of related code

### ✅ Improved Maintainability

- Smaller, focused modules
- Easier to test individual components
- Reduced code duplication

### ✅ Enhanced Security

- Centralized validation
- Consistent error handling
- Better configuration management

### ✅ Easier Development

- Startup scripts for quick development
- Docker support for consistent environments
- Better documentation

### ✅ Scalability

- Easy to add new endpoints
- Simple to extend functionality
- Modular services can be separated later

## Backward Compatibility

The old files (`llm_report.py` and `llm_report_secure.py`) are still in the repository for reference but should not be used. They will be removed in a future version.

### Deprecation Timeline

- **v2.0** (Current): Old files present but deprecated
- **v2.1** (Next): Old files moved to `legacy/` folder
- **v3.0** (Future): Old files removed completely

## Testing Your Migration

1. **Test the health endpoint**:

   ```bash
   curl http://127.0.0.1:8000/api/v1/health
   ```

   Expected response:

   ```json
   { "status": "healthy", "service": "pdf-extractor" }
   ```

2. **Test file upload**:

   ```bash
   curl -X POST "http://127.0.0.1:8000/api/v1/process" \
     -F "file=@test.pdf"
   ```

3. **Check API documentation**:
   - Visit http://127.0.0.1:8000/docs
   - Verify all endpoints are listed
   - Test interactive API

## Common Issues

### Issue: Module not found errors

**Cause:** Running from wrong directory or missing `__init__.py` files

**Solution:**

```bash
# Make sure you're in the project root
cd LLM-Sumamry-Transcript

# Verify backend structure
ls backend/
# Should see: __init__.py, main.py, api/, config/, services/, utils/
```

### Issue: Import errors in backend modules

**Cause:** Python can't find the backend package

**Solution:**

```bash
# Make sure you're running from project root
pwd  # Should end with LLM-Sumamry-Transcript

# Run with proper module path
python -m uvicorn backend.main:app --reload
```

### Issue: Old API endpoints not working

**Cause:** Using old endpoint URLs

**Solution:** Update all API calls to use `/api/v1/` prefix:

- `/process` → `/api/v1/process`
- `/health` → `/api/v1/health`

## Need Help?

- 📚 Read the [README.md](README.md) for full documentation
- 🚀 Check [QUICKSTART.md](QUICKSTART.md) for setup guide
- 🔒 Review [SECURITY.md](SECURITY.md) for security info
- 🐛 Open an issue on GitHub if you encounter problems

---

**Migration completed? Delete this file or keep it for reference!**
