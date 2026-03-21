import os
import glob

def show_structure():
    base_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\capitulos"
    if not os.path.exists(base_dir):
        print("Directory not found.")
        return
        
    files = sorted([f for f in os.listdir(base_dir) if f.startswith("capitulo_") and f.endswith(".md")])
    
    print("ESTRUCTURA DEL LIBRO:\n")
    for f in files:
        filepath = os.path.join(base_dir, f)
        title = "Sin título"
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith("# "):
                    title = line[2:]
                    break
        print(f"- {f}: {title}")

if __name__ == "__main__":
    show_structure()
