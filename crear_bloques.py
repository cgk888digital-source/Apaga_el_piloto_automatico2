from PIL import Image, ImageDraw, ImageFont
import os

width, height = 1200, 300
img = Image.new('RGB', (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# Intentar cargar fuente Arial
font_path = r"C:\Windows\Fonts\arial.ttf"
try:
    font = ImageFont.truetype(font_path, 22)
except:
    font = ImageFont.load_default()

steps = ["PENSAMIENTO", "EMOCIÓN", "SENTIMIENTO", "VIBRACIÓN / ENERGÍA", "COMPORTAMIENTO"]

box_w, box_h = 200, 80
gap = 40
start_x = (width - (len(steps)*(box_w) + (len(steps)-1)*gap)) // 2
start_y = (height - box_h) // 2

for i, text in enumerate(steps):
    x = start_x + i * (box_w + gap)
    y = start_y
    
    # Draw box (rounded if PIL version supports it, else normal rectangle)
    try:
        draw.rounded_rectangle([x, y, x+box_w, y+box_h], radius=15, fill="#2c3e50")
    except AttributeError:
        draw.rectangle([x, y, x+box_w, y+box_h], fill="#2c3e50")
    
    # Calculate text position
    try:
        left, top, right, bottom = font.getbbox(text)
        tw = right - left
        th = bottom - top
    except AttributeError:
        tw, th = font.getsize(text)
    
    # Check if text is too wide, split into two lines if needed
    if tw > box_w - 20: 
        words = text.split(" / ") if " / " in text else text.split()
        if len(words) > 1:
            line1, line2 = words[0], " ".join(words[1:])
            try:
                tw1, th1 = font.getbbox(line1)[2] - font.getbbox(line1)[0], font.getbbox(line1)[3] - font.getbbox(line1)[1]
                tw2, th2 = font.getbbox(line2)[2] - font.getbbox(line2)[0], font.getbbox(line2)[3] - font.getbbox(line2)[1]
            except Exception:
                tw1, th1 = font.getsize(line1)
                tw2, th2 = font.getsize(line2)
            
            draw.text((x + (box_w - tw1) / 2, y + (box_h - th1*2) / 2 - 5), line1, fill="white", font=font)
            draw.text((x + (box_w - tw2) / 2, y + (box_h - th1*2) / 2 + th1 + 5), line2, fill="white", font=font)
        else:
            # Scale it horizontally or just draw it smaller? Since we predefined font size, just draw it centered.
            draw.text((x + (box_w - tw) / 2, y + (box_h - th) / 2 - 2), text, fill="white", font=font)
    else:
        draw.text((x + (box_w - tw) / 2, y + (box_h - th) / 2 - 2), text, fill="white", font=font)
        
    
    # Draw arrow
    if i < len(steps) - 1:
        arr_x = x + box_w
        arr_y = y + box_h/2
        
        # Draw arrow body
        draw.line([(arr_x + 5, arr_y), (arr_x + gap - 10, arr_y)], fill="#e74c3c", width=5)
        # Draw arrow head
        draw.polygon([(arr_x + gap - 15, arr_y - 8),
                      (arr_x + gap - 3, arr_y),
                      (arr_x + gap - 15, arr_y + 8)], fill="#e74c3c")

out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\ciclo_bloques.png"
img.save(out_path)
print(f"Imagen generada en: {out_path}")
