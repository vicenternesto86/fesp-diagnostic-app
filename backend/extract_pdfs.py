import fitz  # PyMuPDF
import os

# Path to the PDFs
pdf_dir = r"c:\Users\Lenovo\OneDrive\Escritorio\APPs\FESP Dx fast"

# Extract text from each DSB PDF
for i in range(1, 13):
    pdf_path = os.path.join(pdf_dir, f"DSB{i} Informe Específico.pdf")
    if os.path.exists(pdf_path):
        print(f"\n{'='*80}")
        print(f"DSB{i} INFORME ESPECÍFICO")
        print(f"{'='*80}")
        
        doc = fitz.open(pdf_path)
        # Get first 3 pages for structure analysis
        for page_num in range(min(5, len(doc))):
            page = doc[page_num]
            text = page.get_text()
            print(f"\n--- Página {page_num + 1} ---")
            print(text[:3000] if len(text) > 3000 else text)
        doc.close()
    else:
        print(f"No encontrado: {pdf_path}")
