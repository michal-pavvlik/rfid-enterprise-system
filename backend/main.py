from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine

class Worker(SQLModel, table=True):
    id_worker: int = Field(primary_key=True)
    name: str
    surname: str
    role: str
    worker_key_rfid: int

postgresql_url = "postgresql://admin:admin@0.0.0.0:5432/rfid_system"
engine = create_engine(postgresql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.post("/rfid-enterprise-system/workers")
def create_worker(worker: Worker, session: SessionDep) -> Worker:
    session.add(worker)
    session.commit()
    session.refresh(worker)
    return worker