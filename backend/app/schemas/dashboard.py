"""
Dashboard Schemas
"""
from pydantic import BaseModel
from typing import List, Optional


class FESPScore(BaseModel):
    fesp_id: str
    fesp_name: str
    fesp_number: int
    earned_points: float
    max_points: float
    compliance_percentage: float
    level: str
    color: str


class CapabilityScore(BaseModel):
    capability: str
    earned_points: float
    max_points: float
    compliance_percentage: float
    level: str
    color: str


class PolicyCycleScore(BaseModel):
    cycle: str
    earned_points: float
    max_points: float
    compliance_percentage: float
    level: str
    color: str


class GapItem(BaseModel):
    item_id: str
    item_name: str
    fesp_id: str
    score: float
    max_points: float
    percentage: float
    priority: str  # "high", "medium"
    recommendation: str


class DashboardSummary(BaseModel):
    assessment_id: int
    unit_name: str
    level: str
    cutoff_date: str
    total_compliance: float
    traffic_light: str
    gap_count: int
    fesp_scores: List[FESPScore]
    capability_scores: List[CapabilityScore]
    policy_cycle_scores: List[PolicyCycleScore]
    gaps: List[GapItem]


class CompareResult(BaseModel):
    unit1: DashboardSummary
    unit2: DashboardSummary
