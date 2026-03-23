from PIL import Image, ImageDraw, ImageFont
import os

def update_master_cover():
    img_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\imagen_portada_master.png"
    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\imagen_portada.png"
    
    if not os.path.exists(img_path): return

    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    draw = ImageDraw.Draw(img)
    
    # Expanded cleaning zone to catch the original "TU GUÍA PARA TOMAR EL CONTROL"
    # We increase the range to y_end*0.38
    title_y_start = int(h * 0.04)
    title_y_end = int(h * 0.38) # Increased to cover the original subtitle
    
    cx1, cx2 = int(w * 0.08), int(w * 0.92)
    # Filling with a clean dark color
    draw.rectangle([cx1, title_y_start, cx2, title_y_end], fill=(5, 5, 5)) 

    def get_font(text, max_w, initial_size, font_path):
        size = initial_size
        while size > 10:
            try:
                f = ImageFont.truetype(font_path, size)
            except:
                f = ImageFont.load_default()
                return f, size
            bbox = draw.textbbox((0, 0), text, font=f)
            if (bbox[2] - bbox[0]) <= max_w:
                return f, size
            size -= 2
        return ImageFont.load_default(), size

    max_text_w = int(w * 0.78)
    f_path_bd = "C:\\Windows\\Fonts\\arialbd.ttf"
    f_path_reg = "C:\\Windows\\Fonts\\arial.ttf"
    
    line1 = "APAGA EL"
    line2 = "PILOTO AUTOMÁTICO"
    
    font1, _ = get_font(line1, max_text_w, 62, f_path_bd)
    font2, _ = get_font(line2, max_text_w, 62, f_path_bd)
    
    y_curr = title_y_start + 45
    for line, f in [(line1, font1), (line2, font2)]:
        bbox = draw.textbbox((0, 0), line, font=f)
        tx = (w - (bbox[2] - bbox[0])) // 2
        draw.text((tx, y_curr), line, font=f, fill=(255, 255, 255))
        y_curr += (bbox[3] - bbox[1]) + 20
        
    sub_text = "Tu Manual de vuelo para tomar el control de tu Vida y tu Mente"
    font_s, _ = get_font(sub_text, max_text_w, 25, f_path_reg)
    bbox_s = draw.textbbox((0, 0), sub_text, font=font_s)
    tx_s = (w - (bbox_s[2] - bbox_s[0])) // 2
    draw.text((tx_s, y_curr + 15), sub_text, font=font_s, fill=(210, 210, 210))
    
    author_text = "Silvio Vasconcelos"
    font_a, _ = get_font(author_text, max_text_w, 28, f_path_bd)
    bbox_a = draw.textbbox((0, 0), author_text, font=font_a)
    tx_a = (w - (bbox_a[2] - bbox_a[0])) // 2
    draw.text((tx_a+2, h - 88), author_text, font=font_a, fill=(0, 0, 0))
    draw.text((tx_a, h - 90), author_text, font=font_a, fill=(255, 255, 255))
    
    img.save(out_path)
    print(f"ULTRA-CLEAN MASTER COVER generated and saved to {out_path}")

if __name__ == "__main__":
    update_master_cover()
