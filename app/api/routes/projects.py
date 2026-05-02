from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models.project import Project
from app.db.session import get_db

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    repo_path: Optional[str] = None
    repo_url: Optional[str] = None
    description: Optional[str] = None


def _project_dict(p: Project) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "repo_path": p.repo_path,
        "repo_url": p.repo_url,
        "description": p.description,
        "created_at": p.created_at.isoformat(),
    }


@router.post("/projects", status_code=201)
def create_project(body: ProjectCreate, db: Session = Depends(get_db)) -> dict:
    project = Project(
        name=body.name,
        repo_path=body.repo_path,
        repo_url=body.repo_url,
        description=body.description,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return _project_dict(project)


@router.get("/projects")
def list_projects(db: Session = Depends(get_db)) -> dict:
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return {"projects": [_project_dict(p) for p in projects]}


@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    return _project_dict(project)
