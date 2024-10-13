from core.app import app
from stab.routes import router as stab_router

app.include_router(stab_router, prefix="", tags=["stab"])
