import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

def create_pdf(output_filename, chapter_files, book_title, book_subtitle=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, parent=styles['Normal'], spaceAfter=12))
    styles.add(ParagraphStyle(name='Quote', parent=styles['Normal'], leftIndent=20, rightIndent=20, spaceAfter=12, fontName='Helvetica-Oblique'))
    styles.add(ParagraphStyle(name='ChapterTitle', parent=styles['Title'], spaceAfter=24, alignment=TA_CENTER, fontSize=24, keepWithNext=True))
    styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Heading2'], spaceAfter=12, spaceBefore=12, keepWithNext=True))
    
    story = []

    # Title Page
    story.append(Spacer(1, 60))
    
    # Try different cover image extensions
    cover_found = False
    for ext in ['.jpg', '.png', '.jpeg']:
        img_path = os.path.join(current_dir, "imagenes", "imagen_portada" + ext)
        if not os.path.exists(img_path):
            img_path = os.path.join(current_dir, "imagen_portada" + ext)
            
        if os.path.exists(img_path):
            img = Image(img_path)
            aspect = img.imageHeight / float(img.imageWidth)
            display_width = 450
            display_height = display_width * aspect
            img.drawWidth = display_width
            img.drawHeight = display_height
            story.append(img)
            story.append(Spacer(1, 30))
            cover_found = True
            break
            
    if not cover_found:
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
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
                continue
            
            # 1. Chapter Title (First non-empty line)
            if is_first_line:
                story.append(Paragraph(line, styles['ChapterTitle']))
                
                # Image logic
                chapter_base = os.path.splitext(os.path.basename(file_path))[0]
                for ext in ['.jpg', '.png', '.jpeg']:
                    img_path = os.path.join(current_dir, "imagenes", chapter_base + ext)
                    if os.path.exists(img_path):
                        img = Image(img_path)
                        aspect = img.imageHeight / float(img.imageWidth)
                        display_width = 400
                        display_height = display_width * aspect
                        img.drawWidth = display_width
                        img.drawHeight = display_height
                        story.append(Spacer(1, 12))
                        story.append(img)
                        story.append(Spacer(1, 24))
                        break
                
                is_first_line = False
                continue

            # 2. Horizontal Rule
            if line == '---' or line == '***':
                story.append(Spacer(1, 12))
                story.append(HRFlowable(width="80%", thickness=1, color=colors.lightgrey, spaceBefore=6, spaceAfter=6))
                story.append(Spacer(1, 12))
                continue

            # 3. Blockquotes
            if line.startswith('> '):
                text = line[2:].strip()
                text = format_inline_styles(text)
                story.append(Paragraph(text, styles['Quote']))
                continue
            
            # 4. List items
            if line.startswith('- ') or line.startswith('* ') or re.match(r'^\d+\.', line):
                if line.startswith('- ') or line.startswith('* '):
                    text = line[2:].strip()
                else:
                    text = line.split('.', 1)[1].strip()
                text = format_inline_styles(text)
                story.append(Paragraph(f"• {text}" if not line[0].isdigit() else f"{line.split('.')[0]}. {text}", styles['Normal']))
                continue

            # 5. Section Titles (Heuristics)
            is_title = (len(line) < 100 and 
                      line[0].isupper() and 
                      not line.endswith('.') and 
                      not line.endswith(':') and
                      not line.endswith(';'))
            
            if is_title:
                text = format_inline_styles(line)
                story.append(Paragraph(text, styles['SectionTitle']))
            else:
                text = format_inline_styles(line)
                story.append(Paragraph(text, styles['Justify']))
                
        story.append(PageBreak())

    doc.build(story)
    print(f"PDF generated: {output_filename}")

def format_inline_styles(text):
    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text* -> <i>text</i>
    text = re.sub(r'(?<!^)\*(.*?)\*', r'<i>\1</i>', text) 
    return text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_dir, "capitulos")
    output_pdf = os.path.join(current_dir, "Apaga_el_Piloto_Automatico.pdf")
    book_title = "Apaga el Piloto Automático"
    book_subtitle = ""

    # Discover all chapters automatically
    chapters = []
    if os.path.exists(base_dir):
        chapters = sorted([
            os.path.join(base_dir, f) 
            for f in os.listdir(base_dir) 
            if f.startswith("capitulo_") and f.endswith(".md")
        ])
    
    if not chapters:
        print("No matching chapter files found.")
        exit(1)

    
    create_pdf(output_pdf, chapters, book_title, book_subtitle)
