# Security Policy

## 🔒 Security Overview

This document outlines the security considerations and best practices for the LLM PDF Applicant Info Extractor project.

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainers directly (add your email here)
3. Include detailed information about the vulnerability
4. Allow reasonable time for a fix before public disclosure

We take security seriously and will respond promptly to security reports.

## ⚠️ Current Security Considerations

### Development vs Production

This repository contains two versions of the backend:

1. **`llm_report.py`** - Development version with relaxed security for easy testing
2. **`llm_report_secure.py`** - Production-ready version with enhanced security

### Known Security Issues in Development Version

The `llm_report.py` file contains the following security considerations:

#### 1. CORS Configuration

```python
# ⚠️ DEVELOPMENT ONLY
allow_origins=["*"]  # Allows requests from any origin
```

**Risk**: Any website can make requests to your API  
**Production Fix**: Use specific origins in `llm_report_secure.py`

#### 2. No File Size Limits

**Risk**: Large files could cause denial of service  
**Production Fix**: 10MB limit enforced in secure version

#### 3. No File Type Validation

**Risk**: Malicious files could be processed  
**Production Fix**: MIME type validation in secure version

#### 4. No Rate Limiting

**Risk**: API abuse and excessive OpenAI costs  
**Production Fix**: Implement rate limiting middleware

#### 5. Output Files Saved to Disk

**Risk**: Sensitive data persists on server  
**Production Fix**: Use temporary files or in-memory processing

## ✅ Security Features in Production Version

### 1. CORS Protection

```python
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
allow_origins=ALLOWED_ORIGINS
```

### 2. File Validation

- Maximum file size: 10MB
- MIME type verification using python-magic
- Extension validation
- Content validation

### 3. Input Sanitization

- Proper error handling
- Type validation
- Empty document detection

### 4. Environment Variables

- API keys stored in `.env` (not in code)
- `.env` excluded from git via `.gitignore`
- Example configuration in `env.example`

### 5. Error Handling

- Proper HTTP status codes
- No sensitive information in error messages
- Graceful failure handling

## 🔐 Production Deployment Checklist

Before deploying to production, ensure you complete ALL items:

### Required

- [ ] Use `llm_report_secure.py` instead of `llm_report.py`
- [ ] Set `ALLOWED_ORIGINS` to your actual domain(s)
- [ ] Use HTTPS (never HTTP in production)
- [ ] Set up proper environment variables
- [ ] Never commit `.env` file to git
- [ ] Use strong, unique API keys
- [ ] Set up monitoring and logging

### Recommended

- [ ] Implement rate limiting (e.g., using `slowapi`)
- [ ] Add authentication/authorization if handling sensitive data
- [ ] Set up automated security scanning
- [ ] Implement request logging
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Configure firewall rules
- [ ] Use a reverse proxy (nginx/Apache)
- [ ] Implement request size limits at proxy level
- [ ] Set up automated backups
- [ ] Create incident response plan

### Optional (Enhanced Security)

- [ ] Implement API key rotation
- [ ] Add request signing
- [ ] Use Web Application Firewall (WAF)
- [ ] Implement IP whitelisting
- [ ] Add honeypot endpoints
- [ ] Set up intrusion detection
- [ ] Implement audit logging
- [ ] Use secrets management service (e.g., AWS Secrets Manager)

## 🛡️ Best Practices

### API Key Management

1. **Never commit API keys to git**

   ```bash
   # Check if .env is in .gitignore
   grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
   ```

2. **Use environment-specific keys**

   - Development: Limited quota, test key
   - Production: Full quota, monitored key

3. **Rotate keys regularly**

   - Set calendar reminders
   - Rotate every 90 days minimum
   - Rotate immediately if compromised

4. **Monitor API usage**
   - Set up billing alerts in OpenAI dashboard
   - Monitor for unusual patterns
   - Set usage limits

### File Upload Security

1. **Validate file types**

   ```python
   # Don't trust file extensions alone
   # Use MIME type detection (python-magic)
   ```

2. **Limit file sizes**

   ```python
   MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
   ```

3. **Scan for malware** (if handling untrusted files)

   - Consider using ClamAV or similar
   - Implement in production environment

4. **Don't store files permanently**
   - Process and delete immediately
   - Use temporary directories
   - Implement cleanup jobs

### CORS Configuration

Development:

```python
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

Production:

```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

Never use in production:

```python
allow_origins=["*"]  # ❌ NEVER DO THIS IN PRODUCTION
```

### Rate Limiting

Example using `slowapi`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/process")
@limiter.limit("5/minute")  # 5 requests per minute
async def process_pdf(request: Request, file: UploadFile = File(...)):
    # ... implementation
```

## 🔍 Security Monitoring

### What to Monitor

1. **API Usage**

   - Request frequency
   - Failed authentication attempts
   - Unusual patterns

2. **OpenAI Costs**

   - Token usage
   - Cost per request
   - Unexpected spikes

3. **Error Rates**

   - 4xx errors (client errors)
   - 5xx errors (server errors)
   - Validation failures

4. **File Uploads**
   - File sizes
   - File types
   - Processing times

### Logging Best Practices

```python
import logging

# Don't log sensitive data
logger.info(f"Processing file: {file.filename}")  # ✅ OK
logger.info(f"API Key: {api_key}")  # ❌ NEVER DO THIS

# Log security events
logger.warning(f"Invalid file type attempted: {mime_type}")
logger.error(f"File size exceeded: {file_size} bytes")
```

## 🚀 Deployment Security

### Environment Variables

Production `.env`:

```env
# Required
OPENAI_API_KEY=sk-prod-xxxxxxxxxxxxx
ALLOWED_ORIGINS=https://yourdomain.com

# Optional but recommended
MAX_FILE_SIZE=10485760
MAX_TOKENS=4000
LOG_LEVEL=INFO
```

### HTTPS Configuration

Always use HTTPS in production. Example nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📦 Dependency Security

### Keep Dependencies Updated

```bash
# Check for outdated packages
pip list --outdated

# Update packages
pip install --upgrade package-name

# Check for security vulnerabilities
pip-audit
```

### Pin Versions

Always pin versions in `requirements.txt`:

```
fastapi==0.104.1  # ✅ Good
fastapi>=0.104.1  # ⚠️ Risky
fastapi           # ❌ Bad
```

## 🧪 Security Testing

### Automated Testing

1. **Dependency scanning**: Use `pip-audit` or `safety`
2. **Static analysis**: Use `bandit` for Python security issues
3. **SAST**: Integrate with GitHub Security or similar
4. **Container scanning**: If using Docker

### Manual Testing

Test these scenarios:

- [ ] Upload non-PDF file
- [ ] Upload oversized file
- [ ] Upload empty file
- [ ] Upload malformed PDF
- [ ] Send requests from unauthorized origin
- [ ] Send malformed requests
- [ ] Test rate limiting
- [ ] Test error handling

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## 📝 Version History

- **v1.0.0** - Initial security documentation
- Added production-ready secure version
- Documented all known security considerations

---

**Remember**: Security is an ongoing process, not a one-time setup. Regularly review and update security measures.
