# Backend Python

Este diretório contém a aplicação FastAPI (`api.py`) e suas dependências.

## Executar localmente

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
backend/.venv/bin/uvicorn backend.api:app --reload
```

Com o serviço em execução, acesse `http://127.0.0.1:8000/docs` para a
documentação interativa e `http://127.0.0.1:8000/health` para a verificação de
saúde.

## Testar

```bash
backend/.venv/bin/pip install -r backend/requirements-dev.txt
backend/.venv/bin/pytest -q
```
