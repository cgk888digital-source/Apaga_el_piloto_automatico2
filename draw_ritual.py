import os
import math
from PIL import Image, ImageDraw, ImageFont

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def create_circular_diagram():
    labels = [
        "1. Silencio y\nrespiración\n(2 min)",
        "2. Lee tus\nintenciones\nen voz alta",
        "3. Visualiza\ncon emoción\n(3-5 min)",
        "4. Intención\ndel día\n('Hoy me...')",
        "5. Acción\nconcreta\nen el día"
    ]
    
    colors = [
        "#2C3E50", # Dark blue
        "#8E44AD", # Purple
        "#E67E22", # Orange
        "#F39C12", # Yellow-orange
        "#3498DB", # Light blue
    ]
    
    width, height = 800, 800
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 18)
        font_italic = ImageFont.truetype("C:\\Windows\\Fonts\\ariali.ttf", 26)
    except IOError:
        font_bold = ImageFont.load_default()
        font_italic = ImageFont.load_default()
        
    center_x, center_y = width // 2, height // 2
    radius = 240
    block_w, block_h = 170, 90
    
    # Draw gray circle track underneath
    track_radius = radius
    draw.ellipse([center_x - track_radius, center_y - track_radius, 
                   center_x + track_radius, center_y + track_radius], 
                 outline="#BDC3C7", width=4)
                 
    # Draw arrow heads on the track
    for i in range(5):
        # Positions at halfway between nodes
        angle_deg = -90 + i * 72 + 36 # Halfway
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
        angle_deg = -90 + i * 72
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
            
        # Draw multiline text (centered)
        text_bbox = draw.multiline_textbbox((0, 0), label, font=font_bold, align="center")
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        
        text_x = bx - text_w / 2
        text_y = by - text_h / 2 - 4
        
        draw.multiline_text((text_x, text_y), label, fill=(255, 255, 255), font=font_bold, align="center")
        
    # Draw center text
    center_label = "Ritual de\nla Mañana"
    text_bbox = draw.multiline_textbbox((0, 0), center_label, font=font_italic, align="center")
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    draw.multiline_text((center_x - text_w/2, center_y - text_h/2), center_label, fill="#2C3E50", font=font_italic, align="center")

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes", "ritual_manana.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print("Saved circular diagram to", out_path)

if __name__ == '__main__':
    create_circular_diagram()
