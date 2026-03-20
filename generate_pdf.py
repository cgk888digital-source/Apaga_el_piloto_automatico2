import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

def format_inline_styles(text):
    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text* -> <i>text</i>
    text = re.sub(r'(?<!^)\*(.*?)\*', r'<i>\1</i>', text) 
    return text

def create_pdf(output_filename, chapter_files, book_title, book_subtitle=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=54)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, parent=styles['Normal'], spaceAfter=12, leading=14))
    styles.add(ParagraphStyle(name='Quote', parent=styles['Normal'], leftIndent=30, rightIndent=30, spaceAfter=12, fontName='Helvetica-Oblique', fontSize=10, leading=14))
    styles.add(ParagraphStyle(name='ChapterTitle', parent=styles['Title'], spaceAfter=24, alignment=TA_CENTER, fontSize=28, keepWithNext=True))
    styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Heading2'], spaceAfter=12, spaceBefore=18, keepWithNext=True, fontSize=18, alignment=TA_LEFT, color=colors.HexColor('#2c3e50')))
    styles.add(ParagraphStyle(name='SubSectionTitle', parent=styles['Heading3'], spaceAfter=8, spaceBefore=12, keepWithNext=True, fontSize=14, alignment=TA_LEFT, color=colors.HexColor('#34495e')))
    styles.add(ParagraphStyle(name='ListItem', parent=styles['Normal'], leftIndent=20, spaceAfter=6, leading=14))
    
    story = []

    # Portada
    story.append(Spacer(1, 40))
    cover_found = False
    for ext in ['.jpg', '.png', '.jpeg', '.PNG']:
        img_path = os.path.join(current_dir, "imagenes", "imagen_portada" + ext)
        if os.path.exists(img_path):
            img = Image(img_path)
            aspect = img.imageHeight / float(img.imageWidth)
            display_width = 400
            img.drawWidth = display_width
            img.drawHeight = display_width * aspect
            story.append(img)
            story.append(Spacer(1, 40))
            cover_found = True
            break
    if not cover_found: story.append(Spacer(1, 140))

    story.append(Paragraph(book_title, styles['ChapterTitle']))
    if book_subtitle: story.append(Paragraph(book_subtitle, styles['Heading2']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Edición Completa", styles['Heading1']))
    story.append(PageBreak())

    for file_path in chapter_files:
        if not os.path.exists(file_path): continue
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        
        chapter_idx = 0
        while chapter_idx < len(lines):
            line = lines[chapter_idx]
            
            # --- Títulos con Markdown (#, ##) ---
            if line.startswith('# '):
                story.append(Paragraph(format_inline_styles(line[2:]), styles['ChapterTitle']))
                chapter_idx += 1; continue
            if line.startswith('## '):
                story.append(Paragraph(format_inline_styles(line[3:]), styles['SectionTitle']))
                chapter_idx += 1; continue
            
            # --- Títulos heurísticos (incluyendo los que terminan en :) ---
            is_title = (len(line) < 100 and (line[0].isupper() or line[0] in "¿¡") and not line.endswith('.'))
            
            if is_title and chapter_idx > 0:
                title_text = format_inline_styles(line)
                if not title_text.startswith('<b>'): title_text = f"<b>{title_text}</b>"
                title_p = Paragraph(title_text, styles['SectionTitle'])
                
                if chapter_idx + 1 < len(lines):
                    next_line = lines[chapter_idx+1]
                    next_p = Paragraph(format_inline_styles(next_line), styles['Justify'])
                    story.append(KeepTogether([title_p, next_p]))
                    chapter_idx += 2 
                    continue
                else:
                    story.append(title_p)
            elif chapter_idx == 0:
                # Título de Capítulo + Imagen de Capítulo
                story.append(Paragraph(format_inline_styles(line), styles['ChapterTitle']))
                chapter_base = os.path.splitext(os.path.basename(file_path))[0]
                # Prefer clean version, then fall back to originals
                img_candidates = [
                    os.path.join(current_dir, "imagenes", chapter_base + "_clean.png"),
                ] + [
                    os.path.join(current_dir, "imagenes", chapter_base + ext)
                    for ext in ['.jpg', '.png', '.jpeg', '.PNG']
                ]
                for img_path in img_candidates:
                    if os.path.exists(img_path):
                        try:
                            c_img = Image(img_path)
                            aspect = c_img.imageHeight / float(c_img.imageWidth)
                            display_width = 468 # Ancho máximo de la página
                            c_img.drawWidth = display_width
                            c_img.drawHeight = display_width * aspect
                            story.append(Spacer(1, 12))
                            story.append(c_img)
                            story.append(Spacer(1, 24))
                            break
                        except: pass
            elif line.startswith('- ') or line.startswith('* '):
                story.append(Paragraph(f"• {format_inline_styles(line[2:])}", styles['ListItem']))
            elif line == '---':
                story.append(HRFlowable(width="80%", thickness=1, color=colors.lightgrey, spaceBefore=10, spaceAfter=10))
            elif line == '[[PAGE_BREAK]]':
                story.append(PageBreak())
            else:
                story.append(Paragraph(format_inline_styles(line), styles['Justify']))
            chapter_idx += 1
                
        story.append(PageBreak())

    doc.build(story)
    print(f"PDF generado exitosamente con imágenes.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_dir, "capitulos")
    output_pdf = os.path.join(current_dir, "Apaga_el_Piloto_Automatico.pdf")
    
    chapters = []
    if os.path.exists(base_dir):
        chapters = sorted([
            os.path.join(base_dir, f) 
            for f in os.listdir(base_dir) 
            if f.startswith("capitulo_") and f.endswith(".md")
        ])
    
    if chapters:
        create_pdf(output_pdf, chapters, "Apaga el Piloto Automático")
