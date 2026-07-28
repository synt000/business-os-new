from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel


class WelcomeResponse(BaseModel):

    language: str

    title: Optional[str] = None
    subtitle: Optional[str] = None
    hero_message: Optional[str] = None

    faq_content: Optional[str] = None

    features_json: Optional[list] = None
    button_text: Optional[str] = None

    live_banner: Optional[str] = None
    banner_active: bool = True

    logo_url: Optional[str] = None
    hero_image_url: Optional[str] = None

    theme_color: str = "#2563eb"

    seo_title: Optional[str] = None
    seo_description: Optional[str] = None

    sections_json: Optional[List[Any]] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


    class Config:
        from_attributes = True



class WelcomeUpdate(BaseModel):

    language: str = "mm"

    title: str = "Business OS"
    subtitle: str = ""
    hero_message: str = ""

    faq_content: str = ""

    features_json: list = []
    button_text: str = "Continue"

    live_banner: str = "Welcome to Business OS"
    banner_active: bool = True

    logo_url: str = ""
    hero_image_url: str = ""

    theme_color: str = "#2563eb"

    seo_title: str = ""
    seo_description: str = ""

    sections_json: List[Any] = []
