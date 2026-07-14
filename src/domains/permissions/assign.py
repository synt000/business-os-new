from pydantic import BaseModel


class PermissionAssign(BaseModel):
    role_name: str
    permission_id: int
