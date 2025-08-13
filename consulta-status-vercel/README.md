Projeto: Consulta de Status (pronto para deploy na Vercel)
Arquivos incluídos:
- api/index.py        (FastAPI backend que lê CSV export do Google Sheets)
- templates/index.html (Interface de busca)
- requirements.txt
- vercel.json

Como subir na Vercel:
1. Instale vercel CLI: npm i -g vercel
2. Faça login: vercel login
3. No diretório do projeto, rode: vercel
4. Confirme deploy.

Observações:
- A planilha precisa estar pública para leitura (qualquer pessoa com o link).
- Se preferir usar credenciais em vez de CSV público, me avise que adapto o index.py.
