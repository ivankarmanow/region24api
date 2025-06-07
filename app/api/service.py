from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import SessionDep, SuperAdmin
from app.model.db import Service as ServiceDB, Advantage, Stage
from app.model.schema.service.core import Service, ServiceIn
from app.model.schema.service.depends import ServiceList
from app.response import APIResponse

service = APIRouter(tags=["service"], prefix="/service")


@service.get("/list")
async def service_list(session: SessionDep) -> list[Service]:
    services = session.scalars(select(ServiceDB)).all()
    # result = [Service(
    #     id=service.id,
    #     title=service.title,
    #     description=service.description,
    #     image=service.image,
    #     stages=[i.stage for i in service.stages],
    #     advantages=[i.advantage for i in service.advantages],
    # ) for service in services]
    return services


@service.post("/create")
async def create_service(session: SessionDep, service: ServiceIn, admin: SuperAdmin) -> APIResponse:
    advs = [Advantage(advantage=i) for i in service.advantages]
    stages = [Stage(stage=i) for i in service.stages]
    dump = service.model_dump()
    dump["stages"] = stages
    dump["advantages"] = advs
    session.add(ServiceDB(**dump))
    session.commit()
    return APIResponse()


@service.put("/edit")
async def edit_service(session: SessionDep, service_id: int, service: ServiceIn, admin: SuperAdmin) -> APIResponse:
    old_obj = session.get(ServiceDB, service_id)
    if not old_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    for key, value in service.model_dump().items():
        if key == "stages":
            old_obj.stages = [Stage(stage=i) for i in value]
        elif key == "advantages":
            old_obj.advantages = [Advantage(advantage=i) for i in value]
        else:
            setattr(old_obj, key, value)
    session.add(old_obj)
    session.commit()
    return APIResponse()


@service.delete("/delete")
async def delete_service(session: SessionDep, service_id: int, admin: SuperAdmin) -> APIResponse:
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
