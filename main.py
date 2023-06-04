from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import pandas as pd
import requests
import toml
from dotenv import dotenv_values
import json

# Problem trying to solve:
# News lacks context and trends. 
# See news across idealogies.
# News without ads and tracking

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# Read in the config files
config = toml.load("config.toml")
env = dotenv_values(".env")

# Set the app title from the config file
app_name = config["app"]["name"]
version = config["app"]["version"]

# ms = media stack
msk = env["MEDIASTACK_KEY"]

ms_sources = "http://api.mediastack.com/v1/sources"
ms_live_news = "http://api.mediastack.com/v1/news"

ms_sources_payload = {'access_key': msk, 'search': 'cnn', 'countries': 'us', 'languages': 'en'}
ms_live_news_payload = {'access_key': msk, 'countries': 'us', 'languages': 'en', 'categories', ['-sports', -'entertainment']}

async def index(request: Request):

    # Create a functions that requests json from media stack url http://api.mediastack.com/v1/sources?access_key = YOUR_ACCESS_KEY
    news = requests.get(ms_live_news, payload=ms_sources_payload)
    df = pd.DataFrame.from_dict(news['data']) 
    return templates.TemplateResponse("index.html", {"request": request})
