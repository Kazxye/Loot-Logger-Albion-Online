#!/usr/bin/env python3
"""
Build Script - Gera executáveis do Loot Logger
Usa PyInstaller para criar os .exe

Feito por Kazz

Uso:
    python build.py          # Builda ambos
    python build.py gui      # Builda apenas GUI + CLI
    python build.py web      # Builda apenas Dashboard + CLI
"""

import os
import sys
import shutil
import subprocess

# Cores para output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}  {text}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}\n")


def print_step(text):
    print(f"{Colors.BLUE}[*]{Colors.END} {text}")


def print_success(text):
    print(f"{Colors.GREEN}[✓]{Colors.END} {text}")


def print_error(text):
    print(f"{Colors.RED}[✗]{Colors.END} {text}")


def print_warning(text):
    print(f"{Colors.YELLOW}[!]{Colors.END} {text}")


def check_pyinstaller():
    """Verifica se PyInstaller está instalado."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Instala PyInstaller."""
    print_step("Instalando PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print_success("PyInstaller instalado!")


def clean_build():
    """Limpa diretórios de build anteriores."""
    print_step("Limpando builds anteriores...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    # Remove .spec files
    for f in os.listdir('.'):
        if f.endswith('.spec'):
            os.remove(f)
    
    print_success("Diretórios limpos!")


def build_gui():
    """Builda o executável GUI + CLI."""
    print_header("Building: Loot Logger GUI")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=LootLogger-GUI",
        "--onefile",
        "--windowed",  # Sem console para GUI
        "--icon=assets/icon.ico",
        "--add-data=assets;assets",
        "--add-data=gui;gui",
        "--add-data=core;core",
        "--add-data=handlers;handlers",
        "--add-data=models;models",
        "--add-data=services;services",
        "--add-data=storage;storage",
        "--add-data=utils;utils",
        "--add-data=security;security",
        "--hidden-import=customtkinter",
        "--hidden-import=PIL",
        "--hidden-import=scapy",
        "--hidden-import=scapy.all",
        "--hidden-import=scapy.layers.inet",
        "--collect-all=customtkinter",
        "--collect-all=scapy",
        "main_gui.py"
    ]
    
    print_step("Executando PyInstaller...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print_success("LootLogger-GUI.exe criado com sucesso!")
        return True
    else:
        print_error("Falha ao criar LootLogger-GUI.exe")
        return False


def build_web():
    """Builda o executável Dashboard + CLI."""
    print_header("Building: Loot Logger Dashboard")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=LootLogger-Dashboard",
        "--onefile",
        "--console",  # Com console para ver os logs
        "--icon=assets/icon.ico",
        "--add-data=assets;assets",
        "--add-data=dashboard;dashboard",
        "--add-data=core;core",
        "--add-data=handlers;handlers",
        "--add-data=models;models",
        "--add-data=services;services",
        "--add-data=storage;storage",
        "--add-data=utils;utils",
        "--add-data=security;security",
        "--hidden-import=flask",
        "--hidden-import=flask_socketio",
        "--hidden-import=engineio.async_drivers.threading",
        "--hidden-import=scapy",
        "--hidden-import=scapy.all",
        "--hidden-import=scapy.layers.inet",
        "--collect-all=flask",
        "--collect-all=flask_socketio",
        "--collect-all=scapy",
        "main_web.py"
    ]
    
    print_step("Executando PyInstaller...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print_success("LootLogger-Dashboard.exe criado com sucesso!")
        return True
    else:
        print_error("Falha ao criar LootLogger-Dashboard.exe")
        return False


def copy_to_release():
    """Copia executáveis para pasta release."""
    print_step("Organizando arquivos de release...")
    
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copia executáveis
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        for f in os.listdir(dist_dir):
            if f.endswith('.exe'):
                shutil.copy(os.path.join(dist_dir, f), release_dir)
                print_success(f"Copiado: {f}")
    
    # Copia README
    if os.path.exists("README.md"):
        shutil.copy("README.md", release_dir)
    
    print_success(f"Arquivos organizados em: {os.path.abspath(release_dir)}")


def main():
    print_header("Loot Logger - Build Script")
    print(f"Python: {sys.version}")
    print(f"Diretório: {os.getcwd()}")
    
    # Verifica se está no diretório correto
    if not os.path.exists("main_gui.py"):
        print_error("Execute este script no diretório raiz do projeto!")
        sys.exit(1)
    
    # Verifica/instala PyInstaller
    if not check_pyinstaller():
        print_warning("PyInstaller não encontrado.")
        install_pyinstaller()
    
    # Parse argumentos
    build_target = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    # Limpa builds anteriores
    clean_build()
    
    success = True
    
    if build_target in ["all", "gui"]:
        if not build_gui():
            success = False
    
    if build_target in ["all", "web"]:
        if not build_web():
            success = False
    
    if success:
        copy_to_release()
        print_header("Build Completo!")
        print(f"""
{Colors.GREEN}Executáveis criados:{Colors.END}

  📦 release/LootLogger-GUI.exe
     └─ Interface gráfica + logs no console (quando executado via cmd)
     
  📦 release/LootLogger-Dashboard.exe  
     └─ Dashboard Web (http://localhost:5000) + logs no console

{Colors.YELLOW}Nota:{Colors.END} Execute como Administrador para captura de pacotes funcionar!
        """)
    else:
        print_error("Build falhou! Verifique os erros acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()
