#!/usr/bin/env python3
"""
AO Loot Logger - GUI Version
Albion Online Loot Logger com interface gráfica moderna

Feito por Kazz

Baseado no projeto ao-loot-logger de matheussampaio
https://github.com/matheussampaio/ao-loot-logger

Requer: Npcap (Windows) ou libpcap (Linux)
Executar como Administrador/root

Open Source Version - https://github.com/Kazxye/ao-loot-logger
"""

import sys
import os
import ctypes

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def setup_windows_app_id():
    """Configura o AppUserModelID para o ícone correto na barra de tarefas."""
    if sys.platform == 'win32':
        try:
            app_id = "kazz.lootlogger.app.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except:
            pass


def check_admin():
    """Verifica se está rodando como admin (Windows)."""
    if sys.platform == 'win32':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    return True  # Linux/Mac não verifica aqui


def request_admin():
    """Solicita elevação de privilégios (Windows)."""
    if sys.platform == 'win32':
        # Re-executa como admin
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            " ".join(sys.argv), 
            None, 
            1
        )
        sys.exit(0)


def main():
    """Função principal."""
    
    # Configura AppUserModelID ANTES de qualquer coisa (para ícone correto)
    setup_windows_app_id()
    
    print("[INFO] Iniciando Loot Logger...")
    
    # Verifica admin no Windows
    if sys.platform == 'win32' and not check_admin():
        print("Este programa precisa ser executado como Administrador.")
        print("Solicitando elevação de privilégios...")
        
        try:
            request_admin()
        except Exception as e:
            print(f"Erro ao solicitar privilégios: {e}")
            print("\nPor favor, execute manualmente como Administrador:")
            print("  1. Clique com botão direito no arquivo")
            print("  2. Selecione 'Executar como administrador'")
            input("\nPressione Enter para sair...")
            sys.exit(1)
    
    # Importa e inicia GUI
    try:
        print("[INFO] Carregando interface...")
        from gui import run_app
        print("[INFO] Interface carregada, iniciando...")
        run_app()
    
    except ImportError as e:
        print(f"Erro ao importar módulos: {e}")
        print("\nVerifique se todas as dependências estão instaladas:")
        print("  pip install customtkinter scapy requests pillow")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")
        sys.exit(1)


if __name__ == "__main__":
    main()
