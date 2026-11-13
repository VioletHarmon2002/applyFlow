from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_conn, create_schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_schema()
    yield

app = FastAPI(lifespan=lifespan)

#initializing db
#CORS. The javaScript frontend could send requests to the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ #who is allowed access?
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False, #This is a setting for requests with credentials, such as authorization cookies.
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)



#basemodel to know whcih info is going to be send

#Validates the data sent by JavaScript
class Application(BaseModel):
    company:str
    position:str
    status:str
    
#Validated data from db
class ApplicationDB(Application): #inherits 3 fileds from Application and adds 2 more
    id:UUID
    created_at:datetime

#GET
@app.get("/applications", response_model=list[ApplicationDB]) #response_model which data is gonna be send back to js
def get_application():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM applications;")
        return cur.fetchall()


#POST
@app.post("/applications", response_model = ApplicationDB)
def post_application(application: Application):#what api recieves from js, what js sends to api
    with get_conn() as conn, conn.cursor() as cur: #cur execute What Python sends to PostgreSQL
            cur.execute(""" 
            INSERT INTO applications (company,position,status)
            VALUES (%s, %s, %s)
            RETURNING *;
            """,
            (application.company, application.position, application.status)
            )
            return cur.fetchone() #Python returns the row to FastAPI, which can send it to JavaScript as JSON.

#DELETE 
@app.delete("/applications/{id}", status_code= 204 ) #HTTP 204 No Content means the deletion succeeded, and there's no response body.
def delete_application(id: UUID):
    with get_conn() as conn, conn.cursor() as cur: #RETURNING returns data from PostgreSQL back to your Python backend (FastAPI)
        cur.execute("""
        DELETE from applications WHERE id=%s RETURNING id; 
          """,
          (id, )
        )
        deleted = cur.fetchone() #gets the row
        if deleted is None:
            raise HTTPException(
                status_code= 404,
                detail="application not found"

            )
            
#PUT(EDIT)
@app.put("/applications/{id}", response_model= ApplicationDB)
def put_application(id: UUID, application: Application):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
        UPDATE applications
        SET company = %s,
            position = %s,
            status = %s
        WHERE id = %s
        RETURNING *;   
        """,
        (
          application.company,
          application.position,
          application.status,
          id

        )
    )
        updated = cur.fetchone()
        if updated is None:
          raise HTTPException(
            status_code=404,
            detail="no such application"
        )
        return updated



