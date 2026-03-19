import subprocess
import osModule

class wingetModule(osModule.osModule): #inherit from osModule to have access to its methods hehehe
    def __init__(self):
        pass #idk why not

    #INSTALL WINGET BY COMMAND. MAN IM SO BAD AT THESE COMMENTS (TOT)
    def direct_install(self, command: str, app_id: str) -> None:
        
        full_command = [
            "winget", command, "--id", app_id, 
            "--silent", "--accept-source-agreements", "--accept-package-agreements"
        ]
        print(f"--Installing {app_id}--")
        
        result = subprocess.run(full_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Installed with success: {app_id}")
        else:
            error_msg = result.stdout if result.stdout else result.stderr #Sometimes winget outputs errors to stdout, sometimes to stderr, so we check both
            print(f"Error installing {app_id}: {error_msg[:200].strip()}...")

    #INSTALL WINGET
    def winget_install(self, data: dict= None) -> None:

        data = self.get_json()

        # Iterate over the apps defined in the JSON and process them
        for app_id, app_data in data.get("apps", {}).items():
            self.direct_install("install", app_id)

            # Check if we need to clean shortcuts based on config of each app
            config = app_data.get("config", {})

            remove_desktop = config.get("desktop_shortcut") is False
            remove_start_menu = config.get("start_menu") is False
            
            if remove_desktop or remove_start_menu:
                osModule.remove_shortcuts(app_id, remove_desktop, remove_start_menu)

        print("\nAll done!")

    #FUNCTION THAT WILL SEARCH AND GIVE A BUNCH OF IDS TO CHOOSE FROM WHEN TYPING AN APPLICATION
    def winget_search(self, data: dict) -> None:
        pass

    #UPDATE WINGET

    ##########################
    ####WORK IN PROGRESS######
    ##########################
    def winget_update(self) -> None:
        print("Updating winget...")
        subprocess.run([
            "winget", "upgrade", "--all", "--silent", "--accept-source-agreements"
        ])

    #FUNCTION TO SWITCH "DESKTOP SHORTCUT" AND "STARTMENU SHORTCUT"
    def configuration(self) -> None:
        pass