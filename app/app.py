from fastapi import FastAPI, HTTPException

from app.api import admin, admin_auth, client, contact, history, order, project, request, service, upload, auth
from app.error import exception_handler, http_exception_handler

app = FastAPI(title="Region24 API", summary="API веб-сайта Регион24", version="0.1.0", swagger_ui_parameters = {"docExpansion":"none"})

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, exception_handler)

admin.include_router(admin_auth)
app.include_router(admin)
app.include_router(auth)
app.include_router(client)
app.include_router(contact)
app.include_router(history)
app.include_router(order)
app.include_router(project)
app.include_router(request)
app.include_router(service)
app.include_router(upload)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=1342)
