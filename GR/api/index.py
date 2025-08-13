from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
import requests
from io import StringIO

app = FastAPI()

# URL pública da planilha em formato CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/10uW600iHgIkN33_coO5XkZ16TxewmsG5BvxqEtyrCgE/export?format=csv&gid=234741149"

# Mapeamento de cores para status
COLOR_MAP = {
    "verde": "Aprovado",
    "amarelo": "Em análise",
    "vermelho": "Reprovado",
    "laranja": "Pendência de documento"
}

@app.get("/")
def root():
    return {"status": "API de análise de risco está no ar!"}

@app.get("/buscar")
def buscar_status(nome: str = Query(..., description="Nome completo para busca")):
    try:
        # Baixa a planilha
        r = requests.get(CSV_URL)
        r.raise_for_status()

        # Carrega no pandas
        df = pd.read_csv(StringIO(r.text))

        # Garantir que colunas tenham nomes consistentes
        df.columns = [c.strip() for c in df.columns]

        # Procura pelo nome exato (case insensitive)
        linha = df[df["Nome Completo"].str.lower() == nome.lower()]

        if linha.empty:
            return JSONResponse(content={"erro": "Nome não encontrado"}, status_code=404)

        status_texto = linha.iloc[0]["STATUS DA ANALISE"]
        service = linha.iloc[0]["Service de atuação"]
        cor_detectada = None

        # Detectar a cor pelo texto (se tiver indicação no texto)
        for cor, descricao in COLOR_MAP.items():
            if cor.lower() in status_texto.lower():
                cor_detectada = cor
                status_legivel = f"{descricao} >> {status_texto}"
                break

        if cor_detectada is None:
            status_legivel = status_texto

        return {
            "nome": nome,
            "status": status_legivel,
            "service": service
        }

    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
