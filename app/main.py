from fastapi import FastAPI
from app.endpoints import projects

app = FastAPI()

# Incluye los endpoints de proyectos
app.include_router(projects.router)

@app.get("/")
def read_root():
    return {"message": "Project Management Microservice"}