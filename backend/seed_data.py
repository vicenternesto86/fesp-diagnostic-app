"""
Seed Data Script - Initialize database with sample data
"""
import sys
import os
# Add current directory to sys.path so 'app' can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.state import State
from app.models.jurisdiction import Jurisdiction
from app.models.assessment import Assessment, AssessmentItem
from app.fesp_items import FESP_ITEMS, get_all_items
from app.utils.auth import get_password_hash


def seed_database():
    """Seed the database with initial data"""
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Creating states...")
        states_data = [
            {"name": "Tamaulipas", "code": "TAM"},
            {"name": "Veracruz", "code": "VER"},
            {"name": "Coahuila", "code": "COA"},
            {"name": "Durango", "code": "DUR"},
            {"name": "Puebla", "code": "PUE"},
        ]
        states = []
        for s in states_data:
            state = State(**s)
            db.add(state)
            states.append(state)
        db.flush()
        
        print("Creating Distritos de Salud...")
        jurisdictions_data = [
            # Tamaulipas - 12 Distritos de Salud
            {"state_id": states[0].id, "name": "Distrito I - Victoria", "code": "D1"},
            {"state_id": states[0].id, "name": "Distrito II - Tampico", "code": "D2"},
            {"state_id": states[0].id, "name": "Distrito III - Matamoros", "code": "D3"},
            {"state_id": states[0].id, "name": "Distrito IV - Reynosa", "code": "D4"},
            {"state_id": states[0].id, "name": "Distrito V - Nuevo Laredo", "code": "D5"},
            {"state_id": states[0].id, "name": "Distrito VI - Mante", "code": "D6"},
            {"state_id": states[0].id, "name": "Distrito VII - San Fernando", "code": "D7"},
            {"state_id": states[0].id, "name": "Distrito VIII - Jaumave", "code": "D8"},
            {"state_id": states[0].id, "name": "Distrito IX - Miguel Alemán", "code": "D9"},
            {"state_id": states[0].id, "name": "Distrito X - Valle Hermoso", "code": "D10"},
            {"state_id": states[0].id, "name": "Distrito XI - Padilla", "code": "D11"},
            {"state_id": states[0].id, "name": "Distrito XII - Altamira", "code": "D12"},
        ]
        jurisdictions = []
        for j in jurisdictions_data:
            jurisdiction = Jurisdiction(**j)
            db.add(jurisdiction)
            jurisdictions.append(jurisdiction)
        db.flush()
        
        print("Creating users...")
        users_data = [
            {
                "name": "Administrador FESP",
                "email": "admin@fesp.gob.mx",
                "password": "Fesp_SNSP_2026",
                "role": "admin",
                "state_id": None,
                "jurisdiction_id": None
            },
            {
                "name": "Capturista Tamaulipas",
                "email": "captura.tam@fesp.gob.mx",
                "password": "Fesp_SNSP_2026",
                "role": "writer",
                "state_id": states[0].id,
                "jurisdiction_id": None
            },
            {
                "name": "Capturista J1 Nuevo Laredo",
                "email": "captura.j1@fesp.gob.mx",
                "password": "Fesp_SNSP_2026",
                "role": "writer",
                "state_id": states[0].id,
                "jurisdiction_id": jurisdictions[0].id
            },
            {
                "name": "Lector Tamaulipas",
                "email": "lector.tam@fesp.gob.mx",
                "password": "Fesp_SNSP_2026",
                "role": "reader",
                "state_id": states[0].id,
                "jurisdiction_id": None
            },
        ]
        users = []
        for u in users_data:
            user = User(
                name=u["name"],
                email=u["email"],
                password_hash=get_password_hash(u["password"]),
                role=u["role"],
                state_id=u.get("state_id"),
                jurisdiction_id=u.get("jurisdiction_id")
            )
            db.add(user)
            users.append(user)
        db.flush()
        
        print(f"Creating sample assessments with {len(get_all_items())} items...")
        
        # State-level assessment for Tamaulipas
        assessment1 = Assessment(
            level="state",
            state_id=states[0].id,
            jurisdiction_id=None,
            cutoff_date=date(2025, 12, 31),
            status="completed",
            created_by=users[1].id
        )
        db.add(assessment1)
        db.flush()
        
        # Sample scores for state assessment (mostly 3-5)
        import random
        random.seed(42)  # Deterministic sample
        
        for item_def in get_all_items():
            db.add(AssessmentItem(
                assessment_id=assessment1.id,
                fesp_id=item_def["fesp_id"],
                item_id=item_def["id"],
                score=random.choice([3, 4, 5]),
                evidence_text=f"Evidencia para {item_def['name']}",
                notes="Cumple satisfactoriamente"
            ))
        
        # Jurisdiction-level assessment
        assessment2 = Assessment(
            level="jurisdiction",
            state_id=states[0].id,
            jurisdiction_id=jurisdictions[0].id,
            cutoff_date=date(2025, 12, 31),
            status="completed",
            created_by=users[2].id
        )
        db.add(assessment2)
        db.flush()
        
        # Sample scores for jurisdiction (mostly 1-3 to show gaps)
        for item_def in get_all_items():
            db.add(AssessmentItem(
                assessment_id=assessment2.id,
                fesp_id=item_def["fesp_id"],
                item_id=item_def["id"],
                score=random.choice([1, 2, 3]),
                evidence_text=f"Evidencia limitada para {item_def['name']}",
                notes="Se requiere reforzar"
            ))
        
        # Draft assessment
        assessment3 = Assessment(
            level="jurisdiction",
            state_id=states[0].id,
            jurisdiction_id=jurisdictions[1].id,
            cutoff_date=date(2026, 1, 15),
            status="draft",
            created_by=users[1].id
        )
        db.add(assessment3)
        db.flush()
        
        # Empty items for draft
        for item_def in get_all_items():
            db.add(AssessmentItem(
                assessment_id=assessment3.id,
                fesp_id=item_def["fesp_id"],
                item_id=item_def["id"],
                score=0
            ))
        
        db.commit()
        print("=" * 50)
        print("Seed completed successfully!")
        print("=" * 50)
        print("\nTest users created:")
        print("  admin@fesp.gob.mx / Fesp_SNSP_2026 (Admin)")
        print("  captura.tam@fesp.gob.mx / Fesp_SNSP_2026 (Writer - State)")
        print("  captura.j1@fesp.gob.mx / Fesp_SNSP_2026 (Writer - Jurisdiction)")
        print("  lector.tam@fesp.gob.mx / Fesp_SNSP_2026 (Reader)")
        print("\nSample assessments created:")
        print("  - Tamaulipas State: Completed (Dec 2025)")
        print("  - Jurisdicción I Nuevo Laredo: Completed (Dec 2025)")
        print("  - Jurisdicción II Reynosa: Draft (Jan 2026)")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
