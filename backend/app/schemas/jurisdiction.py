"""
Jurisdiction Schemas
"""
from pydantic import BaseModel
from typing import Optional


class JurisdictionBase(BaseModel):
    state_id: int
    name: str
    code: str
    active: bool = True


class JurisdictionCreate(JurisdictionBase):
    pass


class JurisdictionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    active: Optional[bool] = None


class JurisdictionResponse(JurisdictionBase):
    id: int
    
    class Config:
        from_attributes = True
