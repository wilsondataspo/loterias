from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse

from requests import get

from typing import Any, Dict

from bs4 import BeautifulSoup

from loterias_config import Config

from requests import get

from pymongo import errors
from app.funcoes_lotofacil import lotofacil, lotofacil_by_conc

from app.schemas import Result
from db import mongodb

app = FastAPI()
mongodb.install(app)

URL = Config.URL_LOTO


class ConcNotFoundException(Exception):
    pass
    

@app.exception_handler(ConcNotFoundException)
async def conc_not_found_handler(request: Request, exc: ConcNotFoundException):
    return JSONResponse(status_code=404, content={"message": "Concurso não encontrado"})



async def save_result(result: dict):
    app.db.insert_one(result)
    

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.get("/resultado_lotofacil/")
async def resultado_lotofacil():
    response = lotofacil(BeautifulSoup, get, URL)
    return response


@app.get("/resultado_lotofacil/{conc}", response_model=Result)
async def resultado_lotofacil_by_conc(conc: str = Path(default=Any, min_length=1, max_length=4)):
    resultado = app.db.find_one({"CONC": conc})
    #resultado = app.db.find({"CONC": conc})
    if not resultado:
        resultado = lotofacil_by_conc(BeautifulSoup, get, URL, conc)
        
        if "erro" in resultado:
            raise ConcNotFoundException()
            
        await save_result(resultado)
    
    return resultado