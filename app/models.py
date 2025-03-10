from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Relación con usuarios

    # Relación (opcional, si necesitas acceder a los usuarios desde proyectos)
    owner = relationship("User", back_populates="projects")