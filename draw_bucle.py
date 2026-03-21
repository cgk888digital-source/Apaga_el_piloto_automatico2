import os
import math
from PIL import Image, ImageDraw, ImageFont

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def create_circular_diagram():
    labels = ["Creencia", "Pensamiento", "Emoción", "Acción", "Resultado", "\"¡Lo sabía!\""]
    
    colors = [
        "#2E3B4E", # Dark Blue-Grey
        "#E0533C", # Coral
        "#B93B2C", # Dark Red
        "#A03C12", # Dark Rust
        "#D45D00", # Rust Orange
        "#E48324"  # Orange
    ]
    
    # Make it wider for high res
    width, height = 900, 800
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 20)
        font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 20)
        font_italic = ImageFont.truetype("C:\\Windows\\Fonts\\ariali.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font
        font_italic = font
        
    center_x, center_y = width // 2, height // 2
    radius = 260
    block_w, block_h = 180, 70
    
    # Draw gray circle track underneath
    track_radius = radius
    draw.ellipse([center_x - track_radius, center_y - track_radius, 
                   center_x + track_radius, center_y + track_radius], 
                 outline="#BDC3C7", width=4)
                 
    # Draw arrow heads on the track
    for i in range(6):
        # Positions at halfway between nodes
        angle_deg = -60 + i * 60
        angle_rad = math.radians(angle_deg)
        ax = center_x + track_radius * math.cos(angle_rad)
        ay = center_y + track_radius * math.sin(angle_rad)
        
        tangent_rad = math.radians(angle_deg + 90)
        
        arrow_len, arrow_w = 20, 12
        
        p1x = ax + (arrow_len/2) * math.cos(tangent_rad)
        p1y = ay + (arrow_len/2) * math.sin(tangent_rad)
        
        bcx = ax - (arrow_len/2) * math.cos(tangent_rad)
        bcy = ay - (arrow_len/2) * math.sin(tangent_rad)
        
        normal_rad = angle_rad
        p2x = bcx + arrow_w * math.cos(normal_rad)
        p2y = bcy + arrow_w * math.sin(normal_rad)
        
        p3x = bcx - arrow_w * math.cos(normal_rad)
        p3y = bcy - arrow_w * math.sin(normal_rad)
        
        draw.polygon([(p1x, p1y), (p2x, p2y), (p3x, p3y)], fill="#95A5A6")

    # Draw blocks
    for i, label in enumerate(labels):
        angle_deg = -90 + i * 60
        angle_rad = math.radians(angle_deg)
        
        bx = center_x + radius * math.cos(angle_rad)
        by = center_y + radius * math.sin(angle_rad)
        
        rx = bx - block_w / 2
        ry = by - block_h / 2
        
        fill_color = hex_to_rgb(colors[i])
        try:
            draw.rounded_rectangle([rx, ry, rx + block_w, ry + block_h], radius=15, fill=fill_color)
        except AttributeError:
            draw.rectangle([rx, ry, rx + block_w, ry + block_h], fill=fill_color)
            
        text_bbox = draw.textbbox((0, 0), label, font=font_bold)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        
        text_x = bx - text_w / 2
        text_y = by - text_h / 2 - 5
        
        draw.text((text_x, text_y), label, fill=(255, 255, 255), font=font_bold)
        
    # Removed center text per user request

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes", "diagrama_creencia.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print("Saved circular diagram to", out_path)

if __name__ == '__main__':
    create_circular_diagram()
