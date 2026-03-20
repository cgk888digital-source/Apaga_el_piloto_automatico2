from PIL import Image, ImageDraw, ImageFont

def draw_diagram():
    width, height = 1000, 250
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26)
    except:
        font_main = ImageFont.load_default()

    blocks = ["ERROR", "RECHAZO", "PELIGRO"]
    
    box_w, box_h = 240, 90
    gap = 100
    
    start_x = (width - (len(blocks)*(box_w) + (len(blocks)-1)*gap)) // 2
    y = (height - box_h) // 2

    for i, text in enumerate(blocks):
        x = start_x + i * (box_w + gap)
        
        # Draw box
        try:
            draw.rounded_rectangle([x, y, x+box_w, y+box_h], radius=15, fill="#2c3e50")
        except AttributeError:
            draw.rectangle([x, y, x+box_w, y+box_h], fill="#2c3e50")
            
        # Draw text
        try:
            mw, mh = font_main.getbbox(text)[2] - font_main.getbbox(text)[0], font_main.getbbox(text)[3] - font_main.getbbox(text)[1]
        except:
            mw, mh = font_main.getsize(text)
            
        draw.text((x + box_w/2 - mw/2, y + box_h/2 - mh/2 - 4), text, font=font_main, fill="white")
        
        # Draw equals sign
        if i < len(blocks) - 1:
            eq_x = x + box_w + gap/2
            eq_y = y + box_h/2
            
            line_w = 40
            line_thickness = 8
            y_offset = 8
            
            draw.line([(eq_x - line_w/2, eq_y - y_offset), (eq_x + line_w/2, eq_y - y_offset)], fill="#e74c3c", width=line_thickness)
            draw.line([(eq_x - line_w/2, eq_y + y_offset), (eq_x + line_w/2, eq_y + y_offset)], fill="#e74c3c", width=line_thickness)

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\error_rechazo_peligro.png"
    img.save(out_path)
    print("Imagen guardada en:", out_path)

if __name__ == "__main__":
    draw_diagram()
