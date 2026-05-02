from __future__ import annotations

import hashlib
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models.blueprint import Blueprint
from app.db.models.project import Project
from app.db.session import get_db

router = APIRouter()


class BlueprintCreate(BaseModel):
    project_id: int
    name: str
    file_path: Optional[str] = None
    content: Optional[str] = None


def _blueprint_dict(b: Blueprint) -> dict:
    return {
        "id": b.id,
        "project_id": b.project_id,
        "name": b.name,
        "file_path": b.file_path,
        "content_hash": b.content_hash,
        "created_at": b.created_at.isoformat(),
    }


@router.post("/blueprints", status_code=201)
def create_blueprint(body: BlueprintCreate, db: Session = Depends(get_db)) -> dict:
    project = db.get(Project, body.project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project {body.project_id} not found")

    content_hash = (
        hashlib.sha256(body.content.encode()).hexdigest() if body.content else None
    )
    blueprint = Blueprint(
        project_id=body.project_id,
        name=body.name,
        file_path=body.file_path,
        content_hash=content_hash,
    )
    db.add(blueprint)
    db.commit()
    db.refresh(blueprint)
    return _blueprint_dict(blueprint)


@router.get("/blueprints")
def list_blueprints(
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> dict:
    q = db.query(Blueprint)
    if project_id is not None:
        q = q.filter(Blueprint.project_id == project_id)
    blueprints = q.order_by(Blueprint.created_at.desc()).all()
    return {"blueprints": [_blueprint_dict(b) for b in blueprints]}


@router.get("/blueprints/{blueprint_id}")
def get_blueprint(blueprint_id: int, db: Session = Depends(get_db)) -> dict:
    blueprint = db.get(Blueprint, blueprint_id)
    if blueprint is None:
        raise HTTPException(status_code=404, detail=f"Blueprint {blueprint_id} not found")
    return _blueprint_dict(blueprint)
