# Consulta de Status — Deploy Vercel (FastAPI)

Este projeto lê sua planilha **Análise de Risco - MELI** diretamente via CSV público do Google Sheets e expõe:

- **GET /** → página HTML com formulário de busca
- **GET /buscar?nome=...** → JSON com Nome, Service e Status (cor + categoria + texto original)

## Configurar
A planilha precisa estar acessível publicamente (qualquer pessoa com o link).
URL CSV usada:
https://docs.google.com/spreadsheets/d/10uW600iHgIkN33_coO5XkZ16TxewmsG5BvxqEtyrCgE/export?format=csv&gid=234741149

## Rodar localmente
```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
# abra: http://127.0.0.1:8000
```

## Deploy na Vercel
```bash
npm i -g vercel
vercel login
vercel
```
