import os

def get_folder_structure(base_dirs):
    """Erstellt die Ordnerstruktur als String."""
    structure = []
    for base_dir in base_dirs:
        for root, dirs, files in os.walk(base_dir):
            level = root.replace(base_dir, '').count(os.sep)
            indent = '    ' * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = '    ' * (level + 1)
            for file in files:
                structure.append(f"{subindent}{file}")
    return "\n".join(structure)

def merge_python_files():
    base_dirs = ["src", "assets", "data", "theme"]
    target_file = "temp/merged.py"
    main_file = "main.py"

    # Sicherstellen, dass der Zielordner existiert
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    # Ordnerstruktur generieren
    folder_structure = get_folder_structure(base_dirs)

    with open(target_file, "w", encoding="utf-8") as merged_file:
        # Ordnerstruktur als Kommentar hinzufügen
        merged_file.write("""# Ordnerstruktur:\n"""
)
        for line in folder_structure.split("\n"):
            merged_file.write(f"# {line}\n")
        merged_file.write("\n")

        # main.py hinzufügen
        if os.path.exists(main_file):
            with open(main_file, "r", encoding="utf-8") as main:
                merged_file.write(f"# Inhalt von {main_file}\n")
                merged_file.write(main.read())
                merged_file.write("\n\n")
        else:
            print(f"Warnung: {main_file} nicht gefunden!")

        # Python-Dateien aus src hinzufügen
        for root, _, files in os.walk("src"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as src_file:
                        relative_path = os.path.relpath(file_path, "src")
                        merged_file.write(f"# Inhalt von src/{relative_path}\n")
                        merged_file.write(src_file.read())
                        merged_file.write("\n\n")

if __name__ == "__main__":
    merge_python_files()
