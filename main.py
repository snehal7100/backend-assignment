from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, auth
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

VALID_STATUS = ["not_started", "in_progress", "completed"]

# ---------------- AUTH ----------------

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = auth.hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

@app.post("/login")
def login(user: schemas.Login, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(400, "Invalid credentials")
    token = auth.create_token({"user_id": db_user.id})
    return {"access_token": token}

# ---------------- USERS ----------------

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# ---------------- TASKS ----------------

@app.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    if task.status not in VALID_STATUS:
        raise HTTPException(400, "Invalid status")

    user = db.query(models.User).get(task.assigned_to)
    if not user:
        raise HTTPException(404, "User not found")

    new_task = models.Task(**task.dict(), created_by=1)
    db.add(new_task)
    db.commit()
    return {"msg": "Task created"}

@app.get("/tasks")
def get_tasks(status: str = None, assigned_to: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)
    if assigned_to:
        query = query.filter(models.Task.assigned_to == assigned_to)

    return query.all()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).get(task_id)
    if not db_task:
        raise HTTPException(404, "Task not found")

    for key, value in task.dict().items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.utcnow()
    db.commit()
    return {"msg": "Updated"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).get(task_id)
    if not db_task:
        raise HTTPException(404, "Task not found")

    db.delete(db_task)
    db.commit()
    return {"msg": "Deleted"}

# ---------------- MOVE TASK (JIRA LOGIC) ----------------

@app.post("/move-task")
def move_task(data: schemas.MoveTask, db: Session = Depends(get_db)):
    if data.new_status not in VALID_STATUS:
        raise HTTPException(400, "Invalid status")

    task = db.query(models.Task).get(data.task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    task.status = data.new_status
    task.position = data.new_position
    db.commit()

    return {"msg": "Task moved"}

# ---------------- DASHBOARD ----------------

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.status == "completed").count()
    in_progress = db.query(models.Task).filter(models.Task.status == "in_progress").count()

    return {
        "total_tasks": total,
        "completed": completed,
        "in_progress": in_progress,
        "completion_percentage": (completed / total * 100) if total else 0
    }