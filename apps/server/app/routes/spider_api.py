from fastapi import FastAPI,APIRouter

import requests
from bs4 import BeautifulSoup
import time
import random

app=APIRouter()
@app.post('/spider')
def spider(web_url:str):
    data=requests.get(web_url).text
    
    return data