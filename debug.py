import re
import sys

def test_grouping():
    file_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\capitulos\capitulo_03.md"
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    current_group_text = []
    waiting_for_next = False
    in_outro = False
    
    chapter_idx = 0
    group_num = 1
    
    for chapter_idx, line in enumerate(lines):
        if "Ejercicio 3:" in line or "Ejemplo completo:" in line or "Estoy notando" in line:
            # We are in the interesting area
            pass
            
        # Simplified parsing logic
        is_list_item = bool(re.match(r'^([*_]*)(\d+\.)\s+|^([-*]\s*)', line))
        is_header = False
        
        if (len(line) < 120 and (line[0].isupper() or line[0] in "¿¡" or line[0].isdigit()) and not line.endswith('.') and not line.startswith('- ') and not line.startswith('* ')):
            is_header = True

        def flush_group(reason):
            nonlocal current_group_text, group_num, waiting_for_next
            if current_group_text and any("Ejemplo completo" in x or "Estoy notando" in x for x in current_group_text):
                print(f"\n--- FLUSHING GROUP {group_num} at line '{line[:30]}' (Reason: {reason}) ---")
                for item in current_group_text:
                    print("  ", item[:50])
            if current_group_text:
                current_group_text.clear()
                group_num += 1
            waiting_for_next = False

        if is_header:
            waiting_for_next = False
            has_normal = True # assume it has normal text
            if has_normal:
                flush_group("is_header with normal text")
            current_group_text.append(line)
            
        elif is_list_item:
            was_waiting = waiting_for_next
            waiting_for_next = False
            if len(current_group_text) > 15 and not was_waiting:
                flush_group("list_item limit > 15 and not was_waiting")
            current_group_text.append(line)
            
        elif line == '---':
            flush_group("--- separator")
        else:
            # regular text
            is_bold_header = bool(re.match(r'^[*_]{2,}[^*_]+[*_]{2,}$', line.strip()))
            is_quote = bool(re.match(r'^[*_]*["\u201C]', line))
            
            if "Antes de pasar al Capítulo" in line:
                in_outro = True
                
            current_group_text.append(line)
            if line.strip(' *_').endswith(':') or is_quote or is_bold_header or in_outro:
                waiting_for_next = True
            else:
                flush_group("normal text flush")

test_grouping()
