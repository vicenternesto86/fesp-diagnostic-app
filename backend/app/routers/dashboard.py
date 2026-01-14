"""
Dashboard Router
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.assessment import Assessment, AssessmentItem
from app.models.user import User
from app.schemas.dashboard import DashboardSummary, CompareResult
from app.utils.auth import get_current_user
from app.utils.calculations import (
    calculate_traffic_light, calculate_fesp_scores,
    calculate_capability_scores, calculate_policy_cycle_scores,
    calculate_gaps, calculate_overall_compliance
)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary/{assessment_id}", response_model=DashboardSummary)
def get_dashboard_summary(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard summary for a specific assessment"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Get items as dictionaries
    items = [
        {
            "fesp_id": item.fesp_id,
            "item_id": item.item_id,
            "score": item.score,
            "evidence_text": item.evidence_text,
            "notes": item.notes
        }
        for item in assessment.items
    ]
    
    # Calculate metrics
    total_compliance = calculate_overall_compliance(items)
    fesp_scores = calculate_fesp_scores(items)
    capability_scores = calculate_capability_scores(items)
    policy_cycle_scores = calculate_policy_cycle_scores(items)
    gaps = calculate_gaps(items)
    
    # Build unit name
    if assessment.level == "state":
        unit_name = assessment.state.name
    else:
        unit_name = f"{assessment.jurisdiction.name}, {assessment.state.name}"
    
    return DashboardSummary(
        assessment_id=assessment.id,
        unit_name=unit_name,
        level=assessment.level,
        cutoff_date=assessment.cutoff_date.isoformat(),
        total_compliance=total_compliance,
        traffic_light=calculate_traffic_light(total_compliance),
        gap_count=len([g for g in gaps if g["priority"] == "high"]),
        fesp_scores=fesp_scores,
        capability_scores=capability_scores,
        policy_cycle_scores=policy_cycle_scores,
        gaps=gaps
    )


@router.get("/latest")
def get_latest_assessment(
    state_id: int,
    jurisdiction_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the most recent completed assessment for a unit"""
    query = db.query(Assessment).filter(
        Assessment.state_id == state_id,
        Assessment.status == "completed"
    )
    
    if jurisdiction_id:
        query = query.filter(Assessment.jurisdiction_id == jurisdiction_id)
    else:
        query = query.filter(Assessment.level == "state")
    
    assessment = query.order_by(Assessment.cutoff_date.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No hay evaluaciones completadas")
    
    return get_dashboard_summary(assessment.id, db, current_user)


@router.get("/compare", response_model=CompareResult)
def compare_assessments(
    assessment_id_1: int,
    assessment_id_2: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compare two assessments side by side"""
    summary1 = get_dashboard_summary(assessment_id_1, db, current_user)
    summary2 = get_dashboard_summary(assessment_id_2, db, current_user)
    
    return CompareResult(unit1=summary1, unit2=summary2)


@router.get("/history")
def get_assessment_history(
    state_id: int,
    jurisdiction_id: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get historical assessments for trend analysis"""
    query = db.query(Assessment).filter(
        Assessment.state_id == state_id,
        Assessment.status == "completed"
    )
    
    if jurisdiction_id:
        query = query.filter(Assessment.jurisdiction_id == jurisdiction_id)
    else:
        query = query.filter(Assessment.level == "state")
    
    assessments = query.order_by(Assessment.cutoff_date.desc()).limit(limit).all()
    
    history = []
    for assessment in assessments:
        items = [
            {
                "fesp_id": item.fesp_id, 
                "item_id": item.item_id, 
                "score": item.score
            }
            for item in assessment.items
        ]
        
        compliance = calculate_overall_compliance(items)
        fesp_scores = calculate_fesp_scores(items)
        
        history.append({
            "assessment_id": assessment.id,
            "cutoff_date": assessment.cutoff_date.isoformat(),
            "total_compliance": compliance,
            "traffic_light": calculate_traffic_light(compliance),
            "fesp_scores": {f["fesp_id"]: f["compliance_percentage"] for f in fesp_scores}
        })
    
    return history
