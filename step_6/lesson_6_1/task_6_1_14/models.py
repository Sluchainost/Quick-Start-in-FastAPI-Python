"""Pydantic models for successful and error API responses."""

from pydantic import BaseModel


class ItemsResponse(BaseModel):
    """Response model for a successful /items/{item_id}/ request."""

    item_id: int


class CustomExceptionAModel(BaseModel):
    """Error response model for CustomExceptionA (e.g., 404 Not Found)."""

    status_code: int
    er_message: str
    er_details: str


class CustomExceptionBModel(BaseModel):
    """Error response model for CustomExceptionB (e.g., 403 Forbidden)."""

    status_code: int
    er_message: str
    er_details: str
