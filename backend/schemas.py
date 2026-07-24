from datetime import datetime
from pydantic import BaseModel, HttpUrl, field_validator


class LinkCreate(BaseModel):
    original_url: HttpUrl
    custom_code: str | None = None

    @field_validator("custom_code")
    @classmethod
    def code_is_url_safe(cls, v):
        if v is not None:
            if not v.isalnum() or len(v) > 16:
                raise ValueError(
                    "custom_code must be alphanumeric and at most 16 characters"
                )
        return v


class LinkOut(BaseModel):
    code: str
    original_url: str
    created_at: datetime
    click_count: int

    class Config:
        from_attributes = True
