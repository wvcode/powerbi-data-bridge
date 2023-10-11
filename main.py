import os
from fastapi.responses import StreamingResponse
import uvicorn
import traceback
import time
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI()

# Adicionando middleware para habilitar o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

valid_apikeys = ["R1NtQVIyMDIz", "UEVSU09OQUw="]
keys = {"R1NtQVIyMDIz": "GTMART", "UEVSU09OQUw=": "PERSONAL"}


def stream_data(url, apk, tbl_name):
    resultados = []
    supabase: Client = create_client(url, apk)
    tbl = supabase.table(tbl_name).select("*").execute()
    i = 0
    for item in tbl.data:
        resultados.append(item)
    return resultados


@app.get("/")
def default():
    result = "The API is UP!"
    return result


@app.get("/retrieve/{tbl_name}")
def read_data(tbl_name: str, apikey: str):
    try:
        if apikey in valid_apikeys:
            url = os.getenv(f"{keys[apikey]}_SUPABASE_URL")
            apk = os.getenv(f"{keys[apikey]}_SUPABASE_KEY")
            dados = stream_data(url, apk, tbl_name)
            return dados
        else:
            raise HTTPException(status_code=500, detail="Invalid APIKEY.")
    except:
        print(traceback.format_exc())
        raise HTTPException(status_code=404, detail="No data found.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
