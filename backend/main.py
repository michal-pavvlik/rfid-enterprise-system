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
    access_histories: list["Access_History"] | None = Relationship(back_populates="worker")
    system_account: "System_Account" = Relationship(back_populates="worker")

class Access_History(SQLModel, table=True):
    id_history: int = Field(primary_key=True)
    attempt_time: datetime
    id_worker: int = Field(foreign_key="worker.id_worker")
    id_gate: int = Field(foreign_key="access_gate.id_gate")
    rfid: str = Field(foreign_key="access_key.rfid")
    successful_access: bool

    worker: Worker = Relationship(back_populates="access_histories")
    access_gate: "Access_Gate" = Relationship(back_populates="access_histories")

class Access_Gate(SQLModel, table=True):
    id_gate: int = Field(primary_key=True)
    location: str
    required_privilege: str

    access_histories: list[Access_History] = Relationship(back_populates="access_gate")

class System_Account(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password_hash: str
    account_worker_id: int = Field(foreign_key="worker.id_worker")
    privilege: str

    worker: Worker = Relationship(back_populates="system_account")

postgresql_url = "postgresql://admin:admin@0.0.0.0:5432/rfid_system"
engine = create_engine(postgresql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def verify_key_to_gate_privileges(key_privilege, gate_req_privilege):
    flag_key_access = False
    if(key_privilege=="IT staff" and gate_req_privilege=="IT staff"):
        flag_key_access = True
    elif(key_privilege=="administration" and gate_req_privilege=="administration"):
        flag_key_access = True
    elif(gate_req_privilege=="default"):
        flag_key_access = True
    return flag_key_access
        
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

@app.get("/workers")
def read_worker(session: SessionDep, offset: int=0, limit: Annotated[int, Query(le=100)] = 100,) -> list [Worker]:
    workers = session.exec(select(Worker).offset(offset).limit(limit)).all()
    return workers

@app.get("/can_accesskey_enter_accessgate/")
def compare_accesskey_with_accessgate(session: SessionDep, key_rfid: str, gate_id: str):
    search_key = select(Access_Key).where(Access_Key.rfid == key_rfid)
    key_result = session.exec(search_key)
    key_one = key_result.one_or_none()
    search_gate = select(Access_Gate).where(Access_Gate.id_gate == gate_id)
    gate_result = session.exec(search_gate)
    gate_one = gate_result.one_or_none()
    return verify_key_to_gate_privileges(key_one.privilege, gate_one.required_privilege)

def main():
    print(can_rfid_x_access_gate_y("3qds", 1))

if __name__ == "__main__":
    main()

#TODO create full communication needed for edge layer to work