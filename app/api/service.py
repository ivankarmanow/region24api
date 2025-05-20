from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, SuperAdmin
from app.model.db import Service as ServiceDB, ServiceCategory as ServiceCategoryDB
from app.model.schema.service.core import Service, ServiceIn, ServiceCategory, ServiceCategoryList, \
    ServiceCategoryIn
from app.model.schema.service.depends import ServiceList
from app.response import APIResponse

service = APIRouter(tags=["service"], prefix="/service")
category = APIRouter(prefix="/category")


@service.get("/list")
async def service_list(session: SessionDep) -> list[Service]:
    services = session.scalars(select(ServiceDB)).all()
    return services


@service.post("/create")
async def create_service(session: SessionDep, service: ServiceIn, admin: SuperAdmin) -> APIResponse:
    session.add(ServiceDB(**service.model_dump()))
    session.commit()
    return APIResponse()


@service.put("/edit")
async def edit_service(session: SessionDep, service_id: int, service: ServiceIn, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ServiceDB, service_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    for key, value in service.model_dump().items():
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@service.delete("/delete")
async def delete(session: SessionDep, service_id: int, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ServiceDB, service_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@service.get("/{id}")
async def service_get(session: SessionDep, id: int) -> ServiceList:
    service = session.get(ServiceDB, id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@category.get("/list")
async def category_list(session: SessionDep) -> list[ServiceCategory]:
    categories = session.scalars(select(ServiceCategoryDB)).all()
    return categories


@category.post("/create")
async def category_create(session: SessionDep, category: ServiceCategoryIn, admin: SuperAdmin) -> APIResponse:
    session.add(ServiceCategoryDB(**category.model_dump()))
    session.commit()
    return APIResponse()


@category.put("/edit")
async def edit_category(
    session: SessionDep, category_id: int, category: ServiceCategoryIn, admin: SuperAdmin
    ) -> APIResponse:
    old_obj = session.get(ServiceCategoryDB, category_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Service category not found")
    for key, value in category.model_dump().items():
        setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@category.delete("/delete")
async def delete(session: SessionDep, category_id: int, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ServiceCategoryDB, category_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Service category not found")
    session.delete(old_obj)
    session.commit()
    return APIResponse()


@category.get("/{id}")
async def category_get(session: SessionDep, id: int) -> ServiceCategoryList:
    category = session.get(ServiceCategoryDB, id)
    if not category:
        raise HTTPException(status_code=404, detail="Service category not found")
    return category
