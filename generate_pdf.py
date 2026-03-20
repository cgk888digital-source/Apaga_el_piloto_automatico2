import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

def format_inline_styles(text):
    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text* -> <i>text</i>  (Permitiendo que esté al inicio del string)
    text = re.sub(r'\*(?!\s)(.+?)(?<!\s)\*', r'<i>\1</i>', text) 
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
    styles.add(ParagraphStyle(name='ListItem', parent=styles['Normal'], leftIndent=25, bulletIndent=10, spaceAfter=6, leading=14))
    
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
        
        current_group = []
        table_data = []
        waiting_for_next = False
        
        def flush_table():
            if table_data:
                # filter formatting row |---|---|
                data = [row for i, row in enumerate(table_data) if not (i == 1 and all(c in '-: ' for c in ''.join(row)))]
                styled_data = []
                for i, row in enumerate(data):
                    styled_row = []
                    for cell in row:
                        if i == 0:
                            styled_row.append(Paragraph(f"<b>{format_inline_styles(cell.strip())}</b>", styles['Normal']))
                        else:
                            styled_row.append(Paragraph(format_inline_styles(cell.strip()), styles['Justify']))
                    styled_data.append(styled_row)
                
                t = Table(styled_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 8),
                    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ecf0f1')),
                    ('GRID', (0,0), (-1,-1), 1, colors.white)
                ]))
                current_group.append(t)
                table_data.clear()

        def flush_group():
            nonlocal waiting_for_next
            flush_table()
            if current_group:
                story.append(KeepTogether(list(current_group)))
                current_group.clear()
            waiting_for_next = False

        chapter_idx = 0
        while chapter_idx < len(lines):
            line = lines[chapter_idx]
            
            # Título de capítulo
            if chapter_idx == 0:
                title_text = line
                if title_text.startswith('# '): title_text = title_text[2:]
                story.append(Paragraph(format_inline_styles(title_text), styles['ChapterTitle']))
                chapter_base = os.path.splitext(os.path.basename(file_path))[0]
                
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
                            display_width = 468
                            c_img.drawWidth = display_width
                            c_img.drawHeight = display_width * aspect
                            story.append(Spacer(1, 12))
                            story.append(KeepTogether([c_img, Spacer(1, 24)]))
                            break
                        except: pass
                chapter_idx += 1
                continue

            # Check inline images
            import re
            img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', line)
            if img_match:
                img_name = os.path.basename(img_match.group(2))
                img_path = os.path.join(current_dir, "imagenes", img_name)
                if os.path.exists(img_path):
                    try:
                        c_img = Image(img_path)
                        aspect = c_img.imageHeight / float(c_img.imageWidth)
                        display_width = 468
                        c_img.drawWidth = display_width
                        c_img.drawHeight = display_width * aspect
                        
                        # Anclamos la imagen al grupo actual para que respete el KeepTogether del párrafo anterior
                        current_group.append(Spacer(1, 6))
                        current_group.append(c_img)
                        current_group.append(Spacer(1, 12))
                        flush_group()
                    except Exception as e:
                        print(f"Failed to load image {img_path}: {e}")
                chapter_idx += 1
                continue

            # Determinación del tipo de línea
            is_header = False
            title_p = None
            is_list_item = False
            
            # Formatos de Markdown y Heurísticos
            if line.startswith('# '):
                is_header, title_p = True, Paragraph(format_inline_styles(line[2:]), styles['ChapterTitle'])
            elif line.startswith('## '):
                is_header, title_p = True, Paragraph(format_inline_styles(line[3:]), styles['SectionTitle'])
            elif line.startswith('### '):
                is_header, title_p = True, Paragraph(format_inline_styles(line[4:]), styles['SubSectionTitle'])
            elif (len(line) < 120 and (line[0].isupper() or line[0] in "¿¡" or line[0].isdigit()) and not line.endswith('.') and not line.startswith('- ') and not line.startswith('* ')):
                # Es un título heurístico
                is_header, title_p = True, Paragraph("<b>" + format_inline_styles(line) + "</b>", styles['SectionTitle'])
            elif line.startswith('- ') or line.startswith('* '):
                is_list_item = True
            elif re.match(r'^[*_]*\d+\.\s+', line):
                is_list_item = True

            is_table_row = bool(re.match(r'^\s*\|.*\|\s*$', line))

            # Tabla lógica
            if is_table_row:
                waiting_for_next = False
                raw_row = [cell.strip() for cell in re.sub(r'^\s*\||\|\s*$', '', line).split('|')]
                table_data.append(raw_row)
                chapter_idx += 1
                continue
            else:
                flush_table()

            # Lógica de acumulación
            if is_header:
                waiting_for_next = False
                has_normal = any(hasattr(x, 'style') and getattr(x.style, 'name', '') not in ['ChapterTitle', 'SectionTitle', 'SubSectionTitle'] for x in current_group)
                if has_normal:
                    flush_group()
                current_group.append(title_p)
                
            elif is_list_item:
                waiting_for_next = False
                if len(current_group) > 15: # Elevado a 15 para evitar que listas largas se corten torpemente
                    flush_group()
                
                raw_text = line
                num_match = re.match(r'^([*_]*)(\d+\.)\s+', raw_text)
                if num_match:
                    # Lista numerada
                    decor = num_match.group(1)
                    bullet_text = num_match.group(2)
                    raw_text = re.sub(r'^[*_]*\d+\.\s+', '', raw_text)
                    if '**' in decor:
                        bullet_text = f"<b>{bullet_text}</b>"
                        raw_text = f"**{raw_text}"
                    elif '*' in decor or '_' in decor:
                        bullet_text = f"<i>{bullet_text}</i>"
                        raw_text = f"*{raw_text}"
                    p = Paragraph(f"<bullet>{bullet_text}</bullet>{format_inline_styles(raw_text)}", styles['ListItem'])
                else:
                    # Lista normal de viñetas
                    raw_text = re.sub(r'^([-*]\s*)', '', raw_text)
                    raw_text = re.sub(r'^([^\w\*\'"\[\(\¿\¡\u201C\u201D\-\+]\s*)+', '', raw_text, flags=re.UNICODE).strip()
                    if not raw_text:
                        raw_text = " "
                    p = Paragraph(f"<bullet>&bull;</bullet>{format_inline_styles(raw_text)}", styles['ListItem'])
                
                current_group.append(p)
                
            elif line == '---':
                flush_group()
                story.append(HRFlowable(width="80%", thickness=1, color=colors.lightgrey, spaceBefore=10, spaceAfter=10))
            elif line == '[[PAGE_BREAK]]':
                flush_group()
                story.append(PageBreak())
            else:
                p = Paragraph(format_inline_styles(line), styles['Justify'])
                
                has_title = any(hasattr(x, 'style') and getattr(x.style, 'name', '') in ['ChapterTitle', 'SectionTitle', 'SubSectionTitle'] for x in current_group)
                
                if has_title:
                    is_quote = bool(re.match(r'^[*_]*["\u201C]', line))
                    current_group.append(p)
                    if line.strip(' *_').endswith(':'):
                        waiting_for_next = True
                    elif is_quote:
                        waiting_for_next = True
                    else:
                        flush_group()
                else:
                    is_quote = bool(re.match(r'^[*_]*["\u201C]', line))
                    if waiting_for_next:
                        current_group.append(p)
                        if is_quote:
                             waiting_for_next = True
                        else:
                             flush_group()
                    elif line.strip(' *_').endswith(':'):
                        flush_group()
                        current_group.append(p)
                        waiting_for_next = True
                    elif is_quote:
                        flush_group()
                        current_group.append(p)
                        waiting_for_next = True
                    else:
                        flush_group()
                        current_group.append(p)
                        flush_group()

            chapter_idx += 1
            
        flush_group()
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
