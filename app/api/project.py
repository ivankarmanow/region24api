from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, SuperAdmin
from app.model.db import Project as ProjectDB, Feature, ProjectMedia
from app.model.schema.project import Project, ProjectIn
from app.response import APIResponse

project = APIRouter(tags=["project"], prefix="/project")


@project.get("/list")
async def project_list(session: SessionDep) -> list[Project]:
    projects = session.scalars(select(ProjectDB)).all()
    return projects


@project.post("/create")
async def create_project(session: SessionDep, project: ProjectIn, admin: SuperAdmin) -> APIResponse:
    dump = project.model_dump(exclude={"features", "media"})
    dump["features"] = [Feature(feature=i) for i in project.features]
    dump["media"] = [ProjectMedia(image=i.image, is_main=i.is_main) for i in project.media]
    session.add(ProjectDB(**dump))
    session.commit()
    return APIResponse()


@project.put("/edit")
async def edit_project(session: SessionDep, project_id: int, project: ProjectIn, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ProjectDB, project_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.model_dump().items():
        if key == "features":
            old_obj.features = [Feature(feature=i) for i in value]
        else:
            setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@project.delete("/delete")
async def delete(session: SessionDep, project_id: int, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ProjectDB, project_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@project.get("/{id}")
async def project_get(session: SessionDep, id: int) -> Project:
    project = session.get(ProjectDB, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
