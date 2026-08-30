from typing import Annotated
from fastapi import Depends, FastAPI, Query, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from datetime import datetime

class Access_Key(SQLModel, table=True):
    rfid: str = Field(primary_key=True)
    privilege: str

    workers: list["Worker"] = Relationship(back_populates="access_key")

class Worker(SQLModel, table=True):
    id_worker: int = Field(primary_key=True)
    name: str
    surname: str
    role: str
    worker_key_rfid: str = Field(foreign_key="access_key.rfid")

    access_key: Access_Key = Relationship(back_populates="workers")

class Access_Gate(SQLModel, table=True):
    id_gate: int = Field(primary_key=True)
    location: str
    required_privilege: str

"""
class AccessHistory(SQLModel, table=True):
    id_history: int = Field(primary_key=True)
    attempt_time: datetime
    id_worker: int = Field(foreign_key="worker.id_worker")
    id_gate: int = Field(foreign_key="accessgate.id_gate")
    rfid: str = Field(foreign_key="accesskey.rfid")
    successful_access: bool

class SystemAccount(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password_hash: str
    account_worker_id: int = Field(foreign_key="worker.id_worker")
    privilege: str

class AccessGate(SQLModel, table=True):
    id_gate: int = Field(primary_key=True)
    location: str
    required_privilege: str
"""


postgresql_url = "postgresql://admin:admin@0.0.0.0:5432/rfid_system"
engine = create_engine(postgresql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def can_rfid_x_access_gate_y(rfid, gate):
    with Session(engine) as session:
        search_gate = select(Access_Gate).where(Access_Gate.id_gate == gate)
        gate_result = session.exec(search_gate)
        gate_one = gate_result.one_or_none()
        return gate_one.required_privilege
    
app = FastAPI()

@app.post("/workers")
def create_worker(worker: Worker, session: SessionDep) -> Worker:
    session.add(worker)
    session.commit()
    session.refresh(worker)
    return worker

@app.post("/accessgate")
def create_gate(accessgate: Access_Gate, session: SessionDep) -> Access_Gate:
    session.add(accessgate)
    session.commit()
    session.refresh(accessgate)
    return accessgate


"""
@app.post("/workers")
def create_worker(worker: Worker, session: SessionDep) -> Worker:
    session.add(worker)
    session.commit()
    session.refresh(worker)
    return worker

@app.get("/workers")
def read_worker(session: SessionDep, offset: int=0, limit: Annotated[int, Query(le=100)] = 100,) -> list [Worker]:
    workers = session.exec(select(Worker).offset(offset).limit(limit)).all()
    return workers

@app.delete("/workers/{worker_id}")
def delete_worker(worker_id: int, session: SessionDep):
    worker = session.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    session.delete(worker)
    session.commit()
    return {"ok": True}
"""

def main():
    print(can_rfid_x_access_gate_y("3qds", 1))

if __name__ == "__main__":
    main()

#TODO create full communication needed for edge layer to work