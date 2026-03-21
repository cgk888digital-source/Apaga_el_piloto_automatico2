import re

line1 = '**Ejemplo completo:**'
line2 = '1. *"Estoy notando que hay enojo"*'
line3 = '2. *"Es frustración específicamente"*'
line4 = '3. *"La siento en mi pecho y mandíbula. Se siente caliente y tensa"*'
line5 = '4. *"Elijo respirar profundamente y expresar mi límite con claridad y calma"*'

def test_line(line):
    print("---")
    print("Line:", line)
    
    is_list_item = bool(re.match(r'^([*_]*)(\d+\.)\s+|^([-*]\s*)', line))
    is_header = False
    
    if (len(line) < 120 and (line[0].isupper() or line[0] in "¿¡" or line[0].isdigit()) and not line.endswith('.') and not line.startswith('- ') and not line.startswith('* ')):
        is_header = True
        
    is_bold_header = bool(re.match(r'^[*_]{2,}[^*_]+[*_]{2,}$', line.strip()))
    is_quote = bool(re.match(r'^[*_]*["\u201C]', line))
    ends_with_colon = line.strip(' *_').endswith(':')
    
    print(f"is_header: {is_header}")
    print(f"is_list_item: {is_list_item}")
    print(f"is_bold_header: {is_bold_header}")
    print(f"is_quote: {is_quote}")
    print(f"ends_with_colon: {ends_with_colon}")

test_line(line1)
test_line(line2)
test_line(line3)

