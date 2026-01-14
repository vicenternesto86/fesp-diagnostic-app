"""
State Schemas
"""
from pydantic import BaseModel
from typing import Optional


class StateBase(BaseModel):
    name: str
    code: str
    active: bool = True


class StateCreate(StateBase):
    pass


class StateUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    active: Optional[bool] = None


class StateResponse(StateBase):
    id: int
    
    class Config:
        from_attributes = True
