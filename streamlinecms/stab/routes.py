from typing import Annotated

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
def get_items(
    name: Annotated[str | None, Query(description="The name for display.")] = "No Name",
):
    return {"name": name, "message": f"Hello, {name}!"}
