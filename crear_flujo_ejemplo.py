from PIL import Image, ImageDraw, ImageFont
import math

def draw_flowchart():
    width, height = 1150, 1200
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\arialb.ttf", 24)
    except:
        try:
            font_main = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)
        except:
            font_main = ImageFont.load_default()

    try:
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 21)
    except:
        font_sub = ImageFont.load_default()

    nodes = [
        ("1. Estímulo:", "Tu jefe te pide hablar en privado", "#2c3e50"),
        ("2. Pensamiento automático:", '"Me va a despedir" (basado en miedo programado)', "#e74c3c"),
        ("3. Emoción:", "Ansiedad", "#c0392b"),
        ("4. Sentimiento:", "Estrés prolongado (sigues pensando en ello toda la tarde)", "#d35400"),
        ("5. Vibración:", "Energía baja, cortisol alto", "#e67e22"),
        ("6. Comportamiento:", "Llegas nervioso, defensivo, poco claro", "#f39c12"),
        ("7. Resultado:", "La conversación sale mal porque proyectaste inseguridad", "#f1c40f"),
        ("8. Refuerzo:", '"Sabía que algo malo iba a pasar, nunca me va bien"', "#7f8c8d")
    ]

    box_w, box_h = 750, 95
    gap = 40
    start_y = 60
    cx = width // 2 - 80 

    boxes = []
    for i, (main_text, sub_text, color) in enumerate(nodes):
        y = start_y + i * (box_h + gap)
        x1, x2 = cx - box_w//2, cx + box_w//2
        y1, y2 = y, y + box_h
        boxes.append((x1, y1, x2, y2))
        
        try:
            mw, mh = font_main.getbbox(main_text)[2] - font_main.getbbox(main_text)[0], font_main.getbbox(main_text)[3] - font_main.getbbox(main_text)[1]
        except:
            mw, mh = font_main.getsize(main_text)
            
        if sub_text:
            try:
                sw, sh = font_sub.getbbox(sub_text)[2] - font_sub.getbbox(sub_text)[0], font_sub.getbbox(sub_text)[3] - font_sub.getbbox(sub_text)[1]
            except:
                sw, sh = font_sub.getsize(sub_text)
            total_h = mh + sh + 10
            ty_main = y + box_h/2 - total_h/2
            ty_sub = ty_main + mh + 10
        else:
            total_h = mh
            ty_main = y + box_h/2 - total_h/2 - 2
            ty_sub = None

        try:
            draw.rounded_rectangle([x1, y1, x2, y2], radius=15, fill=color)
        except AttributeError:
            draw.rectangle([x1, y1, x2, y2], fill=color)
            
        draw.text((cx - mw/2, ty_main), main_text, font=font_main, fill="white")
        if ty_sub is not None:
            # If the text is quotes, draw it a little lighter or italic? We'll just draw it nicely formatted
            draw.text((cx - sw/2, ty_sub), sub_text, font=font_sub, fill="#ecf0f1")

        if i < len(nodes) - 1:
            arr_y1 = y2
            arr_y2 = y2 + gap
            draw.line([(cx, arr_y1), (cx, arr_y2)], fill="#bdc3c7", width=6)
            draw.polygon([(cx, arr_y2), (cx - 10, arr_y2 - 12), (cx + 10, arr_y2 - 12)], fill="#bdc3c7")

    n1 = boxes[1] 
    n7 = boxes[7] 
    
    RightX = cx + box_w//2 + 90
    
    draw.line([(n7[2], (n7[1]+n7[3])/2), (RightX, (n7[1]+n7[3])/2)], fill="#e74c3c", width=8)
    draw.line([(RightX, (n7[1]+n7[3])/2), (RightX, (n1[1]+n1[3])/2)], fill="#e74c3c", width=8)
    draw.line([(RightX, (n1[1]+n1[3])/2), (n1[2], (n1[1]+n1[3])/2)], fill="#e74c3c", width=8)
    
    draw.polygon([(n1[2], (n1[1]+n1[3])/2), 
                  (n1[2] + 16, (n1[1]+n1[3])/2 - 14), 
                  (n1[2] + 16, (n1[1]+n1[3])/2 + 14)], fill="#e74c3c")
                  
    text_loop = "EL CICLO SE REPITE LA PRÓXIMA VEZ"
    
    try:
        th = font_sub.getbbox("A")[3] - font_sub.getbbox("A")[1]
    except:
        th = font_sub.getsize("A")[1]
        
    total_text_height = len(text_loop.replace(' ', '')) * (th + 2)
    start_text_y = ((n1[1]+n1[3])/2 + (n7[1]+n7[3])/2)/2 - total_text_height/2
    
    idx_y = 0
    for char in text_loop:
        if char == ' ':
            idx_y += th/2
            continue
        try:
            cw = font_sub.getbbox(char)[2] - font_sub.getbbox(char)[0]
        except:
            cw = font_sub.getsize(char)[0]
            
        draw.text((RightX + 25 - cw/2, start_text_y + idx_y), char, font=font_sub, fill="#c0392b")
        idx_y += (th + 2)

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\ejemplo_real.png"
    img.save(out_path)
    print("Imagen generada en:", out_path)

if __name__ == "__main__":
    draw_flowchart()
