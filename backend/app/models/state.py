"""
State Model
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class State(Base):
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(5), unique=True, nullable=False)  # e.g., "TAM", "NL"
    active = Column(Boolean, default=True)
    
    # Relationships
    jurisdictions = relationship("Jurisdiction", back_populates="state")
    users = relationship("User", back_populates="state")
    assessments = relationship("Assessment", back_populates="state")
