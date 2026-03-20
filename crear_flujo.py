from PIL import Image, ImageDraw, ImageFont

def draw_flowchart():
    width, height = 1100, 1200
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26)
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 20)
    except:
        font_main = ImageFont.load_default()
        font_sub = font_main

    nodes = [
        ("Estímulo", "(interno o externo)", "#2c3e50"),
        ("Pensamiento automático", "(basado en programación pasada)", "#e74c3c"),
        ("Emoción reactiva", "(generalmente negativa)", "#c0392b"),
        ("Sentimiento prolongado", "", "#d35400"),
        ("Vibración / Energía baja", "", "#e67e22"),
        ("Comportamiento reactivo", "", "#f39c12"),
        ("Resultados", "(confirman el pensamiento original)", "#f1c40f"),
        ("Refuerzo de la programación", "", "#7f8c8d")
    ]

    box_w, box_h = 650, 90
    gap = 40
    start_y = 60
    cx = width // 2 - 80 # Shift left slightly to make room for return arrow

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
            total_h = mh + sh + 8
            ty_main = y + box_h/2 - total_h/2
            ty_sub = ty_main + mh + 8
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
            draw.text((cx - sw/2, ty_sub), sub_text, font=font_sub, fill="#ecf0f1")

        if i < len(nodes) - 1:
            arr_y1 = y2
            arr_y2 = y2 + gap
            draw.line([(cx, arr_y1), (cx, arr_y2)], fill="#95a5a6", width=6)
            draw.polygon([(cx, arr_y2), (cx - 10, arr_y2 - 12), (cx + 10, arr_y2 - 12)], fill="#95a5a6")

    n1 = boxes[1] 
    n7 = boxes[7] 
    
    RightX = cx + box_w//2 + 90
    
    draw.line([(n7[2], (n7[1]+n7[3])/2), (RightX, (n7[1]+n7[3])/2)], fill="#e74c3c", width=8)
    draw.line([(RightX, (n7[1]+n7[3])/2), (RightX, (n1[1]+n1[3])/2)], fill="#e74c3c", width=8)
    draw.line([(RightX, (n1[1]+n1[3])/2), (n1[2], (n1[1]+n1[3])/2)], fill="#e74c3c", width=8)
    
    draw.polygon([(n1[2], (n1[1]+n1[3])/2), 
                  (n1[2] + 16, (n1[1]+n1[3])/2 - 14), 
                  (n1[2] + 16, (n1[1]+n1[3])/2 + 14)], fill="#e74c3c")
                  
    text_loop = "EL CICLO SE REPITE"
    
    # We will draw the text letter by letter vertically to look awesome!
    try:
        th = font_sub.getbbox("A")[3] - font_sub.getbbox("A")[1]
    except:
        th = font_sub.getsize("A")[1]
        
    total_text_height = len(text_loop) * (th + 2)
    start_text_y = ((n1[1]+n1[3])/2 + (n7[1]+n7[3])/2)/2 - total_text_height/2
    
    for idx, char in enumerate(text_loop):
        try:
            cw = font_sub.getbbox(char)[2] - font_sub.getbbox(char)[0]
        except:
            cw = font_sub.getsize(char)[0]
            
        draw.text((RightX + 25 - cw/2, start_text_y + idx*(th+2)), char, font=font_sub, fill="#c0392b")

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\ciclo_vicioso.png"
    img.save(out_path)
    print("Imagen generada en:", out_path)

if __name__ == "__main__":
    draw_flowchart()
