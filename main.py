import json
from pathlib import Path
import fastapi

from services import dentalink_service
from api import citas_api

app = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()

def configure_routing():
    app.include_router(citas_api.router)

def configure_api_keys():
    file = Path("settings.json").absolute()
    if not file.exists():
        print(f"WARNING: {file} file not found")
        raise Exception("settings.json file not found")

    with open("settings.json") as fin:
        settings = json.load(fin)
        dentalink_service.api_key = settings.get("api_key")


configure()
