# Collab Machine

Mobile-first control plane for a Google Colab GPU runtime running Ollama.

## Structure

- frontend: mobile-first web/PWA shell
- backend: FastAPI API
- colab: runtime bootstrap
- .github/workflows: CI

The Colab API is beta and allowlist-based. The integration is isolated so the project can run in mock mode until access is enabled.

## Local backend

python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload

Never commit real Google OAuth credentials or tokens.

## Roadmap

Google OAuth -> Colab runtime lifecycle -> Jupyter bootstrap -> Ollama streaming -> model management -> MCP.
