"""
Assessment Schemas
"""
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, datetime


class AssessmentItemBase(BaseModel):
    fesp_id: str
    item_id: str
    score: int = 0
    evidence_text: Optional[str] = None
    evidence_url: Optional[str] = None
    notes: Optional[str] = None
    
    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        if v < 0 or v > 5:
            raise ValueError('score must be between 0 and 5')
        return v


class AssessmentItemCreate(AssessmentItemBase):
    pass


class AssessmentItemUpdate(BaseModel):
    score: Optional[int] = None
    evidence_text: Optional[str] = None
    evidence_url: Optional[str] = None
    notes: Optional[str] = None


class AssessmentItemResponse(AssessmentItemBase):
    id: int
    assessment_id: int
    
    class Config:
        from_attributes = True


class AssessmentBase(BaseModel):
    level: str  # "state" or "jurisdiction"
    state_id: int
    jurisdiction_id: Optional[int] = None
    cutoff_date: date
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v):
        if v not in ['state', 'jurisdiction']:
            raise ValueError('level must be state or jurisdiction')
        return v


class AssessmentCreate(AssessmentBase):
    items: Optional[List[AssessmentItemCreate]] = None


class AssessmentUpdate(BaseModel):
    cutoff_date: Optional[date] = None
    status: Optional[str] = None
    items: Optional[List[AssessmentItemCreate]] = None


class AssessmentResponse(AssessmentBase):
    id: int
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssessmentWithItems(AssessmentResponse):
    items: List[AssessmentItemResponse] = []
    state_name: Optional[str] = None
    jurisdiction_name: Optional[str] = None
