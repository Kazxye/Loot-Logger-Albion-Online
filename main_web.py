#!/usr/bin/env python3
"""
AO Loot Logger - Dashboard Only Mode
Albion Online Loot Logger apenas com dashboard web (sem GUI)

Feito por Kazz

Este script inicia apenas o sniffer + dashboard web.
Útil para quem prefere usar apenas o browser.
Dashboard disponível em http://localhost:5000

Open Source Version - https://github.com/Kazxye/ao-loot-logger
"""

import sys
import os
import ctypes
import signal

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def setup_windows_app_id():
    """Configura o AppUserModelID."""
    if sys.platform == 'win32':
        try:
            app_id = "kazz.lootlogger.web.1.0"
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
    return True


def request_admin():
    """Solicita elevação de privilégios (Windows)."""
    if sys.platform == 'win32':
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
    
    setup_windows_app_id()
    
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           Loot Logger - Dashboard Web Mode                 ║")
    print("║                      by Kazz                               ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║  Dashboard: http://localhost:5000                          ║")
    print("║  Pressione Ctrl+C para parar                               ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Verifica admin no Windows
    if sys.platform == 'win32' and not check_admin():
        print("[!] Este programa precisa ser executado como Administrador.")
        print("[!] Solicitando elevação de privilégios...")
        
        try:
            request_admin()
        except Exception as e:
            print(f"[ERRO] Erro ao solicitar privilégios: {e}")
            input("\nPressione Enter para sair...")
            sys.exit(1)
    
    sniffer = None
    
    def cleanup(signum=None, frame=None):
        """Limpa recursos ao sair."""
        print("\n[INFO] Encerrando...")
        if sniffer:
            sniffer.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    try:
        # Carrega serviços
        print("[INFO] Carregando serviços...")
        from services import items_service, tier_service, config_service, events_config
        
        config_service.load()
        events_config.load()
        items_service.locale = config_service.language
        items_service.load()
        
        # Inicia Dashboard
        print("[INFO] Iniciando Dashboard Web...")
        from dashboard import dashboard_server
        
        dashboard_server.inject_tier_service(tier_service)
        dashboard_server.start(open_browser=True)
        print(f"[OK] Dashboard disponível em http://localhost:5000")
        
        # Inicia Sniffer
        print("[INFO] Iniciando captura de pacotes...")
        from core import Sniffer
        from handlers import data_handler
        
        sniffer = Sniffer()
        
        # Registra callback do dashboard
        data_handler.on_loot(dashboard_server.on_loot_event)
        
        # Conecta eventos
        sniffer.on_event(data_handler.handle_event)
        sniffer.on_request(data_handler.handle_request)
        sniffer.on_response(data_handler.handle_response)
        
        def on_albion_online():
            print("[OK] Albion Online detectado! Monitorando...")
            dashboard_server.set_status('online')
        
        def on_albion_offline():
            print("[!] Albion Online não detectado")
            dashboard_server.set_status('offline')
        
        sniffer.on_online(on_albion_online)
        sniffer.on_offline(on_albion_offline)
        
        sniffer.start()
        dashboard_server.set_status('connecting')
        print("[OK] Captura iniciada! Aguardando Albion Online...")
        print()
        print("-" * 60)
        print("  Os loots aparecerão abaixo e no dashboard web")
        print("-" * 60)
        print()
        
        # Mantém rodando
        while True:
            try:
                import time
                time.sleep(1)
            except KeyboardInterrupt:
                cleanup()
                break
    
    except ImportError as e:
        print(f"[ERRO] Erro ao importar módulos: {e}")
        print("\nVerifique se todas as dependências estão instaladas:")
        print("  pip install scapy requests flask flask-socketio")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    except Exception as e:
        print(f"[ERRO] Erro ao iniciar: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")
        sys.exit(1)


if __name__ == "__main__":
    main()
