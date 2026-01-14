"""
Jurisdiction Model
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Jurisdiction(Base):
    __tablename__ = "jurisdictions"
    
    id = Column(Integer, primary_key=True, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False)  # e.g., "J1", "J2"
    active = Column(Boolean, default=True)
    
    # Relationships
    state = relationship("State", back_populates="jurisdictions")
    users = relationship("User", back_populates="jurisdiction")
    assessments = relationship("Assessment", back_populates="jurisdiction")
