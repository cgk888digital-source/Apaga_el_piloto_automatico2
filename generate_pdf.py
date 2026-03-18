import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

def create_pdf(output_filename, chapter_files, book_title, book_subtitle=None):
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, parent=styles['Normal'], spaceAfter=12))
    styles.add(ParagraphStyle(name='Quote', parent=styles['Normal'], leftIndent=20, rightIndent=20, spaceAfter=12, fontName='Helvetica-Oblique'))
    styles.add(ParagraphStyle(name='ChapterTitle', parent=styles['Title'], spaceAfter=24, alignment=TA_CENTER, fontSize=24))
    styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Heading2'], spaceAfter=12, spaceBefore=12))
    
    story = []

    # Title Page
    story.append(Spacer(1, 60))
    
    img_path = os.path.join(current_dir, "imagen_portada.png")
    if os.path.exists(img_path):
        # Add image, resizing to fit width comfortably (approx 6 inches = 432 pts)
        img = Image(img_path)
        # Simple aspect ratio scaling
        aspect = img.imageHeight / float(img.imageWidth)
        display_width = 450
        display_height = display_width * aspect
        img.drawWidth = display_width
        img.drawHeight = display_height
        
        story.append(img)
        story.append(Spacer(1, 30))
    else:
        story.append(Spacer(1, 140))

    story.append(Paragraph(book_title, styles['ChapterTitle']))
    if book_subtitle:
        story.append(Paragraph(book_subtitle, styles['Heading2']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Edición Completa", styles['Heading1']))
    story.append(PageBreak())

    for file_path in chapter_files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        is_first_line = True
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Heuristic detection for headers without markdown symbols
            
            # 1. Chapter Title (First non-empty line of the file)
            if is_first_line:
                story.append(Paragraph(line, styles['ChapterTitle']))
                is_first_line = False
                continue

            # 2. Blockquotes
            if line.startswith('> '):
                text = line[2:].strip()
                text = format_inline_styles(text)
                story.append(Paragraph(text, styles['Quote']))
            
            # 3. Horizontal Rule
            elif line == '---':
                story.append(Spacer(1, 12))
            
            # 4. List items
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                text = format_inline_styles(text)
                story.append(Paragraph(f"• {text}", styles['Normal'])) 
            elif re.match(r'^\d+\.', line):
                text = line.split('.', 1)[1].strip()
                text = format_inline_styles(text)
                number = line.split('.', 1)[0]
                story.append(Paragraph(f"{number}. {text}", styles['Normal']))

            # 5. Section Titles (Heuristics: Short line, starts with Upper, no end punctuation or colon)
            # Check length < 100 char
            # Check if it doesn't end with .
            # Check if it's not starting with lowercase (titles usually start with Uppercase)
            elif (len(line) < 100 and 
                  line[0].isupper() and 
                  not line.endswith('.') and 
                  not line.endswith(':') and
                  not line.endswith(';')):
                  
                # Extra check: If it's all uppercase or just Title Case
                # User suggestion: "lines short in uppercase" -> prioritize uppercase detection
                if line.isupper() or len(line) < 60:
                     story.append(Paragraph(line, styles['SectionTitle']))
                else:
                     text = format_inline_styles(line)
                     story.append(Paragraph(text, styles['Justify']))

            # 6. Normal Text
            else:
                text = format_inline_styles(line)
                story.append(Paragraph(text, styles['Justify']))
                
        story.append(PageBreak())

    doc.build(story)
    print(f"PDF generated: {output_filename}")

def format_inline_styles(text):
    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text* -> <i>text</i> - careful with bullets
    # Simple formatting: assume *word* is italic if not at start of line (handled by bullet check)
    # But here we are processing the content of the line.
    text = re.sub(r'(?<!^)\*(.*?)\*', r'<i>\1</i>', text) 
    return text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_dir, "capitulos")
    output_pdf = os.path.join(current_dir, "Apaga_el_Piloto_Automatico.pdf")
    book_title = "Apaga el piloto automático de tu mente"
    book_subtitle = "despierta tu consciencia"

    chapters = [
        os.path.join(base_dir, "capitulo_01.md"),
        os.path.join(base_dir, "capitulo_02.md"),
        os.path.join(base_dir, "capitulo_03.md"),
        os.path.join(base_dir, "capitulo_04.md"),
        os.path.join(base_dir, "capitulo_05.md"),
        os.path.join(base_dir, "capitulo_06.md"),
        os.path.join(base_dir, "capitulo_07.md"),
        os.path.join(base_dir, "capitulo_08.md"),
        os.path.join(base_dir, "capitulo_09.md"),
    ]
    
    create_pdf(output_pdf, chapters, book_title, book_subtitle)
