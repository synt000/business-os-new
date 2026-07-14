from pydantic import BaseModel


class PermissionCreate(BaseModel):
    code: str
    module: str
    description: str | None = None


class PermissionResponse(BaseModel):
    id: int
    code: str
    module: str
    description: str | None = None

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
