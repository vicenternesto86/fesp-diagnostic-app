"""
States Router - Open Access (No Authentication)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.state import State
from app.schemas.state import StateCreate, StateResponse, StateUpdate

router = APIRouter(prefix="/api/states", tags=["Estados"])


@router.get("/", response_model=List[StateResponse])
def list_states(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all states"""
    query = db.query(State)
    if active_only:
        query = query.filter(State.active == True)
    return query.order_by(State.name).all()


@router.get("/{state_id}", response_model=StateResponse)
def get_state(
    state_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific state"""
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return state


@router.post("/", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
def create_state(
    state_data: StateCreate,
    db: Session = Depends(get_db)
):
    """Create a new state"""
    existing = db.query(State).filter(
        (State.name == state_data.name) | (State.code == state_data.code)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Estado ya existe con ese nombre o código")
    
    state = State(**state_data.model_dump())
    db.add(state)
    db.commit()
    db.refresh(state)
    return state


@router.put("/{state_id}", response_model=StateResponse)
def update_state(
    state_id: int,
    state_data: StateUpdate,
    db: Session = Depends(get_db)
):
    """Update a state"""
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    
    for field, value in state_data.model_dump(exclude_unset=True).items():
        setattr(state, field, value)
    
    db.commit()
    db.refresh(state)
    return state


@router.delete("/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_state(
    state_id: int,
    db: Session = Depends(get_db)
):
    """Delete a state"""
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    
    db.delete(state)
    db.commit()
