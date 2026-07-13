from pydantic import BaseModel


class BusinessProfileCreate(BaseModel):

    business_name: str
    logo_url: str | None = None
    phone: str | None = None
    address: str | None = None
    description: str | None = None



class SocialAccountCreate(BaseModel):

    platform: str
    account_name: str | None = None
    account_url: str | None = None



class SocialAccountResponse(BaseModel):

    id: str
    platform: str
    account_name: str | None
    account_url: str | None
    status: str


    class Config:
        from_attributes = True
