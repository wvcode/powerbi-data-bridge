import os
import uvicorn
import traceback
import math

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


def stream_data(url, apk, tbl_name, page, page_size, order_column):
    resultados = []
    supabase: Client = create_client(url, apk)
    start = (page - 1) * page_size

    if page_size == 0:
        tbl = supabase.table(tbl_name).select("*").execute()
        records = tbl.data
    else:
        tbl = supabase.table(tbl_name).select("*").order(order_column).execute()
        records = tbl.data[start : (start + page_size)]

    if page_size == 0:
        return records
    else:
        return {
            "page": page,
            "total_records": len(tbl.data),
            "total_pages": math.ceil(len(tbl.data) / page_size) if page_size > 0 else 1,
            "records_on_this_page": len(records),
            "data": records,
        }


@app.get("/")
def default():
    result = "The API is UP!"
    return result


@app.get("/retrieve_page/{tbl_name}")
def read_data(tbl_name: str, apikey: str, page: int = 1, order_column: str = "1"):
    page_size = 100
    try:
        if apikey in valid_apikeys:
            url = os.getenv(f"{keys[apikey]}_SUPABASE_URL")
            apk = os.getenv(f"{keys[apikey]}_SUPABASE_KEY")
            dados = stream_data(url, apk, tbl_name, page, page_size, order_column)
            return dados
        else:
            raise HTTPException(status_code=500, detail="Invalid APIKEY.")
    except:
        print(traceback.format_exc())
        raise HTTPException(status_code=404, detail="No data found.")


@app.get("/retrieve/{tbl_name}")
def read_data(tbl_name: str, apikey: str):
    try:
        if apikey in valid_apikeys:
            url = os.getenv(f"{keys[apikey]}_SUPABASE_URL")
            apk = os.getenv(f"{keys[apikey]}_SUPABASE_KEY")
            dados = stream_data(url, apk, tbl_name, 1, 0, "1")
            return dados
        else:
            raise HTTPException(status_code=500, detail="Invalid APIKEY.")
    except:
        print(traceback.format_exc())
        raise HTTPException(status_code=404, detail="No data found.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
