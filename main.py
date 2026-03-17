#IMPORTS
import json
import os

#MODULES
import cleanModule
import wingetModule

#FUNCTION
def main() -> None:
    if not os.path.exists('applist.json'):
        print("Failed to find 'applist.json'.")
        return

    try:
        with open('applist.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in 'applist.json'\nDetails: {e}")
        return

    # Iterate over the apps defined in the JSON and process them
    for app_id, app_data in data.get("apps", {}).items():
        wingetModule.install_winget("install", app_id)

        # Check if we need to clean shortcuts based on config of each app
        config = app_data.get("config", {})

        remove_desktop = config.get("desktop_shortcut") is False
        remove_start_menu = config.get("start_menu") is False
        
        if remove_desktop or remove_start_menu:
            cleanModule.cleanup_shortcuts(app_id, remove_desktop, remove_start_menu)

    print("\nAll done!")

#ENTRY POINT
if __name__ == "__main__":
    main()