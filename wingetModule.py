import subprocess

#INSTALL WINGET
def install_winget(command: str, app_id: str) -> None:
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

#UPDATE WINGET

##########################
####WORK IN PROGRESS######
##########################
def update_winget() -> None:
    print("Updating winget...")
    subprocess.run([
        "winget", "upgrade", "--all", "--silent", "--accept-source-agreements"
    ])