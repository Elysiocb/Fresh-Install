#IMPORTS
import json
import subprocess
import os

#MODULES
import configModule

def run_winget(command: str, app_id: str) -> None:
    """Executa o comando winget e retorna o resultado."""
    full_command = [
        "winget", command, "--id", app_id, 
        "--silent", "--accept-source-agreements", "--accept-package-agreements"
    ]
    print(f"--- Processando: {app_id} ---")
    
    result = subprocess.run(full_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Sucesso: {app_id}")
    else:
        # Se o erro for porque já está instalado, o winget avisa
        error_msg = result.stdout if result.stdout else result.stderr
        print(f"⚠️ Aviso/Erro em {app_id}: {error_msg[:100].strip()}...")

def main() -> None:
    if not os.path.exists('applist.json'):
        print("❌ Erro: Arquivo applist.json não encontrado!")
        return

    try:
        with open('applist.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erro: Arquivo apps.json possui formato JSON inválido!\nDetalhes: {e}")
        return

    # Itera sobre os apps 
    for app_id, app_data in data.get("apps", {}).items():
        print(f"Instalando {app_id}")
        run_winget("install", app_id)

        # Verifica as configurações e limpa atalhos se o usuário optou por "false"
        config = app_data.get("config", {})

        remove_desktop = config.get("desktop_shortcut") is False
        remove_start_menu = config.get("start_menu") is False
        
        if remove_desktop or remove_start_menu:
            configModule.cleanup_shortcuts(app_id, remove_desktop, remove_start_menu)

    print("\n✨ Processo finalizado! Garantindo atualizações finais...")
    subprocess.run([
        "winget", "upgrade", "--all", "--silent", "--accept-source-agreements"
    ])

if __name__ == "__main__":
    main()