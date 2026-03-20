import math
from PIL import Image, ImageDraw, ImageFont

def draw_cycle():
    width, height = 1200, 1200
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
    except:
        font_main = ImageFont.load_default()
        font_sub = font_main

    nodes = [
        ("PENSAMIENTO", ""),
        ("EMOCIÓN", "(30-90 s de química corporal)"),
        ("Si agregas MÁS PENSAMIENTOS", "sobre la emoción"),
        ("SENTIMIENTO", "(emoción prolongada)"),
        ("ESTADO EMOCIONAL", "(sentimientos habituales)"),
        ("PERSONALIDAD", "(estados emocionales crónicos)")
    ]

    cx, cy = width / 2, height / 2
    R = 420

    angles = [
        -math.pi/2,         # Top
        -math.pi/6,         # Top Right
         math.pi/6,         # Bottom Right
         math.pi/2,         # Bottom
         math.pi - math.pi/6, # Bottom Left
         math.pi + math.pi/6  # Top Left
    ]

    box_w, box_h = 320, 100

    boxes = []
    for i in range(len(nodes)):
        x = cx + R * math.cos(angles[i]) - box_w/2
        y = cy + R * math.sin(angles[i]) - box_h/2
        boxes.append((x, y, x+box_w, y+box_h))

    # Definimos la funcion de padding para el bounding box
    def point_in_box(px, py, b):
        pad = 8
        return (b[0] - pad <= px <= b[2] + pad) and (b[1] - pad <= py <= b[3] + pad)

    # Dibujar el circulo de fondo que conecta todo (como esta debajo de las cajas, no se vera dentro)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline="#e74c3c", width=6)

    # Dibujar las puntas de flecha
    for i in range(len(boxes)):
        b = boxes[i]
        theta_i = angles[i]
        
        # Encontramos la punta de la flecha retrocediendo un poco el angulo 
        # hasta salir del bounding box
        tip_x = cx
        tip_y = cy
        tip_alpha = theta_i
        
        for delta_deg in range(1, 90, 1):
            alpha = theta_i - math.radians(delta_deg)
            px = cx + R * math.cos(alpha)
            py = cy + R * math.sin(alpha)
            if not point_in_box(px, py, b):
                tip_x = px
                tip_y = py
                tip_alpha = alpha
                break
                
        # Tangente en ese punto para un circulo clockwise
        dx = -math.sin(tip_alpha)
        dy =  math.cos(tip_alpha)
        
        tangent_angle = math.atan2(dy, dx)
        wing_length = 24
        
        w1_x = tip_x - wing_length * math.cos(tangent_angle - math.pi/7)
        w1_y = tip_y - wing_length * math.sin(tangent_angle - math.pi/7)
        w2_x = tip_x - wing_length * math.cos(tangent_angle + math.pi/7)
        w2_y = tip_y - wing_length * math.sin(tangent_angle + math.pi/7)

        draw.polygon([(tip_x, tip_y), (w1_x, w1_y), (w2_x, w2_y)], fill="#e74c3c")

    # Dibujar las cajas sobre el circulo
    for i, (main_text, sub_text) in enumerate(nodes):
        x1, y1, x2, y2 = boxes[i]
        
        try:
            draw.rounded_rectangle([x1, y1, x2, y2], radius=20, fill="#2c3e50")
        except AttributeError:
            draw.rectangle([x1, y1, x2, y2], fill="#2c3e50")
            
        try:
            mw, mh = font_main.getbbox(main_text)[2] - font_main.getbbox(main_text)[0], font_main.getbbox(main_text)[3] - font_main.getbbox(main_text)[1]
        except:
            mw, mh = font_main.getsize(main_text)
            
        if sub_text:
            try:
                sw, sh = font_sub.getbbox(sub_text)[2] - font_sub.getbbox(sub_text)[0], font_sub.getbbox(sub_text)[3] - font_sub.getbbox(sub_text)[1]
            except:
                sw, sh = font_sub.getsize(sub_text)
                
            total_h = mh + sh + 8
            
            draw.text(((x1+x2)/2 - mw/2, (y1+y2)/2 - total_h/2), main_text, font=font_main, fill="white")
            draw.text(((x1+x2)/2 - sw/2, (y1+y2)/2 - total_h/2 + mh + 8), sub_text, font=font_sub, fill="#bdc3c7")
        else:
            draw.text(((x1+x2)/2 - mw/2, (y1+y2)/2 - mh/2 - 2), main_text, font=font_main, fill="white")

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\ciclo_pensamiento.png"
    img.save(out_path)
    print("Imagen guardada en:", out_path)

if __name__ == "__main__":
    draw_cycle()
