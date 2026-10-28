import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {"pool_pre_ping": True})

@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTO_INCREMENT, title VARCHAR(200) NOT NULL, done BOOLEAN NOT NULL DEFAULT FALSE)" if not DATABASE_URL.startswith("sqlite") else "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(200) NOT NULL, done BOOLEAN NOT NULL DEFAULT 0)"))
    yield

app = FastAPI(title="CI/CD Task API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")], allow_methods=["GET", "POST", "PATCH"], allow_headers=["Content-Type"])

class TaskInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(text("SELECT id, title, done FROM tasks ORDER BY id DESC")).mappings()]

@app.post("/tasks", status_code=201)
def add_task(payload: TaskInput):
    with engine.begin() as conn:
        result = conn.execute(text("INSERT INTO tasks (title, done) VALUES (:title, 0)"), {"title": payload.title})
        task_id = result.lastrowid
    return {"id": task_id, "title": payload.title, "done": False}

@app.patch("/tasks/{task_id}")
def finish_task(task_id: int):
    with engine.begin() as conn:
        result = conn.execute(text("UPDATE tasks SET done = 1 WHERE id = :id"), {"id": task_id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "done": True}
