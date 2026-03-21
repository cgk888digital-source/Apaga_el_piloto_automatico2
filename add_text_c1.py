import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def add_texts():
    img_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\capitulo_01_clean.png"
    
    if not os.path.exists(img_path):
        print("Image not found")
        return
        
    # Guardamos un backup si no existe
    backup_path = img_path + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy(img_path, backup_path)
    
    # Abrimos desde el backup para no sobreescribir repetidamente si corremos varias veces
    img = Image.open(backup_path).convert('RGBA')
    
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    w, h = img.size
    
    box_x = int(w * 0.65)
    box_w = int(w * 0.3)
    box_h = int(h * 0.22)
    
    y_start = int(h * 0.15)
    spacing = int(h * 0.05)
    
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", int(h*0.035))
    except:
        font = ImageFont.load_default()

    texts = [
        "LA MENTE\n(Procesador)",
        "EL EGO\n(Identidad)",
        "LA CONSCIENCIA\n(El Observador)"
    ]
    
    # Colores que encajan con la estética sci-fi/energía (cyan, dorado/naranja, verde)
    colors = [
        (100, 200, 255, 255), # Cyan para Mente
        (255, 150, 50, 255),  # Naranja para Ego
        (100, 255, 150, 255), # Verde luminoso para Consciencia
    ]

    for i in range(3):
        y = y_start + i * (box_h + spacing)
        
        text = texts[i]
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        tx = box_x + box_w/2 - tw/2
        ty = y + box_h/2 - th/2
        
        draw.multiline_text((tx+2, ty+2), text, fill=(0, 0, 0, 200), font=font, align="center")
        draw.multiline_text((tx, ty), text, fill=colors[i], font=font, align="center")
        
    final_img = Image.alpha_composite(img, txt_layer)
    final_img = final_img.convert("RGB")
    final_img.save(img_path)
    
    print(f"Applied texts and saved to {img_path}")

if __name__ == '__main__':
    add_texts()
