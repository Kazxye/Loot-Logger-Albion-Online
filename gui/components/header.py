"""
Header - Cabeçalho com título, logo e controles
Feito por Kazz
"""

import customtkinter as ctk
from typing import Callable, Optional
import math

from gui.icons import get_emoji


class Header(ctk.CTkFrame):
    """Cabeçalho da aplicação com linha animada."""
    
    def __init__(
        self, 
        master, 
        theme: dict,
        on_start: Optional[Callable] = None,
        on_stop: Optional[Callable] = None,
        on_export: Optional[Callable] = None,
        on_clear: Optional[Callable] = None,
        on_theme_toggle: Optional[Callable] = None,
        on_settings: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=theme["bg_secondary"],
            corner_radius=0,
            **kwargs
        )
        self.theme = theme
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_export = on_export
        self.on_clear = on_clear
        self.on_theme_toggle = on_theme_toggle
        self.on_settings = on_settings
        self.is_running = False
        self.is_dark = True
        
        # Animação
        self._animation_running = True
        self._glow_phase = 0
        
        self._create_widgets()
        
        # Inicia animação
        self._animate_line()
    
    def _create_widgets(self):
        """Cria todos os widgets."""
        
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Container interno com padding
        container = ctk.CTkFrame(main_container, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=25, pady=(18, 12))
        
        # ===== LADO ESQUERDO - Título =====
        left_frame = ctk.CTkFrame(container, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # Título (sem emoji)
        title_label = ctk.CTkLabel(
            left_frame,
            text="Loot Logger",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme["accent"]  # Título em LARANJA
        )
        title_label.pack(side="left")
        
        # ===== LADO DIREITO - Botões =====
        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        # Botão Limpar
        self.clear_btn = ctk.CTkButton(
            right_frame,
            text="🗑️ Limpar",
            width=100,
            height=45,
            corner_radius=10,
            fg_color=self.theme["bg_tertiary"],
            hover_color=self.theme["bg_hover"],
            border_width=1,
            border_color=self.theme["border"],
            text_color=self.theme["text_primary"],
            font=("Segoe UI", 13),
            command=self._on_clear_click
        )
        self.clear_btn.pack(side="left", padx=(0, 8))
        
        # Botão Export
        self.export_btn = ctk.CTkButton(
            right_frame,
            text=f"{get_emoji('download')} Exportar",
            width=120,
            height=45,
            corner_radius=10,
            fg_color=self.theme["bg_tertiary"],
            hover_color=self.theme["bg_hover"],
            border_width=1,
            border_color=self.theme["border"],
            text_color=self.theme["text_primary"],
            font=("Segoe UI", 13),
            command=self._on_export_click
        )
        self.export_btn.pack(side="left", padx=(0, 8))
        
        # Botão Configurações
        self.settings_btn = ctk.CTkButton(
            right_frame,
            text="⚙️",
            width=45,
            height=45,
            corner_radius=10,
            fg_color=self.theme["bg_tertiary"],
            hover_color=self.theme["bg_hover"],
            border_width=1,
            border_color=self.theme["border"],
            font=("Segoe UI Emoji", 18),
            command=self._on_settings_click
        )
        self.settings_btn.pack(side="left", padx=(0, 8))
        
        # Botão Start/Stop
        self.toggle_btn = ctk.CTkButton(
            right_frame,
            text=f"{get_emoji('play')} Iniciar",
            width=130,
            height=45,
            corner_radius=10,
            fg_color=self.theme["success"],
            hover_color=self.theme["success_hover"],
            text_color="#FFFFFF",
            font=("Segoe UI", 14, "bold"),
            command=self._on_toggle_click
        )
        self.toggle_btn.pack(side="left")
        
        # ===== LINHA ANIMADA (na parte inferior) =====
        self.line_container = ctk.CTkFrame(main_container, fg_color="transparent", height=6)
        self.line_container.pack(fill="x", side="bottom")
        self.line_container.pack_propagate(False)
        
        # Linha central animada
        self.animated_line = ctk.CTkFrame(
            self.line_container,
            fg_color=self.theme["accent"],
            height=3,
            width=200,
            corner_radius=2
        )
        self.animated_line.place(relx=0.5, rely=0.5, anchor="center")
    
    def _animate_line(self):
        """Animação da linha laranja (inspira/exala)."""
        if not self._animation_running:
            return
        
        self._glow_phase += 0.03
        
        # Varia a largura entre 150 e 350
        base_width = 250
        variation = 100
        width = base_width + variation * math.sin(self._glow_phase * 2)
        
        self.animated_line.configure(width=int(width))
        
        # Continua animação
        self.after(30, self._animate_line)
    
    def _on_toggle_click(self):
        """Callback do botão iniciar/parar."""
        if self.is_running:
            self.set_stopped()
            if self.on_stop:
                self.on_stop()
        else:
            self.set_running()
            if self.on_start:
                self.on_start()
    
    def _on_export_click(self):
        """Callback do botão exportar."""
        if self.on_export:
            self.on_export()
    
    def _on_clear_click(self):
        """Callback do botão limpar."""
        if self.on_clear:
            self.on_clear()
    
    def _on_settings_click(self):
        """Callback do botão de configurações."""
        if self.on_settings:
            self.on_settings()
    
    def set_running(self):
        """Define estado como rodando."""
        self.is_running = True
        self.toggle_btn.configure(
            text=f"{get_emoji('stop')} Parar",
            fg_color=self.theme["error"],
            hover_color=self.theme["error_hover"]
        )
    
    def set_stopped(self):
        """Define estado como parado."""
        self.is_running = False
        self.toggle_btn.configure(
            text=f"{get_emoji('play')} Iniciar",
            fg_color=self.theme["success"],
            hover_color=self.theme["success_hover"]
        )
    
    def destroy(self):
        """Para animação ao destruir."""
        self._animation_running = False
        super().destroy()
