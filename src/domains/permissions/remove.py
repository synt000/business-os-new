from pydantic import BaseModel


class PermissionRemove(BaseModel):
    role_name: str
    permission_id: int
