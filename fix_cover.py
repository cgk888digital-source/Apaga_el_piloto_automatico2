from PIL import Image, ImageDraw, ImageFont
import os

def fix_cover_final_version():
    img_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\imagen_portada.png"
    # Always start from v2 to have the original pilot image details
    src_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\imagen_portada_v2.png"
    
    if not os.path.exists(src_path): src_path = img_path

    img = Image.open(src_path).convert('RGB')
    w, h = img.size
    draw = ImageDraw.Draw(img)
    
    # 1. Clean the subtitle area completely but carefully to preserve pilot (assuming pilot is below Y=400)
    # Most pilots in cockpit views are in the lower half. 
    # We will clean the sky/pillar from Y=140 to Y=400 to remove all previous text layers.
    clean_y_start = 140
    clean_y_end = 405
    
    print(f"Cleaning area Y={clean_y_start} to Y={clean_y_end}...")
    for y in range(clean_y_start, clean_y_end):
        cl = img.getpixel(( int(w*0.1), y))
        cr = img.getpixel(( int(w*0.9), y))
        for x in range(w):
            ratio = x / w
            r = int(cl[0] * (1 - ratio) + cr[0] * ratio)
            g = int(cl[1] * (1 - ratio) + cr[1] * ratio)
            b = int(cl[2] * (1 - ratio) + cr[2] * ratio)
            img.putpixel((x, y), (r, g, b))

    # 2. Redraw the central pillar from a clean source high up (Y=100)
    pillar_x = w // 2
    pillar_w = 44
    p_strip = [img.getpixel((x, 100)) for x in range(pillar_x - pillar_w//2, pillar_x + pillar_w//2)]
    for y in range(clean_y_start, clean_y_end):
        for i, x in enumerate(range(pillar_x - pillar_w//2, pillar_x + pillar_w//2)):
            img.putpixel((x, y), p_strip[i])

    # 3. Clean the AUTHOR area at the bottom to avoid repetition
    # Bottom area Y=540 to 600
    author_clean_start = 530
    author_clean_end = 610
    for y in range(author_clean_start, author_clean_end):
        cl = img.getpixel((40, y))
        cr = img.getpixel((w-40, y))
        for x in range(w):
            ratio = x / w
            r = int(cl[0] * (1 - ratio) + cr[0] * ratio)
            g = int(cl[1] * (1 - ratio) + cr[1] * ratio)
            b = int(cl[2] * (1 - ratio) + cr[2] * ratio)
            img.putpixel((x, y), (r, g, b))

    # 4. Draw the CORRECT texts
    try:
        font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 25)
        font_author = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 18)
    except:
        font_sub = ImageFont.load_default()
        font_author = ImageFont.load_default()
        
    # Subtitle
    text_sub = "Tu manual de Vuelo para Tomar el Control de tu vida y de tu mente."
    words = text_sub.split()
    line1 = " ".join(words[:7]) # Tu manual de Vuelo para Tomar el
    line2 = " ".join(words[7:]) # Control de tu vida y de tu mente.
    
    # Render line 1 at Y=250
    bbox1 = draw.textbbox((0, 0), line1, font=font_sub)
    tx1 = (w - (bbox1[2] - bbox1[0])) // 2
    draw.text((tx1+1, 251), line1, font=font_sub, fill=(0, 0, 0, 160))
    draw.text((tx1, 250), line1, font=font_sub, fill=(245, 245, 245))
    
    # Render line 2 at Y=320
    bbox2 = draw.textbbox((0, 0), line2, font=font_sub)
    tx2 = (w - (bbox2[2] - bbox2[0])) // 2
    draw.text((tx2+1, 321), line2, font=font_sub, fill=(0, 0, 0, 160))
    draw.text((tx2, 320), line2, font=font_sub, fill=(245, 245, 245))
    
    # Author
    author_text = "Por Silvio Vasconcelos"
    bbox_a = draw.textbbox((0, 0), author_text, font=font_author)
    txa = (w - (bbox_a[2] - bbox_a[0])) // 2
    draw.text((txa, 560), author_text, font=font_author, fill=(220, 220, 220))
    
    img.save(img_path)
    print(f"SUCCESS: Cover fixed (cleared repetitions) and saved to {img_path}")

if __name__ == "__main__":
    fix_cover_final_version()
