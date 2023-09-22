from fastapi import FastAPI
from .utils import ConnectionManager
import os
import uvicorn
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware
import dotenv
dotenv.load_dotenv()

app = FastAPI()

client = MongoClient(os.getenv('DATABASE'))
database = client["mindscapeqdb_staging"]

ConnectionManager.initialize()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

