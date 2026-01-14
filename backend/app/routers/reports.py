"""
Reports Router - PDF and CSV Export for 11 FESP structure
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import io
import csv
from datetime import datetime

from app.database import get_db
from app.models.assessment import Assessment
from app.fesp_items import FESP_ITEMS, get_all_items
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.calculations import (
    calculate_traffic_light, calculate_fesp_scores,
    calculate_capability_scores, calculate_policy_cycle_scores,
    calculate_gaps, calculate_overall_compliance
)

router = APIRouter(prefix="/api/reports", tags=["Reportes"])


def generate_pdf_html(assessment: Assessment, summary: dict) -> str:
    """Generate HTML for PDF report"""
    
    # Compliance level colors
    colors = {
        "Inicial": "#FF4444",
        "Limitado": "#FF8C00",
        "Moderado": "#FFD700",
        "Intermedio": "#90EE90",
        "Avanzado": "#00C853"
    }
    
    # Build FESP table rows
    fesp_rows = ""
    for fesp in summary["fesp_scores"]:
        color = fesp["color"]
        fesp_rows += f"""
        <tr>
            <td style="font-weight: bold;">FESP {fesp['fesp_number']}</td>
            <td>{fesp['fesp_name']}</td>
            <td style="text-align: center;">{fesp['earned_points']} / {fesp['max_points']}</td>
            <td style="text-align: center; background-color: {color}; color: white; font-weight: bold;">
                {fesp['compliance_percentage']}%
            </td>
            <td style="text-align: center;">{fesp['level']}</td>
        </tr>
        """
    
    # Build gaps table
    gaps_rows = ""
    for gap in summary["gaps"]:
        priority_color = "#ef4444" if gap["priority"] == "high" else "#f59e0b"
        gaps_rows += f"""
        <tr>
            <td style="background-color: {priority_color}; color: white; text-align: center; font-weight: bold;">
                {gap['priority'].upper()}
            </td>
            <td>{gap['item_name']} (FESP {gap['fesp_id'].replace('fesp_', '')})</td>
            <td style="text-align: center;">{gap['score']} / {gap['max_points']}</td>
            <td>{gap['recommendation']}</td>
        </tr>
        """
    
    main_color = summary["traffic_light"]
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: letter;
                margin: 1.5cm;
            }}
            body {{
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.3;
                color: #1f2937;
            }}
            h1 {{
                color: #1e3a8a;
                border-bottom: 2px solid #1e3a8a;
                padding-bottom: 5px;
                margin-top: 20px;
            }}
            h2 {{
                color: #1e40af;
                margin-top: 15px;
            }}
            .cover {{
                text-align: center;
                padding: 80px 30px;
            }}
            .cover h1 {{
                font-size: 24pt;
                border: none;
            }}
            .summary-box {{
                background: #f8fafc;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border: 1px solid #e2e8f0;
            }}
            .score-badge {{
                display: inline-block;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 20pt;
                font-weight: bold;
                color: white;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
            }}
            th, td {{
                border: 1px solid #cbd5e1;
                padding: 6px;
                text-align: left;
                font-size: 8.5pt;
            }}
            th {{
                background: #1e3a8a;
                color: white;
            }}
            .page-break {{
                page-break-before: always;
            }}
        </style>
    </head>
    <body>
        <div class="cover">
            <h1>DIAGNÓSTICO BASAL FESP</h1>
            <h2>{summary['unit_name']}</h2>
            <p style="font-size: 14pt; margin-top: 30px;">
                Nivel de Evaluación: <strong>{summary['level'].upper()}</strong>
            </p>
            <p style="font-size: 12pt;">
                Fecha de Corte: {summary['cutoff_date']}
            </p>
            <div style="margin-top: 50px;">
                <p>Cumplimiento Global:</p>
                <span class="score-badge" style="background-color: {main_color};">
                    {summary['total_compliance']}%
                </span>
            </div>
            <p style="margin-top: 80px; font-size: 9pt; color: #64748b;">
                Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </p>
        </div>
        
        <div class="page-break">
            <h1>Resumen de Resultados por FESP</h1>
            <table>
                <thead>
                    <tr>
                        <th style="width: 60px;">FESP</th>
                        <th>Nombre de la Función Esencial</th>
                        <th style="width: 80px; text-align: center;">Puntos</th>
                        <th style="width: 90px; text-align: center;">% Cumplimiento</th>
                        <th style="width: 80px; text-align: center;">Nivel</th>
                    </tr>
                </thead>
                <tbody>
                    {fesp_rows}
                </tbody>
            </table>
            
            <div style="margin-top: 20px;">
                <h2>Análisis por Capacidad Institucional</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Capacidad</th>
                            <th style="text-align: center;">Puntos</th>
                            <th style="text-align: center;">%</th>
                            <th style="text-align: center;">Nivel</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'<tr><td>{c["capability"].capitalize()}</td><td style="text-align:center;">{c["earned_points"]}/{c["max_points"]}</td><td style="text-align:center; font-weight:bold; color:{c["color"]}">{c["compliance_percentage"]}%</td><td style="text-align:center;">{c["level"]}</td></tr>' for c in summary["capability_scores"]])}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="page-break">
            <h1>Identificación de Brechas y Recomendaciones</h1>
            {"<p>No se identificaron brechas críticas (cumplimiento superior al 60% en todos los ítems).</p>" if not gaps_rows else f'''
            <table>
                <thead>
                    <tr>
                        <th style="width: 70px;">Prioridad</th>
                        <th>Ítem con Oportunidad de Mejora</th>
                        <th style="width: 60px; text-align: center;">Puntaje</th>
                        <th>Recomendación de Fortalecimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {gaps_rows}
                </tbody>
            </table>
            '''}
            
            <div style="margin-top: 30px; background: #fffbeb; padding: 15px; border-left: 5px solid #f59e0b; font-size: 9pt;">
                <strong>Nota:</strong> Los resultados presentados son producto del diagnóstico basal realizado en el DSB. Se recomienda integrar estas recomendaciones en el Plan Distrital de Trabajo (PDT) para el presente ejercicio.
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


@router.get("/pdf/{assessment_id}")
async def download_pdf(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate and download PDF report"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Build calculation data
    items_data = [
        {
            "fesp_id": item.fesp_id,
            "item_id": item.item_id,
            "score": item.score
        }
        for item in assessment.items
    ]
    
    if assessment.level == "state":
        unit_name = assessment.state.name
    else:
        unit_name = f"{assessment.jurisdiction.name}, {assessment.state.name}"
    
    summary = {
        "assessment_id": assessment.id,
        "unit_name": unit_name,
        "level": assessment.level,
        "cutoff_date": assessment.cutoff_date.isoformat(),
        "total_compliance": calculate_overall_compliance(items_data),
        "traffic_light": calculate_traffic_light(calculate_overall_compliance(items_data)),
        "fesp_scores": calculate_fesp_scores(items_data),
        "capability_scores": calculate_capability_scores(items_data),
        "policy_cycle_scores": calculate_policy_cycle_scores(items_data),
        "gaps": calculate_gaps(items_data)
    }
    
    summary["gap_count"] = len([g for g in summary["gaps"] if g["priority"] == "high"])
    
    html_content = generate_pdf_html(assessment, summary)
    
    try:
        import pymupdf
        
        # Create PDF using pymupdf Story
        story = pymupdf.Story(html_content)
        
        # Create a PDF document
        doc = pymupdf.open()
        
        # Letter size in points (8.5 x 11 inches)
        rect = pymupdf.Rect(0, 0, 612, 792)
        content_rect = rect + (36, 36, -36, -36)  # 0.5 inch margins
        
        # Place the story
        more = True
        while more:
            page = doc.new_page(width=rect.width, height=rect.height)
            more, _ = story.place(content_rect)
            story.draw(page)
        
        # Get PDF bytes
        pdf_bytes = doc.tobytes()
        doc.close()
        
        filename = f"FESP_DX_{unit_name.replace(' ', '_')}_{assessment.cutoff_date.isoformat()}.pdf"
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        # Fallback to HTML download
        print(f"PDF generation error: {e}")
        return StreamingResponse(
            io.BytesIO(html_content.encode('utf-8')),
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename=reporte_fesp.html"}
        )


@router.get("/csv")
async def download_csv(
    state_id: Optional[int] = None,
    jurisdiction_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export assessments data as CSV"""
    query = db.query(Assessment).filter(Assessment.status == "completed")
    
    if state_id:
        query = query.filter(Assessment.state_id == state_id)
    if jurisdiction_id:
        query = query.filter(Assessment.jurisdiction_id == jurisdiction_id)
    
    assessments = query.order_by(Assessment.cutoff_date.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Simple header
    header = ["ID", "Nivel", "Estado", "Jurisdicción", "Fecha Corte", "Cumplimiento_Global", "Color"]
    # Add all 43 items to columns
    all_defs = get_all_items()
    for item_def in all_defs:
        header.append(f"F{item_def['fesp_number']}_{item_def['code']}")
        
    writer.writerow(header)
    
    for assessment in assessments:
        items_dict = {item.item_id: item.score for item in assessment.items}
        items_data = [{"fesp_id": it.fesp_id, "item_id": it.item_id, "score": it.score} for it in assessment.items]
        compliance = calculate_overall_compliance(items_data)
        
        row = [
            assessment.id,
            assessment.level,
            assessment.state.name,
            assessment.jurisdiction.name if assessment.jurisdiction else "",
            assessment.cutoff_date.isoformat(),
            f"{compliance}%",
            calculate_traffic_light(compliance)
        ]
        
        for item_def in all_defs:
            row.append(items_dict.get(item_def["id"], 0))
            
        writer.writerow(row)
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fesp_historico.csv"}
    )
