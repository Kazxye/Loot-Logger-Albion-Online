"""
App - Aplicacao principal da GUI
Loot Logger para Albion Online
Feito por Kazz
"""

import customtkinter as ctk
import threading
import json
import sys
import os
from datetime import datetime
from typing import Optional, List, Set, Dict
from tkinter import messagebox, filedialog

from gui.themes import get_theme, DARK_THEME, LIGHT_THEME
from gui.components import Header, StatusBar, LootTable, FilterPanel, SettingsModal
from gui.components.filter_panel import get_item_category
from gui.splash_screen import SplashManager


# Padroes de nomes de MOBs
MOB_PATTERNS = [
    "@", "MOB_", "KEEPER_", "DEMON_", "UNDEAD_", "HERETIC_",
    "CREATURE_", "BOSS_", "MINION_", "GUARD_", "ELEMENTAL_",
    "SPIRIT_", "DRONE_", "TURRET_", "AVALON_", "FACTION_",
]


def is_mob(name: str) -> bool:
    """Verifica se o nome e de um MOB."""
    if not name:
        return True
    if name.startswith("@"):
        return True
    name_upper = name.upper()
    for pattern in MOB_PATTERNS:
        if pattern in name_upper:
            return True
    return False


class LootLoggerApp(ctk.CTk):
    """Aplicacao principal do Loot Logger."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Loot Logger - by Kazz")
        self.geometry("1300x800")
        self.minsize(1000, 600)
        
        self._set_icon()
        self._set_taskbar_icon()
        
        # Estado
        self.is_dark_theme = True
        self.theme = get_theme("dark")
        self.is_running = False
        self.loot_events: List = []
        self.loot_extra_data: Dict[str, dict] = {}
        self.sniffer = None
        self.data_handler = None
        self.tier_service = None
        
        # Controle de duplicacao
        self._processed_events: Set[str] = set()
        self._callback_registered = False
        
        # Filtros de tier
        self._tier_filter: Set[int] = {4, 5, 6, 7, 8}
        self._show_rare_only: bool = False
        
        # Filtros de categorias (NOVO)
        self._selected_categories: Set[str] = {"equipment", "consumable", "resource", "rune", "other"}
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=self.theme["bg_primary"])
        
        self._widgets_created = False
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Inicia direto com splash (versao open source - sem ativacao)
        try:
            self._show_splash()
        except Exception as e:
            import traceback
            print(f"[ERRO] Falha ao iniciar: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Falha ao iniciar: {e}")
    
    def _set_icon(self):
        """Define o icone da janela."""
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_path, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass
    
    def _set_taskbar_icon(self):
        """Define o icone na barra de tarefas do Windows."""
        try:
            import ctypes
            # Define um AppUserModelID único para o aplicativo
            # Isso faz o Windows usar o ícone correto na barra de tarefas
            app_id = "kazz.lootlogger.app.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except:
            pass
    
    def _show_splash(self):
        """Mostra tela de splash."""
        self.splash_manager = SplashManager(
            self, self.theme,
            on_complete=self._on_splash_complete
        )
        self.splash_manager.show()
    
    def _on_splash_complete(self):
        """Callback quando splash fecha."""
        self._load_services()
        self._create_widgets()
        self._widgets_created = True
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1300) // 2
        y = (self.winfo_screenheight() - 800) // 2
        self.geometry(f"1300x800+{x}+{y}")
        self.deiconify()
    
    def _load_services(self):
        """Carrega servicos necessarios."""
        try:
            from services import items_service, tier_service, config_service, discord_service, events_config
            
            # Carrega configuracoes do usuario
            config_service.load()
            
            # Carrega configuracao de eventos
            events_config.load()
            
            # Define idioma
            items_service.locale = config_service.language
            
            # Configura Discord
            if config_service.discord_enabled and config_service.is_webhook_valid():
                discord_service.set_webhook(config_service.discord_webhook)
            
            # Carrega itens em background
            threading.Thread(target=self._load_items_async, daemon=True).start()
            self.tier_service = tier_service
            
        except Exception as e:
            print(f"[ERRO] Falha ao carregar servicos: {e}")
    
    def _load_items_async(self):
        """Carrega itens em background."""
        try:
            from services import items_service
            items_service.load()
        except Exception as e:
            print(f"[ERRO] Falha ao carregar itens: {e}")
    
    def _create_widgets(self):
        """Cria todos os widgets da interface."""
        
        # Header
        self.header = Header(
            self, theme=self.theme,
            on_start=self._on_start,
            on_stop=self._on_stop,
            on_export=self._on_export,
            on_clear=self._on_clear,
            on_theme_toggle=self._toggle_theme,
            on_settings=self._open_settings
        )
        self.header.pack(fill="x")
        
        sep1 = ctk.CTkFrame(self, fg_color=self.theme["border"], height=1)
        sep1.pack(fill="x")
        
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Painel de filtros
        self.filter_panel = FilterPanel(
            main_container, theme=self.theme,
            on_filter_change=self._on_filter_change,
            on_tier_filter_change=self._on_tier_filter_change,
            on_item_filter_change=self._on_item_filter_change
        )
        self.filter_panel.pack(side="left", fill="y")
        
        sep_v = ctk.CTkFrame(main_container, fg_color=self.theme["border"], width=1)
        sep_v.pack(side="left", fill="y")
        
        # Tabela de loot
        self.loot_table = LootTable(main_container, theme=self.theme)
        self.loot_table.pack(side="left", fill="both", expand=True)
        
        sep2 = ctk.CTkFrame(self, fg_color=self.theme["border"], height=1)
        sep2.pack(fill="x")
        
        # Status bar
        self.status_bar = StatusBar(self, theme=self.theme)
        self.status_bar.pack(fill="x")
    
    def _open_settings(self):
        """Abre modal de configuracoes."""
        SettingsModal(self, self.theme, on_save=self._on_settings_save)
    
    def _on_settings_save(self):
        """Callback quando configuracoes sao salvas."""
        from services import config_service, items_service, discord_service
        
        # Atualiza idioma
        items_service.locale = config_service.language
        
        # Atualiza Discord
        if config_service.discord_enabled and config_service.is_webhook_valid():
            discord_service.set_webhook(config_service.discord_webhook)
        else:
            discord_service.disable()
    
    def _toggle_theme(self):
        """Alterna entre tema dark e light."""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.theme = DARK_THEME
            ctk.set_appearance_mode("dark")
        else:
            self.theme = LIGHT_THEME
            ctk.set_appearance_mode("light")
        
        self.header.set_theme_icon(self.is_dark_theme)
        self.configure(fg_color=self.theme["bg_primary"])
        self._recreate_widgets()
    
    def _recreate_widgets(self):
        """Recria widgets com novo tema."""
        events = self.loot_events.copy()
        extra_data = self.loot_extra_data.copy()
        is_running = self.is_running
        
        for widget in self.winfo_children():
            widget.destroy()
        
        self._create_widgets()
        
        self.loot_events = events
        self.loot_extra_data = extra_data
        
        for event in events[-50:]:
            event_key = self._generate_event_key(event)
            extra = extra_data.get(event_key, {})
            
            self.loot_table.add_loot(
                event, "",
                is_rare=extra.get("is_rare", False),
                tier_display=extra.get("tier_display", ""),
                tier_color=extra.get("tier_color", "")
            )
            
            # Adiciona apenas o LOOTER ao filtro
            if not is_mob(event.looted_by.name):
                self.filter_panel.add_player(event.looted_by.name)
        
        self.status_bar.set_count(len(events))
        
        if is_running:
            self.header.set_running()
            self.status_bar.set_status("online")
    
    def _on_start(self):
        """Inicia captura de loot."""
        if self.is_running:
            return
        
        try:
            from core import Sniffer
            from handlers import data_handler
            from services import discord_service, config_service
            
            self.sniffer = Sniffer()
            self.data_handler = data_handler
            
            # Configura callback
            if not self._callback_registered:
                self.data_handler.on_loot(self._on_loot_event)
                self._callback_registered = True
            
            # Configura Discord
            if config_service.discord_enabled and config_service.is_webhook_valid():
                discord_service.set_webhook(config_service.discord_webhook)
            
            # Conecta eventos
            self.sniffer.on_event(self.data_handler.handle_event)
            self.sniffer.on_request(self.data_handler.handle_request)
            self.sniffer.on_response(self.data_handler.handle_response)
            
            # Callbacks de status
            def on_albion_online():
                self.after(0, lambda: self.status_bar.set_status("online"))
                discord_service.send_status("Albion Online Detectado! Loot Logger monitorando.", True)
            
            def on_albion_offline():
                self.after(0, lambda: self.status_bar.set_status("offline"))
            
            self.sniffer.on_online(on_albion_online)
            self.sniffer.on_offline(on_albion_offline)
            
            self.sniffer.start()
            self.is_running = True
            self.header.set_running()
            self.status_bar.set_status("connecting")
            
            # Envia mensagem inicial
            discord_service.send_status("Loot Logger Iniciado! Aguardando Albion Online...", True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar: {e}")
    
    def _on_stop(self):
        """Para captura de loot."""
        if not self.is_running:
            return
        
        try:
            from services import discord_service
            
            if self.sniffer:
                self.sniffer.stop()
            self.is_running = False
            self.header.set_stopped()
            self.status_bar.set_status("offline")
            
            discord_service.send_status("Loot Logger Parado.", False)
            
        except Exception as e:
            print(f"[ERRO] Falha ao parar: {e}")
    
    def _on_loot_event(self, event):
        """Callback quando um loot e detectado."""
        try:
            self.after(0, lambda e=event: self._process_loot_event(e))
        except Exception as e:
            print(f"[ERRO] _on_loot_event: {e}")
    
    def _generate_event_key(self, event) -> str:
        """Gera chave unica para evento."""
        return f"{event.timestamp.timestamp()}:{event.item_id}:{event.looted_by.name}:{event.quantity}"
    
    def _process_loot_event(self, event):
        """Processa evento de loot na thread principal."""
        try:
            event_key = self._generate_event_key(event)
            
            # Evita duplicatas
            if event_key in self._processed_events:
                return
            self._processed_events.add(event_key)
            
            # Limita historico
            if len(self._processed_events) > 1000:
                old_keys = list(self._processed_events)[:500]
                for key in old_keys:
                    self._processed_events.discard(key)
            
            self.loot_events.append(event)
            
            # Info de tier
            tier_display = ""
            tier_color = ""
            is_rare = False
            tier = 0
            enchant = 0
            
            if self.tier_service:
                tier_info = self.tier_service.parse_tier(event.item_id)
                if tier_info:
                    tier_display = tier_info.display_name
                    tier_color = self.tier_service.get_tier_color(event.item_id)
                    is_rare = tier_info.is_rare
                    tier = tier_info.tier
                    enchant = tier_info.enchant
            
            # Salva dados extras
            self.loot_extra_data[event_key] = {
                "is_rare": is_rare,
                "tier_display": tier_display,
                "tier_color": tier_color,
                "tier": tier,
                "enchant": enchant
            }
            
            # Aplica filtros
            if self._should_show_event(event, tier_display):
                self.loot_table.add_loot(
                    event, "",
                    is_rare=is_rare,
                    tier_display=tier_display,
                    tier_color=tier_color,
                    tier=tier,
                    enchant=enchant
                )
            
            # Adiciona apenas o LOOTER (quem pegou) ao filtro
            # NÃO adiciona looted_from para evitar confusão
            if not is_mob(event.looted_by.name):
                self.filter_panel.add_player(event.looted_by.name)
            
            self.status_bar.set_count(len(self.loot_events))
            
            # Envia para Discord
            self._send_to_discord(event, tier_display, is_rare)
            
        except Exception as e:
            print(f"[ERRO] _process_loot_event: {e}")
    
    def _should_show_event(self, event, tier_display: str) -> bool:
        """Verifica se evento deve ser exibido."""
        # Filtro de tier
        if tier_display and self._tier_filter:
            try:
                tier_str = tier_display.replace("T", "").split(".")[0]
                tier = int(tier_str)
                if tier not in self._tier_filter:
                    return False
            except:
                pass
        
        # Filtro de raros
        if self._show_rare_only:
            event_key = self._generate_event_key(event)
            extra = self.loot_extra_data.get(event_key, {})
            if not extra.get("is_rare", False):
                return False
        
        # Filtro de categorias
        item_category = get_item_category(event.item_id)
        if item_category not in self._selected_categories:
            return False
        
        # Filtro de jogadores (apenas looters)
        try:
            selected = self.filter_panel.get_selected_players()
            if selected is not None and len(selected) > 0:
                # Filtra apenas por quem PEGOU o loot
                if event.looted_by.name not in selected:
                    return False
        except:
            pass
        
        return True
    
    def _send_to_discord(self, event, tier_display: str, is_rare: bool):
        """Envia loot para Discord se configurado."""
        try:
            from services import discord_service, config_service
            
            if not config_service.discord_enabled:
                return
            
            discord_service.send_loot_event(event)
            
        except Exception as e:
            print(f"[ERRO] Falha ao enviar para Discord: {e}")
    
    def _on_filter_change(self, selected_players):
        """Callback quando filtro de jogadores muda."""
        self._rebuild_loot_table()
    
    def _on_tier_filter_change(self, selected_tiers: Set[int], show_rare_only: bool):
        """Callback quando filtro de tier muda."""
        self._tier_filter = selected_tiers
        self._show_rare_only = show_rare_only
        self._rebuild_loot_table()
    
    def _on_item_filter_change(self, filters: dict):
        """Callback quando filtro de categorias muda."""
        self._selected_categories = filters.get("categories", {"equipment", "consumable", "resource", "rune", "other"})
        self._rebuild_loot_table()
    
    def _rebuild_loot_table(self):
        """Reconstroi tabela aplicando filtros."""
        self.loot_table.clear()
        
        for event in self.loot_events[-100:]:
            event_key = self._generate_event_key(event)
            extra = self.loot_extra_data.get(event_key, {})
            
            tier_display = extra.get("tier_display", "")
            is_rare = extra.get("is_rare", False)
            tier_color = extra.get("tier_color", "")
            tier = extra.get("tier", 0)
            enchant = extra.get("enchant", 0)
            
            if self._should_show_event(event, tier_display):
                self.loot_table.add_loot(
                    event, "",
                    is_rare=is_rare,
                    tier_display=tier_display,
                    tier_color=tier_color,
                    tier=tier,
                    enchant=enchant
                )
    
    def _on_export(self):
        """Exporta eventos de loot."""
        if not self.loot_events:
            messagebox.showinfo("Exportar", "Nenhum loot para exportar!")
            return
        
        file_types = [
            ("JSON files", "*.json"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=file_types,
            title="Exportar Loots"
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.csv'):
                self._export_csv(file_path)
            else:
                self._export_json(file_path)
            
            messagebox.showinfo("Sucesso", f"Exportado {len(self.loot_events)} eventos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")
    
    def _export_json(self, file_path: str):
        """Exporta para JSON."""
        data = [event.to_dict() for event in self.loot_events]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _export_csv(self, file_path: str):
        """Exporta para CSV."""
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            
            # Header
            writer.writerow([
                'timestamp', 'item_id', 'item_name', 'quantity',
                'looted_by', 'looted_by_guild', 'looted_from', 'looted_from_guild'
            ])
            
            # Data
            for event in self.loot_events:
                writer.writerow([
                    event.timestamp.isoformat(),
                    event.item_id,
                    event.item_name,
                    event.quantity,
                    event.looted_by.name,
                    event.looted_by.guild,
                    event.looted_from.name,
                    event.looted_from.guild
                ])
    
    def _on_clear(self):
        """Limpa todos os eventos."""
        if not self.loot_events:
            return
        
        if messagebox.askyesno("Limpar", "Tem certeza que deseja limpar todos os loots?"):
            self.loot_events.clear()
            self.loot_extra_data.clear()
            self._processed_events.clear()
            self.loot_table.clear()
            self.filter_panel.clear_players()
            self.status_bar.set_count(0)
    
    def _on_closing(self):
        """Callback ao fechar a janela."""
        self._on_stop()
        self.destroy()


def run_app():
    """Inicia a aplicacao."""
    app = LootLoggerApp()
    app.mainloop()
