import math
from PIL import Image, ImageDraw, ImageFont

def draw_cycle():
    width, height = 1200, 1100
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 25)
    except:
        try:
             font_main = ImageFont.truetype(r"C:\Windows\Fonts\arialb.ttf", 25)
        except:
             font_main = ImageFont.load_default()

    try:
        font_center = ImageFont.truetype(r"C:\Windows\Fonts\ariali.ttf", 28)
    except:
        font_center = ImageFont.load_default()

    nodes = [
        ("Ego genera amenaza", ""),
        ("Amígdala se activa", ""),
        ("Estrés y miedo", ""),
        ("Pensamientos más negativos", ""),
        ("Más activación de amígdala", "")
    ]

    cx, cy = width / 2, height / 2
    R = 360

    # 5 angles
    angles = [
        -math.pi/2,           # Top (-90)
        -math.pi/10,          # Right (-18)
         math.pi * 3/10,      # Bottom Right (54)
         math.pi * 7/10,      # Bottom Left (126)
         math.pi + math.pi/10 # Left (198)
    ]

    box_w, box_h = 380, 100
    boxes = []
    
    # Colores secuenciales del ciclo asustado
    colors = ["#2c3e50", "#e74c3c", "#c0392b", "#d35400", "#e67e22"]

    for i in range(len(nodes)):
        x = cx + R * math.cos(angles[i]) - box_w/2
        y = cy + R * math.sin(angles[i]) - box_h/2
        boxes.append((x, y, x+box_w, y+box_h))

    # Definimos la funcion de padding para el bounding box
    def point_in_box(px, py, b):
        pad = 5
        return (b[0] - pad <= px <= b[2] + pad) and (b[1] - pad <= py <= b[3] + pad)

    # Dibujar el circulo de fondo que conecta todo
    # El angulo cambia, asi que simplemente dibujamos la elipse general
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline="#bdc3c7", width=6)

    # Dibujar flechas
    for i in range(len(boxes)):
        b = boxes[(i+1)%len(boxes)] # Apunto a la sig caja
        theta_next = angles[(i+1)%len(angles)]
        if theta_next < 0 and angles[i] > 0 and i == len(nodes) - 1:
             theta_next += 2*math.pi # fix crossover jump

        # Encontrar donde la flecha entra a la siguiente caja
        tip_x, tip_y, tip_alpha = cx, cy, theta_next
        
        # Retroceder desde el centro hacia el inicio
        for delta_deg in range(1, 180, 1):
             alpha = theta_next - math.radians(delta_deg)
             px = cx + R * math.cos(alpha)
             py = cy + R * math.sin(alpha)
             if not point_in_box(px, py, b):
                 tip_x, tip_y, tip_alpha = px, py, alpha
                 break

        # Tangente en ese punto
        dx = -math.sin(tip_alpha)
        dy =  math.cos(tip_alpha)
        tangent_angle = math.atan2(dy, dx)
        wing_length = 26
        
        w1_x = tip_x - wing_length * math.cos(tangent_angle - math.pi/7)
        w1_y = tip_y - wing_length * math.sin(tangent_angle - math.pi/7)
        w2_x = tip_x - wing_length * math.cos(tangent_angle + math.pi/7)
        w2_y = tip_y - wing_length * math.sin(tangent_angle + math.pi/7)

        draw.polygon([(tip_x, tip_y), (w1_x, w1_y), (w2_x, w2_y)], fill="#7f8c8d")

    # Dibujar centro
    center_text = "[El ciclo se retroalimenta]"
    try:
        cw, ch = font_center.getbbox(center_text)[2] - font_center.getbbox(center_text)[0], font_center.getbbox(center_text)[3] - font_center.getbbox(center_text)[1]
    except:
        cw, ch = font_center.getsize(center_text)
    draw.text((cx - cw/2, cy - ch/2), center_text, font=font_center, fill="#c0392b")

    # Dibujar las cajas sobre el circulo
    for i, (main_text, sub_text) in enumerate(nodes):
        x1, y1, x2, y2 = boxes[i]
        color = colors[i]
        
        try:
            draw.rounded_rectangle([x1, y1, x2, y2], radius=15, fill=color)
        except AttributeError:
            draw.rectangle([x1, y1, x2, y2], fill=color)
            
        try:
            mw, mh = font_main.getbbox(main_text)[2] - font_main.getbbox(main_text)[0], font_main.getbbox(main_text)[3] - font_main.getbbox(main_text)[1]
        except:
            mw, mh = font_main.getsize(main_text)
            
        draw.text(((x1+x2)/2 - mw/2, (y1+y2)/2 - mh/2 - 2), main_text, font=font_main, fill="white")

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\ciclo_amigdala.png"
    img.save(out_path)
    print("Imagen guardada en:", out_path)

if __name__ == "__main__":
    draw_cycle()
