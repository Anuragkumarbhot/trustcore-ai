# TRUSTCORE AI

**Authorized defensive cybersecurity, IT monitoring, intelligence, and security-assessment platform.**

## MVP Foundation

This repository contains the core foundation:

- FastAPI application
- JWT authentication
- Role-Based Access Control (RBAC)
- Capability registry
- Provider adapter interface
- Audit logging
- PostgreSQL/SQLite database support
- pytest test suite

## Quick Start (Termux / Linux)

1. Create virtual environment and install dependencies (see Termux Setup Commands).
2. Copy `.env.example` to `.env` and adjust settings (use SQLite for local dev).
3. Initialize database:
   ```bash
   python -c "from app.database import init_db; init_db()" 