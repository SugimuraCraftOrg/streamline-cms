from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from core.settings import get_app_settings
from core.constants import SERVERS

app = FastAPI()
app.openapi_schema = None

app_settings = get_app_settings()

# CORS settings.
# see: https://fastapi.tiangolo.com/ja/tutorial/cors/#corsmiddleware
cors_origins = app_settings.cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# OpenAPI settings.
# see: https://fastapi.tiangolo.com/ja/how-to/extending-openapi/?h=get_openapi#overriding-the-defaults
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Streamline CMS",
        version="0.0.1",
        description="The simple and intuitive headless CMS.",
        routes=app.routes,
    )
    openapi_schema["servers"] = SERVERS
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
