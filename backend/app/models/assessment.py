"""
Assessment and AssessmentItem Models
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # "state" or "jurisdiction"
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    jurisdiction_id = Column(Integer, ForeignKey("jurisdictions.id"), nullable=True)
    cutoff_date = Column(Date, nullable=False)
    status = Column(String(20), default="draft")  # "draft" or "completed"
    
    # Audit fields
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    state = relationship("State", back_populates="assessments")
    jurisdiction = relationship("Jurisdiction", back_populates="assessments")
    created_by_user = relationship("User", back_populates="assessments")
    items = relationship("AssessmentItem", back_populates="assessment", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint("level IN ('state', 'jurisdiction')", name="check_level"),
        CheckConstraint("status IN ('draft', 'completed')", name="check_status"),
    )


class AssessmentItem(Base):
    __tablename__ = "assessment_items"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    fesp_id = Column(String(20), nullable=False)  # e.g., "fesp_1"
    item_id = Column(String(50), nullable=False)  # e.g., "fesp_1_1"
    score = Column(Integer, nullable=False, default=0)  # 0-5
    evidence_text = Column(Text, nullable=True)
    evidence_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationship
    assessment = relationship("Assessment", back_populates="items")
    
    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 5", name="check_score"),
    )


# Item definitions are now in app/fesp_items.py
