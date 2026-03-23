import os
import re
from reportlab.lib.pagesizes import A5
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Image, KeepTogether, HRFlowable, Table, TableStyle

def format_inline_styles(text):
    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text* -> <i>text</i>
    text = re.sub(r'\*(?!\s)(.+?)(?<!\s)\*', r'<i>\1</i>', text) 
    return text

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberingCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Solo dibujamos números a partir de la página de cortesía (saltamos portada si queremos)
        if self._pageNumber > 1:
            page_num = f"{self._pageNumber}"
            self.setFont("Helvetica", 9)
            self.drawRightString(doc_width - 72, 30, page_num)

def create_pdf(output_filename, chapter_files, book_title, book_subtitle=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    global doc_width
    # Usamos A5 para un formato más de "Libro"
    from reportlab.lib.pagesizes import A5
    pagesize = A5
    doc_width, doc_height = pagesize
    
    doc = BaseDocTemplate(output_filename, pagesize=pagesize,
                          rightMargin=40, leftMargin=60, # Optimizado para libro físico
                          topMargin=45, bottomMargin=50)
    
    # Configuración de marcos (Frames)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='all_pages', frames=frame)
    doc.addPageTemplates([template])
    
    styles = getSampleStyleSheet()
    # Estilo base optimizado de 10.5pt/12pt (Estándar de libros de gran venta como Atomic Habits o El Alquimista)
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, parent=styles['Normal'], spaceAfter=7, leading=12, fontSize=10.5))
    styles.add(ParagraphStyle(name='Quote', parent=styles['Normal'], leftIndent=15, rightIndent=15, spaceAfter=8, fontName='Helvetica-Oblique', fontSize=9, leading=11, color=colors.HexColor('#555555')))
    styles.add(ParagraphStyle(name='ChapterTitle', parent=styles['Title'], spaceAfter=15, alignment=TA_CENTER, fontSize=22, keepWithNext=True))
    styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Heading2'], spaceAfter=8, spaceBefore=12, keepWithNext=True, fontSize=14, alignment=TA_LEFT, color=colors.HexColor('#2c3e50')))
    styles.add(ParagraphStyle(name='SubSectionTitle', parent=styles['Heading3'], spaceAfter=5, spaceBefore=8, keepWithNext=True, fontSize=11, alignment=TA_LEFT, color=colors.HexColor('#34495e')))
    styles.add(ParagraphStyle(name='ListItem', parent=styles['Normal'], leftIndent=18, bulletIndent=6, spaceAfter=4, leading=12, fontSize=10.5, bulletFontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='TOCItem', parent=styles['Normal'], fontSize=10, leading=14, leftIndent=5))

    def fit_image(img, max_w, max_h):
        aspect = img.imageHeight / float(img.imageWidth)
        w = max_w
        h = max_w * aspect
        if h > max_h:
            h = max_h
            w = h / aspect
        img.drawWidth = w
        img.drawHeight = h
        return img

    story = []

    # 1. PORTADA
    story.append(Spacer(1, 10)) # Reduced
    cover_found = False
    for ext in ['.jpg', '.png', '.jpeg', '.PNG']:
        img_path = os.path.join(current_dir, "imagenes", "imagen_portada" + ext)
        if os.path.exists(img_path):
            img = Image(img_path)
            img = fit_image(img, 240, 300) # Reduced width/height
            story.append(img)
            story.append(Spacer(1, 10)) # Reduced
            cover_found = True
            break
    if not cover_found: story.append(Spacer(1, 80))

    story.append(Paragraph(book_title, styles['ChapterTitle']))
    if book_subtitle: 
        subtitle_style = ParagraphStyle(name='CoverSubtitle', parent=styles['Heading2'], alignment=TA_CENTER, fontSize=12) # Slightly smaller
        story.append(Paragraph(f"<i>{book_subtitle}</i>", subtitle_style))
    story.append(Spacer(1, 10)) # Reduced
    author_style = ParagraphStyle(name='CoverAuthor', parent=styles['Heading3'], alignment=TA_CENTER, fontSize=11)
    story.append(Paragraph("Silvio Vasconcelos", author_style))
    story.append(PageBreak())

    # 2. ÍNDICE (TOC)
    story.append(Paragraph("<b>Índice</b>", styles['ChapterTitle']))
    story.append(Spacer(1, 15))
    for file_path in chapter_files:
        if not os.path.exists(file_path): continue
        with open(file_path, 'r', encoding='utf-8') as f:
            # Buscamos el primer título real entre las primeras 50 líneas
            toc_title = ""
            for i, line in enumerate(f):
                line_clean = line.strip()
                if line_clean and not line_clean.startswith('!') and not line_clean.startswith('['):
                    toc_title = line_clean.lstrip('#').strip()
                    break
                if i > 50: break
            if toc_title:
                story.append(Paragraph(toc_title, styles['TOCItem']))
    story.append(PageBreak())

    # 3. CONTENIDO DEL LIBRO
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
                print(f"Flushing group with {len(current_group)} items for {os.path.basename(file_path)}")
                story.append(KeepTogether(list(current_group)))
                current_group.clear()
            waiting_for_next = False

        chapter_idx = 0
        in_outro = False
        while chapter_idx < len(lines):
            line = lines[chapter_idx]
            
            # Título de capítulo
            if chapter_idx == 0:
                title_text = line.strip().lstrip('#').strip()
                story.append(Paragraph(format_inline_styles(title_text), styles['ChapterTitle']))
                chapter_base = os.path.splitext(os.path.basename(file_path))[0]
                
                # Extraemos solo 'capitulo_XX' ignorando el texto añadido para encontrar las imágenes
                img_base_match = re.match(r"^(capitulo_\d+)", chapter_base)
                img_base = img_base_match.group(1) if img_base_match else chapter_base
                
                img_candidates = [
                    os.path.join(current_dir, "imagenes", img_base + "_clean.png"),
                    os.path.join(current_dir, "imagenes", img_base + "_clean.jpg"),
                    os.path.join(current_dir, "imagenes", img_base + ".png"),
                    os.path.join(current_dir, "imagenes", img_base + ".jpg")
                ]
                for img_path in img_candidates:
                    if os.path.exists(img_path):
                        try:
                            c_img = Image(img_path)
                            fit_image(c_img, 280, 400)
                            c_img.hAlign = 'CENTER'
                            story.append(Spacer(1, 10))
                            story.append(KeepTogether([c_img, Spacer(1, 15)]))
                            break
                        except: pass
                chapter_idx += 1
                continue

            # Check inline images
            img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', line)
            if img_match:
                img_name = os.path.basename(img_match.group(2))
                img_path = os.path.join(current_dir, "imagenes", img_name)
                if os.path.exists(img_path):
                    try:
                        c_img = Image(img_path)
                        aspect = c_img.imageHeight / float(c_img.imageWidth)
                        display_width = 280
                        if img_name == "diagrama_creencia.png":
                            display_width = 300 # Reducido para que se vea más pequeño en la página
                        
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

            line = line.strip()
            if not line:
                continue
            
            # Determinación del tipo de línea
            is_header = False
            title_p = None
            is_list_item = False
            
            # Formatos de Markdown y Heurísticos
            if line.startswith('#'):
                # Limpiamos todos los '#' iniciales y espacios para que no se impriman en el PDF
                raw_text_clean = line.lstrip('#').strip()
                if line.startswith('###'):
                    is_header, title_p = True, Paragraph(format_inline_styles(raw_text_clean), styles['SubSectionTitle'])
                elif line.startswith('##'):
                    is_header, title_p = True, Paragraph(format_inline_styles(raw_text_clean), styles['SectionTitle'])
                else:
                    is_header, title_p = True, Paragraph(format_inline_styles(raw_text_clean), styles['ChapterTitle'])
            elif line.startswith('- ') or line.startswith('* '):
                is_list_item = True
            elif re.match(r'^[*_]*\d+\.\s+', line):
                is_list_item = True
            elif (len(line) < 120 and (line[0].isupper() or line[0] in "¿¡" or line[0].isdigit()) and not line.endswith('.') and not line.startswith('- ') and not line.startswith('* ')):
                # Es un título heurístico (limpiamos por si acaso tiene # sin espacio)
                raw_text_clean = line.lstrip('#').strip()
                is_header, title_p = True, Paragraph("<b>" + format_inline_styles(raw_text_clean) + "</b>", styles['SectionTitle'])

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
                prev_header_level = 0
                for item in current_group:
                    i_style = getattr(item, 'style', None)
                    s_name = getattr(i_style, 'name', '') if i_style else ''
                    if s_name == 'ChapterTitle': prev_header_level = 1
                    elif s_name == 'SectionTitle': prev_header_level = 2
                    elif s_name == 'SubSectionTitle': prev_header_level = 3
                
                curr_header_level = 0
                s_name_curr = getattr(title_p.style, 'name', '')
                if s_name_curr == 'ChapterTitle': curr_header_level = 1
                elif s_name_curr == 'SectionTitle': curr_header_level = 2
                elif s_name_curr == 'SubSectionTitle': curr_header_level = 3
                
                has_normal = any(hasattr(x, 'style') and getattr(x.style, 'name', '') not in ['ChapterTitle', 'SectionTitle', 'SubSectionTitle'] for x in current_group)
                
                # Si ya hay un encabezado del mismo nivel o nivel superior, o si ya hay contenido normal, flusheamos
                if has_normal or (prev_header_level > 0 and curr_header_level <= prev_header_level):
                    flush_group()
                
                current_group.append(title_p)
                waiting_for_next = True # Forzamos a que el siguiente elemento se una al encabezado
                
            elif is_list_item:
                was_waiting = waiting_for_next
                waiting_for_next = False
                # Protegemos el grupo si la línea anterior terminaba en dos puntos o indicaba continuación
                # Pero si el grupo ya es excesivo, debemos flushear para no romper el layout del PDF
                if len(current_group) > 8: # Reducido para A5
                    flush_group()
                
                raw_text = line
                num_match = re.match(r'^([*_]*)(\d+\.)\s+', raw_text)
                if num_match:
                    # Lista numerada
                    decor = num_match.group(1)
                    bullet_text = num_match.group(2)
                    raw_text = re.sub(r'^[*_]*\d+\.\s+', '', raw_text)
                    if '**' in decor:
                        raw_text = f"**{raw_text}"
                    elif '*' in decor or '_' in decor:
                        raw_text = f"*{raw_text}"
                    p = Paragraph(format_inline_styles(raw_text), styles['ListItem'], bulletText=bullet_text)
                else:
                    # Lista normal de viñetas
                    raw_text = re.sub(r'^([-*]\s*)', '', raw_text)
                    raw_text = re.sub(r'^([^\w\*\'"\[\(\¿\¡\u201C\u201D\-\+]\s*)+', '', raw_text, flags=re.UNICODE).strip()
                    if not raw_text:
                        raw_text = " "
                    # Usamos el punto (\u2022) como viñeta
                    p = Paragraph(format_inline_styles(raw_text), styles['ListItem'], bulletText='\u2022')
                
                current_group.append(p)
                if len(current_group) > 5: print(f"Group growth in {os.path.basename(file_path)}: {len(current_group)} items")
                
            elif line == '---' or line.startswith('[[PAGE_BREAK]]'):
                # Pre-verificación: ¿la siguiente línea es el cierre final?
                next_is_outro = False
                if chapter_idx + 1 < len(lines):
                    next_line = lines[chapter_idx+1].strip()
                    if "Muy buenos días" in next_line or "bienvenido a la libertad mental" in next_line:
                        next_is_outro = True
                
                if not next_is_outro:
                    flush_group()
                
                if line.startswith('[[PAGE_BREAK]]'):
                    story.append(PageBreak())
                elif not next_is_outro:
                    story.append(Spacer(1, 20))
            else:
                p = Paragraph(format_inline_styles(line), styles['Justify'])
                is_bold_header = bool(re.match(r'^[*_]{2,}[^*_]+[*_]{2,}$', line.strip()))
                is_quote = bool(re.match(r'^[*_]*["\u201C]', line))
                is_outro_line = any(x in line for x in ["Antes de pasar al Capítulo", "Nos vemos en el Capítulo", "Muy buenos días", "bienvenido a la libertad mental"])
                
                # Acumulamos el párrafo en el grupo actual
                current_group.append(p)
                if len(current_group) > 6: print(f"Big group found in {os.path.basename(file_path)}: {len(current_group)} items") # Reducido para A5
                
                # Determinamos si es una línea que pide continuidad
                is_continuation = line.strip(' *_').endswith(':') or line.strip(' *_').endswith('...') or is_quote or is_bold_header or is_outro_line
                
                # Si es un párrafo final (no pide continuar), flusheamos el grupo para imprimirlo
                if not is_continuation:
                    flush_group()
                else:
                    # Si es continuación, marcamos que esperamos algo más antes de flushear el KeepTogether
                    waiting_for_next = True

            chapter_idx += 1
            
        flush_group()
        story.append(PageBreak())

    doc.build(story, canvasmaker=NumberingCanvas)
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
        print("Chapters found to process:")
        for c in chapters:
            print(f"  - {os.path.basename(c)}")
        create_pdf(output_pdf, chapters, "Apaga el Piloto Automático", "Tu Manual de vuelo para tomar el control de tu Vida y tu Mente")
