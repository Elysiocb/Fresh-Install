import os

#FUNCTION TO CLEAN SHORTCUTS ON DESKTOP AND START MENU
def cleanup_shortcuts(app_id: str, remove_desktop: bool, remove_start_menu: bool) -> None:

    app_name_keyword = app_id.split('.')[-1].lower()#get the last part of the app_id as a keyword to identify shortcuts
    
    paths_to_check = []

    if remove_desktop:
        paths_to_check.extend([ #adds this paths to the list
            os.path.expanduser("~\\Desktop"), #User's desktop path
            os.path.join(os.environ.get("PUBLIC", "C:\\Users\\Public"), "Desktop") #Public desktop path
        ])

    if remove_start_menu:
        paths_to_check.extend([ #adds this paths to the list
            os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"), #User's start menu path
            os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), "Microsoft\\Windows\\Start Menu\\Programs") #Public start menu path
        ])

    for base_path in paths_to_check:
        if not os.path.exists(base_path): #If the path doesn't exist, skip it
            continue

        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".lnk") and app_name_keyword in file.lower(): #Checks if the file is a shortcut and contains the app name keyword
                    file_path = os.path.join(root, file) #Full path to the shortcut
                    try:
                        os.remove(file_path) #Removes the shortcut
                        print(f"Shortcut removed: {file_path}")
                        if dry_run:
                            print(f"[DRY RUN] Atalho seria removido: {file_path}")
                        else:
                            os.remove(file_path) #Removes the shortcut
                            print(f"Shortcut removed: {file_path}")
                    except Exception as e: #error meh why not
                        print(f"Failed to remove shortcut {file_path}: {e}")