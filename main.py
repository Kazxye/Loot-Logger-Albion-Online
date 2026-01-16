#!/usr/bin/env python3
"""
AO Loot Logger - Albion Online Loot Logger em Python
Versão simplificada (terminal) com webhook Discord

Baseado no projeto ao-loot-logger de matheussampaio
https://github.com/matheussampaio/ao-loot-logger

Requer: Npcap (Windows) ou libpcap (Linux)
Executar como Administrador/root
"""

import sys
import os
import json
import signal
from datetime import datetime
from typing import List

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import AlbionSniffer
from handlers import data_handler
from services import items_service, events_config, discord_service
from models import LootEvent

# ============================================
# CONFIGURAÇÃO
# ============================================

VERSION = "1.0.0"
TITLE = f"AO Loot Logger Python - v{VERSION}"

# Webhook do Discord
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1450577850628309224/xqwPgGtm5KlmMxE2Net7clKYts6XMcF9Ahv5FWxEpq6JN0N3Je9TYWXrG30v3jhZ9KKj"

# ============================================
# CORES PARA TERMINAL
# ============================================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def green(text): return f"{Colors.GREEN}{text}{Colors.RESET}"
def red(text): return f"{Colors.RED}{text}{Colors.RESET}"
def yellow(text): return f"{Colors.YELLOW}{text}{Colors.RESET}"
def cyan(text): return f"{Colors.CYAN}{text}{Colors.RESET}"
def gray(text): return f"{Colors.GRAY}{text}{Colors.RESET}"
def bold(text): return f"{Colors.BOLD}{text}{Colors.RESET}"


# ============================================
# VARIÁVEIS GLOBAIS
# ============================================

loot_events: List[LootEvent] = []
log_file = None
log_filename = None


# ============================================
# FUNÇÕES DE LOG
# ============================================

def create_log_file():
    """Cria um novo arquivo de log."""
    global log_file, log_filename
    
    if log_file:
        log_file.close()
    
    now = datetime.now()
    log_filename = f"loot-events-{now.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    
    log_file = open(log_filename, 'w', encoding='utf-8')
    
    # Escreve header
    header = "timestamp_utc;looted_by__alliance;looted_by__guild;looted_by__name;item_id;item_name;quantity;looted_from__alliance;looted_from__guild;looted_from__name"
    log_file.write(header + "\n")
    log_file.flush()
    
    return log_filename


def write_log(event: LootEvent):
    """Escreve um evento de loot no arquivo."""
    global log_file
    
    if log_file is None:
        create_log_file()
    
    line = ";".join([
        event.timestamp.isoformat(),
        event.looted_by.alliance,
        event.looted_by.guild,
        event.looted_by.name,
        event.item_id,
        event.item_name,
        str(event.quantity),
        event.looted_from.alliance,
        event.looted_from.guild,
        event.looted_from.name
    ])
    
    log_file.write(line + "\n")
    log_file.flush()


def export_json():
    """Exporta eventos para JSON."""
    if not loot_events:
        print(yellow("[AVISO] Nenhum evento para exportar."))
        return
    
    filename = f"loot-export-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([e.to_dict() for e in loot_events], f, indent=2, ensure_ascii=False)
    
    print(green(f"[OK] Exportado {len(loot_events)} eventos para {filename}"))


# ============================================
# CALLBACKS
# ============================================

def on_loot(event: LootEvent):
    """Callback quando um loot é detectado."""
    global loot_events
    
    # Adiciona à lista
    loot_events.append(event)
    
    # Escreve no arquivo
    write_log(event)
    
    # Formata para terminal
    time_str = event.timestamp.strftime("%H:%M:%S")
    
    # Formata jogador que pegou (verde)
    looted_by_str = ""
    if event.looted_by.alliance:
        looted_by_str += gray(f"{{{event.looted_by.alliance}}}") + " "
    if event.looted_by.guild:
        looted_by_str += gray(f"[{event.looted_by.guild}]") + " "
    looted_by_str += green(event.looted_by.name)
    
    # Formata jogador de quem pegou (vermelho)
    looted_from_str = ""
    if event.looted_from.alliance:
        looted_from_str += gray(f"{{{event.looted_from.alliance}}}") + " "
    if event.looted_from.guild:
        looted_from_str += gray(f"[{event.looted_from.guild}]") + " "
    looted_from_str += red(event.looted_from.name)
    
    # Imprime
    print(f"{time_str} UTC: {looted_by_str} looted {bold(str(event.quantity))}x {cyan(event.item_name)} from {looted_from_str}")
    
    # Envia para Discord
    if discord_service.enabled:
        discord_service.send_loot_event(event)


