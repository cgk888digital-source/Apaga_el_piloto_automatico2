import os
import glob
import re

def fix_content(content):
    lines = content.split('\n')
    new_lines = []
    
    # Track numbering per section? 
    # Actually, let's just ensure they are sequential within the whole file for now, 
    # or detect resets if there is a header.
    
    in_numbered_list = False
    current_num = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            continue
            
        # 1. Numeración
        num_match = re.match(r'^(\s*)(\d+)\.\s+', line)
        if num_match:
            indent = num_match.group(1)
            num = int(num_match.group(2))
            
            # Si es el primer número que vemos o si el salto es razonable
            if not in_numbered_list:
                in_numbered_list = True
                current_num = num
            else:
                # Si estamos en una lista, forzamos la secuencia
                # A menos que sea un reset (empieza en 1 otra vez)
                if num == 1:
                    current_num = 1
                else:
                    current_num += 1
                    line = f"{indent}{current_num}. " + line[len(indent)+len(str(num))+2:]
        else:
            # Si no es un número, pero hay mucho texto y no hay un header, seguimos en la lista?
            # No, las listas numeradas suelen estar juntas.
            # Pero en este libro hay párrafos entre medio. 
            # Si hay un header, reseteamos.
            if stripped.startswith('#'):
                in_numbered_list = False
                current_num = 0

        # 2. Puntos finales
        # No añadir si:
        # - Ya tiene puntuación
        # - Es un header
        # - Es una imagen o tag o tabla
        # - Termina en una nota especial o es muy corta
        
        # Saltamos líneas vacías ya handled
        line_to_check = line.rstrip()
        last_char = line_to_check[-1] if line_to_check else ''
        
        if (last_char and 
            not last_char in '.:;?!-)]}>' and 
            not line_to_check.endswith('**') and # A veces termina en negrita sin cerrar? no. 
            # Pero si termina en **, el char anterior es el que importa.
            not stripped.startswith('#') and
            not stripped.startswith('!') and
            not stripped.startswith('[') and
            not stripped.startswith('---') and
            not stripped.startswith('|')):
            
            # Verificar si termina en negrita o cursiva
            if line_to_check.endswith('**') or line_to_check.endswith('*') or line_to_check.endswith('_'):
                # Añadir punto ANTES de las marcas si es markdown (o después?)
                # Normalmente después: **texto**.
                line_to_check += "."
            else:
                line_to_check += "."
                
        new_lines.append(line_to_check)
        
    return '\n'.join(new_lines)

def process_files():
    base_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\capitulos"
    files = glob.glob(os.path.join(base_dir, "*.md"))
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Aplicamos fijaciones
        fixed = fix_content(content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(fixed)
        print(f"Processed {os.path.basename(f)}")

if __name__ == "__main__":
    process_files()
