from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

SHEET_ID = "10uW600iHgIkN33_coO5XkZ16TxewmsG5BvxqEtyrCgE"
GID = "234741149"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def cor_status(status):
    s = str(status).lower()
    if "aprovado" in s:
        return "#4CAF50"
    elif "em analise" in s or "em análise" in s:
        return "#FFD700"
    elif "reprovado" in s:
        return "#FF0000"
    elif "pendente" in s or "ileg" in s or "vencida" in s:
        return "#FF8C00"
    else:
        return "#D3D3D3"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, nome: str = None):
    # read CSV from Google Sheets export
    df = pd.read_csv(CSV_URL)
    resultado = None
    if nome:
        resultado = df[df['Nome Completo'].str.lower() == nome.strip().lower()].to_dict(orient="records")
        if resultado:
            for r in resultado:
                r["cor"] = cor_status(r.get("STATUS DA ANALISE", ""))
    return templates.TemplateResponse("index.html", {"request": request, "resultado": resultado})
