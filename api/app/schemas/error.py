from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: int
    message: str


class ErrorResponse(BaseModel):
    erreur: ErrorDetail