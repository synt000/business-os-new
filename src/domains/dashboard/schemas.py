from pydantic import BaseModel


class DashboardMenuResponse(BaseModel):

    feature_code: str
    menu_name: str
    menu_icon: str | None
    route_path: str

    class Config:
        from_attributes = True
