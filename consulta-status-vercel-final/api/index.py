from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import requests
from io import StringIO

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# URL pública da planilha em formato CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/10uW600iHgIkN33_coO5XkZ16TxewmsG5BvxqEtyrCgE/export?format=csv&gid=234741149"

def carregar_planilha():
    r = requests.get(CSV_URL, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    # Normaliza nomes de colunas (tira espaços extras)
    df.columns = [str(c).strip() for c in df.columns]
    # Garante que as colunas esperadas existem
    esperadas = ["Nome Completo", "STATUS DA ANALISE", "Service de atuação"]
    faltando = [c for c in esperadas if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes na planilha: {{faltando}}. Colunas encontradas: {{list(df.columns)}}")
    return df

def categorizar_cor(status_texto: str):
    s = str(status_texto or "").lower()
    # Mapas por prioridade
    if "aprovado" in s:
        return "verde", "Aprovado"
    if "reprovado" in s:
        return "vermelho", "Reprovado"
    if "em analise" in s or "em análise" in s:
        return "amarelo", "Em análise"
    # Qualquer pendência/documento/ilegível/vencido vai para laranja
    if any(p in s for p in ["pend", "ileg", "vencid", "cnh", "crlv", "doc"]):
        return "laranja", "Pendência de documento"
    # Padrão: cinza sem categoria
    return "cinza", "Indefinido"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Renderiza uma página simples com formulário
    return templates.TemplateResponse("index.html", {{"request": request}})

@app.get("/buscar")
def buscar_status(nome: str = Query(..., description="Nome completo para busca (exato)")):
    try:
        df = carregar_planilha()
        linha = df[df["Nome Completo"].str.lower() == nome.strip().lower()]
        if linha.empty:
            return JSONResponse(content={{"erro": "Nome não encontrado"}}, status_code=404)

        registro = linha.iloc[0]
        status_original = str(registro["STATUS DA ANALISE"])
        cor, categoria = categorizar_cor(status_original)
        exibicao = f"{{categoria}} >> {{status_original}}" if categoria != "Indefinido" else status_original

        return {{
            "nome": str(registro["Nome Completo"]),
            "service": str(registro["Service de atuação"]),
            "status_original": status_original,
            "status_cor": cor,
            "status_categoria": categoria,
            "status_exibicao": exibicao
        }}
    except Exception as e:
        return JSONResponse(content={{"erro": str(e)}}, status_code=500)
