import os
from fastapi.responses import StreamingResponse
import uvicorn
import traceback
import time
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

valid_apikeys = ["R1NtQVIyMDIz", "UEVSU09OQUw="]
keys = {"R1NtQVIyMDIz": "GTMART", "UEVSU09OQUw=": "PERSONAL"}


def stream_data(url, apk, tbl_name):
    supabase: Client = create_client(url, apk)
    tbl = supabase.table(tbl_name).select("*").execute()
    for item in tbl.data:
        yield json.dumps(item)


@app.get("/retrieve/{tbl_name}")
def read_produtos(tbl_name: str, apikey: str):
    try:
        if apikey in valid_apikeys:
            url = os.getenv(f"{keys[apikey]}_SUPABASE_URL")
            apk = os.getenv(f"{keys[apikey]}_SUPABASE_KEY")
            return StreamingResponse(stream_data(url, apk, tbl_name))
        else:
            raise HTTPException(status_code=500, detail="Invalid APIKEY.")
    except:
        print(traceback.format_exc())
        raise HTTPException(status_code=404, detail="No data found.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
