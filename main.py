

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

from database.mongo import MongodbConnectionHandler

from services.register import RegisterHandler
from services.authenticate import AuthenticationHandler

from models.person import Person

mongo_conn = MongodbConnectionHandler(db="rfid").connect()

registration_handler = RegisterHandler(mongo_conn, 'database')
authentication = AuthenticationHandler(mongo_conn)


app = FastAPI()


@app.get('/')
async def root():
    return{'welcome' : 'This is an API for a RFID Authentication System!', 'registrations': 0}

@app.get('/auth/{person_id}')
async def get_authentication(person_id):
    identity = authentication.authenticate(person_id)
    return identity

@app.get('/register/{person_id}/{person_name}')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
