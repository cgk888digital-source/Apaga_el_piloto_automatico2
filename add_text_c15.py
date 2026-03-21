import os
from PIL import Image, ImageDraw, ImageFont

def add_texts():
    img_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\capitulo_15_clean.png"
    
    if not os.path.exists(img_path):
        print("Image not found")
        return
        
    img = Image.open(img_path).convert('RGBA')
    
    # Create a transparent overlay for text
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    w, h = img.size
    
    # Values based on our testing
    box_x = int(w * 0.66)
    box_w = int(w * 0.28)
    box_h = int(h * 0.21)
    
    y_start = int(h * 0.17)
    spacing = int(h * 0.05)
    
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", int(h*0.035))
    except:
        font = ImageFont.load_default()

    texts = [
        "Reprogramación\nSubconsciente",
        "Coherencia del\nSistema Nervioso",
        "Afinación\nVibratoria"
    ]
    
    colors = [
        (133, 193, 233, 255), # Light Blue
        (118, 215, 196, 255), # Light Green
        (244, 208, 63, 255),  # Light Yellow / Gold
    ]

    for i in range(3):
        y = y_start + i * (box_h + spacing)
        
        # Center text in the guessed box
        text = texts[i]
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        tx = box_x + box_w/2 - tw/2
        ty = y + box_h/2 - th/2
        
        # Add a subtle drop shadow to make it pop
        draw.multiline_text((tx+2, ty+2), text, fill=(0, 0, 0, 200), font=font, align="center")
        draw.multiline_text((tx, ty), text, fill=colors[i], font=font, align="center")
        
    final_img = Image.alpha_composite(img, txt_layer)
    final_img = final_img.convert("RGB") # Save as non-alpha for PDF
    final_img.save(img_path)
    
    print(f"Applied texts and saved to {img_path}")

if __name__ == '__main__':
    add_texts()
