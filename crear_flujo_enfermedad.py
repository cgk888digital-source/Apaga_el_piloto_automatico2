from PIL import Image, ImageDraw, ImageFont

def draw_diagram():
    width, height = 1300, 800
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\arialb.ttf", 26)
    except:
        try:
            font_main = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
        except:
            font_main = ImageFont.load_default()

    try:
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 24)
    except:
        font_sub = ImageFont.load_default()

    data = [
        ("Miedo crónico", "Riñones, vejiga, sistema urinario", "#8e44ad", "#34495e"),
        ("Ira reprimida", "Hígado, dolores de cabeza, hipertensión", "#c0392b", "#34495e"),
        ("Tristeza no procesada", "Problemas respiratorios, baja inmunidad", "#2980b9", "#34495e"),
        ("Resentimiento", "Problemas digestivos, úlceras", "#d35400", "#34495e"),
        ("Estrés crónico", "Inflamación sistémica, autoinmunes", "#7f8c8d", "#34495e")
    ]

    left_w = 450
    right_w = 600
    box_h = 95
    gap_y = 40
    start_y = 60

    left_cx = width // 2 - 380
    right_cx = width // 2 + 250

    for i, (left_text, right_text, color_l, color_r) in enumerate(data):
        y = start_y + i * (box_h + gap_y)
        
        # Left Box
        lx1, lx2 = left_cx - left_w//2, left_cx + left_w//2
        ly1, ly2 = y, y + box_h
        try:
            draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=15, fill=color_l)
        except AttributeError:
            draw.rectangle([lx1, ly1, lx2, ly2], fill=color_l)
        
        try:
            mw, mh = font_main.getbbox(left_text)[2] - font_main.getbbox(left_text)[0], font_main.getbbox(left_text)[3] - font_main.getbbox(left_text)[1]
        except:
            mw, mh = font_main.getsize(left_text)
        draw.text((left_cx - mw/2, y + box_h/2 - mh/2 - 2), left_text, font=font_main, fill="white")

        # Right Box
        rx1, rx2 = right_cx - right_w//2, right_cx + right_w//2
        ry1, ry2 = y, y + box_h
        try:
            draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=15, fill=color_r)
        except AttributeError:
            draw.rectangle([rx1, ry1, rx2, ry2], fill=color_r)
        
        try:
            sw, sh = font_sub.getbbox(right_text)[2] - font_sub.getbbox(right_text)[0], font_sub.getbbox(right_text)[3] - font_sub.getbbox(right_text)[1]
        except:
            sw, sh = font_sub.getsize(right_text)
        draw.text((right_cx - sw/2, y + box_h/2 - sh/2 - 2), right_text, font=font_sub, fill="white")

        # Arrow
        arr_x1 = lx2 + 10
        arr_x2 = rx1 - 20
        arr_y = y + box_h//2
        draw.line([(arr_x1, arr_y), (arr_x2, arr_y)], fill="#bdc3c7", width=6)
        draw.polygon([(arr_x2, arr_y), (arr_x2 - 12, arr_y - 10), (arr_x2 - 12, arr_y + 10)], fill="#bdc3c7")

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\bloques_enfermedad.png"
    img.save(out_path)
    print("Imagen generada en:", out_path)

if __name__ == "__main__":
    draw_diagram()
