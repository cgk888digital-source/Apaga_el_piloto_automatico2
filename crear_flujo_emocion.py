from PIL import Image, ImageDraw, ImageFont

def draw_flowchart():
    width, height = 1000, 950
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
    except:
        font_main = ImageFont.load_default()

    try:
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
    except:
        font_sub = ImageFont.load_default()

    nodes = [
        ("PENSAMIENTO", "", "#34495e"),
        ("EMOCIÓN", "(30-90 segundos de química corporal)", "#e74c3c"),
        ("Si agregas MÁS PENSAMIENTOS", "sobre la emoción", "#c0392b"),
        ("SENTIMIENTO", "(emoción prolongada)", "#d35400"),
        ("ESTADO EMOCIONAL", "(sentimientos habituales)", "#e67e22"),
        ("PERSONALIDAD", "(estados emocionales crónicos)", "#f39c12")
    ]

    box_w, box_h = 800, 95
    gap = 40
    start_y = 60
    cx = width // 2

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
            draw.text((cx - sw/2, ty_sub), sub_text, font=font_sub, fill="#ecf0f1")

        if i < len(nodes) - 1:
            arr_y1 = y2
            arr_y2 = y2 + gap
            draw.line([(cx, arr_y1), (cx, arr_y2)], fill="#bdc3c7", width=6)
            draw.polygon([(cx, arr_y2), (cx - 10, arr_y2 - 12), (cx + 10, arr_y2 - 12)], fill="#bdc3c7")

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\proceso_emocional.png"
    img.save(out_path)
    print("Imagen generada en:", out_path)

if __name__ == "__main__":
    draw_flowchart()
