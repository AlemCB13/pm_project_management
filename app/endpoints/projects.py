from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
import httpx

router = APIRouter()
API_GATEWAY_URL = "http://pm_api_gateway:8000"

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/projects/")
async def create_project(project: schemas.ProjectCreate):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_GATEWAY_URL}/api/users/{project.owner_id}")
        if response.raise_for_status != 200:
            raise HTTPException(status_code=404, detail="User not found")
        # Crear el proyecto
        project_data = {
            "name": project.name,
            "description": project.description,
            "owner_id": project.owner_id,
        }
        response = await client.post(f"{API_GATEWAY_URL}/api/projects", json=project_data)
        return response.json()

# @router.post("/projects/", response_model=schemas.Project)
# def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
#     db_project = models.Project(**project.dict())
#     db.add(db_project)
#     db.commit()
#     db.refresh(db_project)
#     return db_project

@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project