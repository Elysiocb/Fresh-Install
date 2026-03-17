import os

def cleanup_shortcuts(app_id: str, remove_desktop: bool, remove_start_menu: bool) -> None:
    """Procura e remove atalhos do Desktop e Menu Iniciar baseados no nome do app."""
    # Extrai a última parte do ID (ex: Mozzila.Firefox -> firefox)
    app_name_keyword = app_id.split('.')[-1].lower()
    
    paths_to_check = []
    if remove_desktop:
        paths_to_check.extend([
            os.path.expanduser("~\\Desktop"),
            os.path.join(os.environ.get("PUBLIC", "C:\\Users\\Public"), "Desktop")
        ])
    if remove_start_menu:
        paths_to_check.extend([
            os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"),
            os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), "Microsoft\\Windows\\Start Menu\\Programs")
        ])

    for base_path in paths_to_check:
        if not os.path.exists(base_path):
            continue
        # Busca recursivamente por atalhos (.lnk)
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".lnk") and app_name_keyword in file.lower():
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"🗑️ Atalho indesejado removido: {file_path}")
                    except Exception as e:
                        print(f"⚠️ Falha ao remover atalho {file_path}: {e}")