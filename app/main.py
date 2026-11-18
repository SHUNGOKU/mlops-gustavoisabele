"""API de classificação de spam.

Para rodar:  uvicorn app.main:app --reload
O contrato da API está no README.md.
"""
import os
from pathlib import Path
from typing import Optional

import joblib
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# --- Configuração (vem de variáveis de ambiente, nunca escrita no código) ---
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")
APP_ENV = os.getenv("APP_ENV", "dev")
API_KEY = os.getenv("API_KEY")  # se vazia, o /predict não exige chave
MODEL_PATH = Path(
    os.getenv("MODEL_PATH", str(Path(__file__).resolve().parent.parent / "model" / "modelo.joblib"))
)
WEB_DIR = Path(__file__).resolve().parent.parent / "front"

# --- Modelo: carregado uma vez, quando a API inicia ---
modelo = joblib.load(MODEL_PATH)

app = FastAPI(title="API de classificação de spam")


class Mensagem(BaseModel):
    texto: str = Field(min_length=1, max_length=2000)


def verificar_chave(x_api_key: Optional[str] = Header(default=None)):
    """Se API_KEY estiver definida, exige o cabeçalho X-API-Key igual a ela."""
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="chave de API inválida ou ausente")


@app.get("/health")
def health():
    return {"status": "ok", "versao": MODEL_VERSION, "ambiente": APP_ENV}


@app.post("/predict", dependencies=[Depends(verificar_chave)])
def predict(msg: Mensagem):
    texto = msg.texto.strip()
    if not texto:
        raise HTTPException(status_code=422, detail="o texto não pode ser vazio")

    probabilidades = modelo.predict_proba([texto])[0]
    indice = probabilidades.argmax()
    return {
        "rotulo": str(modelo.classes_[indice]),
        "probabilidade": round(float(probabilidades[indice]), 2),
        "versao": MODEL_VERSION,
    }


# --- Página web: servida pela própria API (sem CORS) ---
# Fica por último para não "engolir" as rotas acima.
if WEB_DIR.is_dir():
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="front")
