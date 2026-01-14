"""
Assessments Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.assessment import Assessment, AssessmentItem
from app.fesp_items import FESP_ITEMS, get_all_items
from app.models.state import State
from app.models.jurisdiction import Jurisdiction
from app.models.user import User
from app.schemas.assessment import (
    AssessmentCreate, AssessmentUpdate, AssessmentResponse, 
    AssessmentWithItems, AssessmentItemCreate
)
from app.utils.auth import get_current_user, require_writer

router = APIRouter(prefix="/api/assessments", tags=["Evaluaciones"])


def check_user_permission(user: User, state_id: int, jurisdiction_id: Optional[int]) -> bool:
    """Check if user has permission to access/modify this assessment"""
    if user.role == "admin":
        return True
    
    # Writers can only access their assigned state/jurisdiction
    if user.role == "writer":
        if user.state_id and user.state_id != state_id:
            return False
        if user.jurisdiction_id and jurisdiction_id and user.jurisdiction_id != jurisdiction_id:
            return False
    
    return True


@router.get("/", response_model=List[AssessmentResponse])
def list_assessments(
    state_id: Optional[int] = None,
    jurisdiction_id: Optional[int] = None,
    level: Optional[str] = None,
    status_filter: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List assessments with filters"""
    query = db.query(Assessment)
    
    # Apply filters
    if state_id:
        query = query.filter(Assessment.state_id == state_id)
    if jurisdiction_id:
        query = query.filter(Assessment.jurisdiction_id == jurisdiction_id)
    if level:
        query = query.filter(Assessment.level == level)
    if status_filter:
        query = query.filter(Assessment.status == status_filter)
    if from_date:
        query = query.filter(Assessment.cutoff_date >= from_date)
    if to_date:
        query = query.filter(Assessment.cutoff_date <= to_date)
    
    # Non-admin users can only see their assigned state/jurisdiction
    if current_user.role != "admin":
        if current_user.state_id:
            query = query.filter(Assessment.state_id == current_user.state_id)
        if current_user.jurisdiction_id:
            query = query.filter(Assessment.jurisdiction_id == current_user.jurisdiction_id)
    
    return query.order_by(Assessment.cutoff_date.desc()).all()


@router.get("/{assessment_id}", response_model=AssessmentWithItems)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get assessment with all items"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    if not check_user_permission(current_user, assessment.state_id, assessment.jurisdiction_id):
        raise HTTPException(status_code=403, detail="No tiene permiso para ver esta evaluación")
    
    # Build response with state/jurisdiction names
    result = AssessmentWithItems.model_validate(assessment)
    result.state_name = assessment.state.name if assessment.state else None
    result.jurisdiction_name = assessment.jurisdiction.name if assessment.jurisdiction else None
    
    return result


@router.post("/", response_model=AssessmentWithItems, status_code=status.HTTP_201_CREATED)
def create_assessment(
    data: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_writer)
):
    """Create a new assessment with items"""
    # Verify state exists
    state = db.query(State).filter(State.id == data.state_id).first()
    if not state:
        raise HTTPException(status_code=400, detail="Estado no existe")
    
    # Verify jurisdiction if level is jurisdiction
    if data.level == "jurisdiction":
        if not data.jurisdiction_id:
            raise HTTPException(status_code=400, detail="Se requiere jurisdicción para nivel 'jurisdiction'")
        jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.id == data.jurisdiction_id).first()
        if not jurisdiction:
            raise HTTPException(status_code=400, detail="Jurisdicción no existe")
    
    # Check permission
    if not check_user_permission(current_user, data.state_id, data.jurisdiction_id):
        raise HTTPException(status_code=403, detail="No tiene permiso para crear evaluaciones en esta unidad")
    
    # Create assessment
    assessment = Assessment(
        level=data.level,
        state_id=data.state_id,
        jurisdiction_id=data.jurisdiction_id,
        cutoff_date=data.cutoff_date,
        status="draft",
        created_by=current_user.id
    )
    db.add(assessment)
    db.flush()  # Get the ID
    
    # Create items (either from input or default empty)
    if data.items:
        for item_data in data.items:
            item = AssessmentItem(
                assessment_id=assessment.id,
                **item_data.model_dump()
            )
            db.add(item)
    else:
        # Create default items for all 43 FESP items
        for item_def in get_all_items():
            item = AssessmentItem(
                assessment_id=assessment.id,
                fesp_id=item_def["fesp_id"],
                item_id=item_def["id"],
                score=0
            )
            db.add(item)
    
    db.commit()
    db.refresh(assessment)
    
    result = AssessmentWithItems.model_validate(assessment)
    result.state_name = assessment.state.name
    result.jurisdiction_name = assessment.jurisdiction.name if assessment.jurisdiction else None
    
    return result


@router.put("/{assessment_id}", response_model=AssessmentWithItems)
def update_assessment(
    assessment_id: int,
    data: AssessmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_writer)
):
    """Update assessment and its items"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    if not check_user_permission(current_user, assessment.state_id, assessment.jurisdiction_id):
        raise HTTPException(status_code=403, detail="No tiene permiso para modificar esta evaluación")
    
    # Update basic fields
    if data.cutoff_date:
        assessment.cutoff_date = data.cutoff_date
    if data.status:
        assessment.status = data.status
    
    # Update items if provided
    if data.items:
        # Remove existing items
        db.query(AssessmentItem).filter(AssessmentItem.assessment_id == assessment_id).delete()
        
        # Add new items
        for item_data in data.items:
            item = AssessmentItem(
                assessment_id=assessment.id,
                **item_data.model_dump()
            )
            db.add(item)
    
    db.commit()
    db.refresh(assessment)
    
    result = AssessmentWithItems.model_validate(assessment)
    result.state_name = assessment.state.name
    result.jurisdiction_name = assessment.jurisdiction.name if assessment.jurisdiction else None
    
    return result


@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_writer)
):
    """Delete an assessment"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Only admin can delete
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar evaluaciones")
    
    db.delete(assessment)
    db.commit()


@router.get("/fesp-items/definition")
def get_fesp_items():
    """Get FESP items definition"""
    return FESP_ITEMS