def on_online():
    """Callback quando Albion é detectado."""
    print(f"\n\t{green('ALBION DETECTADO')}. Eventos de loot serão registrados.\n")
    
    if discord_service.enabled:
        discord_service.send_status("🎮 Albion Online detectado! Logging iniciado.", is_online=True)


def on_offline():
    """Callback quando Albion não é mais detectado."""
    print(f"\n\t{red('ALBION NÃO DETECTADO')}.")
    print(f"\n\tSe o Albion está rodando, verifique se está executando como Administrador.\n")
    
    if discord_service.enabled:
        discord_service.send_status("🔴 Albion Online não detectado.", is_online=False)


# ============================================
# MAIN
# ============================================

def cleanup():
    """Limpa recursos antes de sair."""
    global log_file
    
    if log_file:
        log_file.close()
        log_file = None
    
    print("\n" + yellow("[INFO] Encerrando..."))


def signal_handler(sig, frame):
    """Handler para Ctrl+C."""
    cleanup()
    sys.exit(0)


def main():
    """Função principal."""
    global log_filename
    
    # Configura signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Banner
    print("\n" + "=" * 50)
    print(bold(cyan(f"  {TITLE}")))
    print("=" * 50)
    print()
    
    # Verifica privilégios (Windows)
    if sys.platform == 'win32':
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print(red("[ERRO] Execute como Administrador!"))
            print(yellow("[DICA] Clique com botão direito -> Executar como administrador"))
            input("\nPressione Enter para sair...")
            sys.exit(1)
    
    # Configura Discord
    if DISCORD_WEBHOOK_URL:
        discord_service.set_webhook(DISCORD_WEBHOOK_URL)
        print(green("[OK] Discord webhook configurado!"))
    
    # Carrega configurações
    print()
    if not events_config.load():
        print(red("[ERRO] Falha ao carregar configuração de eventos."))
        sys.exit(1)
    
    if not items_service.load():
        print(yellow("[AVISO] Lista de itens não carregada. Alguns itens podem aparecer como 'Unknown'."))
    
    # Cria arquivo de log
    log_filename = create_log_file()
    print(f"\n[INFO] Logs serão salvos em: {cyan(log_filename)}")
    
    # Cria sniffer
    print(f"\n[INFO] Iniciando captura de pacotes...")
    print(gray("[INFO] Filtro: UDP portas 5056, 5055, 4535"))
    
    sniffer = AlbionSniffer()
    
    # Registra callbacks
    data_handler.on_loot(on_loot)
    
    sniffer.on_event(data_handler.handle_event)
    sniffer.on_request(data_handler.handle_request)
    sniffer.on_response(data_handler.handle_response)
    sniffer.on_online(on_online)
    sniffer.on_offline(on_offline)
    
    # Inicia captura
    sniffer.start()
    
    print(f"\n{green('[OK]')} Sniffer iniciado!")
    print(f"\n{yellow('Aguardando conexão com Albion Online...')}")
    print(f"{gray('(Abra o jogo ou entre em uma zona para detectar)')}")
    print()
    print(f"Pressione {bold('Ctrl+C')} para encerrar.")
    print(f"Pressione {bold('E')} + Enter para exportar JSON.")
    print()
    
    # Envia status inicial para Discord
    if discord_service.enabled:
        discord_service.send_status("🚀 AO Loot Logger iniciado! Aguardando conexão...", is_online=True)
    
    # Loop principal
    try:
        while True:
            try:
                cmd = input().strip().lower()
                
                if cmd == 'e':
                    export_json()
                elif cmd == 'q':
                    break
                elif cmd == 'status':
                    print(f"\n[STATUS] Eventos capturados: {len(loot_events)}")
                    print(f"[STATUS] Arquivo: {log_filename}")
                    print()
            except EOFError:
                break
    
    except KeyboardInterrupt:
        pass
    
    finally:
        sniffer.stop()
        cleanup()
        
        print(f"\n{green('[OK]')} Total de eventos capturados: {len(loot_events)}")
        if log_filename:
            print(f"{green('[OK]')} Log salvo em: {log_filename}")


if __name__ == "__main__":
    main()
