"""
Jurisdictions Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.jurisdiction import Jurisdiction
from app.models.state import State
from app.schemas.jurisdiction import JurisdictionCreate, JurisdictionResponse, JurisdictionUpdate
from app.utils.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter(prefix="/api/jurisdictions", tags=["Jurisdicciones"])


@router.get("/", response_model=List[JurisdictionResponse])
def list_jurisdictions(
    state_id: int = None,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List jurisdictions, optionally filtered by state"""
    query = db.query(Jurisdiction)
    if state_id:
        query = query.filter(Jurisdiction.state_id == state_id)
    if active_only:
        query = query.filter(Jurisdiction.active == True)
    return query.order_by(Jurisdiction.name).all()


@router.get("/by-state/{state_id}", response_model=List[JurisdictionResponse])
def list_by_state(
    state_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List jurisdictions for a specific state"""
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    
    return db.query(Jurisdiction).filter(
        Jurisdiction.state_id == state_id,
        Jurisdiction.active == True
    ).order_by(Jurisdiction.name).all()


@router.get("/{jurisdiction_id}", response_model=JurisdictionResponse)
def get_jurisdiction(
    jurisdiction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific jurisdiction"""
    jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.id == jurisdiction_id).first()
    if not jurisdiction:
        raise HTTPException(status_code=404, detail="Jurisdicción no encontrada")
    return jurisdiction


@router.post("/", response_model=JurisdictionResponse, status_code=status.HTTP_201_CREATED)
def create_jurisdiction(
    data: JurisdictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new jurisdiction (Admin only)"""
    # Verify state exists
    state = db.query(State).filter(State.id == data.state_id).first()
    if not state:
        raise HTTPException(status_code=400, detail="Estado no existe")
    
    jurisdiction = Jurisdiction(**data.model_dump())
    db.add(jurisdiction)
    db.commit()
    db.refresh(jurisdiction)
    return jurisdiction


@router.put("/{jurisdiction_id}", response_model=JurisdictionResponse)
def update_jurisdiction(
    jurisdiction_id: int,
    data: JurisdictionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a jurisdiction (Admin only)"""
    jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.id == jurisdiction_id).first()
    if not jurisdiction:
        raise HTTPException(status_code=404, detail="Jurisdicción no encontrada")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(jurisdiction, field, value)
    
    db.commit()
    db.refresh(jurisdiction)
    return jurisdiction


@router.delete("/{jurisdiction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jurisdiction(
    jurisdiction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a jurisdiction (Admin only)"""
    jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.id == jurisdiction_id).first()
    if not jurisdiction:
        raise HTTPException(status_code=404, detail="Jurisdicción no encontrada")
    
    db.delete(jurisdiction)
    db.commit()
