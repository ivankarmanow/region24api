from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, SuperAdmin
from app.model.db import Project as ProjectDB, ProjectCategory as ProjectCategoryDB
from app.model.schema.project import Project, ProjectIn, ProjectCategory, ProjectCategoryList, \
    ProjectCategoryIn
from app.response import APIResponse

project = APIRouter(tags=["project"], prefix="/project")
category = APIRouter(prefix="/category")


@project.get("/list")
async def project_list(session: SessionDep) -> list[Project]:
    projects = session.scalars(select(ProjectDB)).all()
    return projects


@project.post("/create")
async def create_project(session: SessionDep, project: ProjectIn, admin: SuperAdmin) -> APIResponse:
    session.add(ProjectDB(**project.model_dump()))
    session.commit()
    return APIResponse()


@project.put("/edit")
async def edit_project(session: SessionDep, project_id: int, project: ProjectIn, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ProjectDB, project_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.model_dump().items():
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


@category.get("/list")
async def category_list(session: SessionDep) -> list[ProjectCategory]:
    categories = session.scalars(select(ProjectCategoryDB)).all()
    return categories


@category.post("/create")
async def category_create(session: SessionDep, category: ProjectCategoryIn, admin: SuperAdmin) -> APIResponse:
    session.add(ProjectCategoryDB(**category.model_dump()))
    session.commit()
    return APIResponse()


@category.put("/edit")
async def edit_category(
    session: SessionDep, category_id: int, category: ProjectCategoryIn, admin: SuperAdmin
    ) -> APIResponse:
    old_obj = session.get(ProjectCategoryDB, category_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Project category not found")
    for key, value in category.model_dump().items():
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@category.delete("/delete")
async def delete(session: SessionDep, category_id: int, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ProjectCategoryDB, category_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Project category not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@category.get("/{id}")
async def category_get(session: SessionDep, id: int) -> ProjectCategoryList:
    category = session.get(ProjectCategoryDB, id)
    if not category:
        raise HTTPException(status_code=404, detail="Project category not found")
    return category
