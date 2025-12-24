"""
Status Bar - Barra de status com indicador e estatísticas
Feito por Kazz
"""

import customtkinter as ctk
import math


class StatusBar(ctk.CTkFrame):
    """Barra de status com indicador de conexão e estatísticas."""
    
    def __init__(self, master, theme: dict, **kwargs):
        super().__init__(
            master,
            fg_color=theme["bg_secondary"],
            corner_radius=0,
            height=50,
            **kwargs
        )
        self.theme = theme
        self._pulse_phase = 0
        self._pulse_running = False
        self._current_status = "waiting"
        
        self.pack_propagate(False)
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # ===== LADO ESQUERDO - Status =====
        left_frame = ctk.CTkFrame(container, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # LED indicator
        self.led_frame = ctk.CTkFrame(
            left_frame,
            fg_color=self.theme["text_muted"],
            width=12,
            height=12,
            corner_radius=6
        )
        self.led_frame.pack(side="left", padx=(0, 10))
        self.led_frame.pack_propagate(False)
        
        # Status text
        self.status_label = ctk.CTkLabel(
            left_frame,
            text="Aguardando...",
            font=("Segoe UI", 12),
            text_color=self.theme["text_secondary"]
        )
        self.status_label.pack(side="left")
        
        # ===== CENTRO - Créditos =====
        center_frame = ctk.CTkFrame(container, fg_color="transparent")
        center_frame.pack(side="left", fill="both", expand=True)
        
        center_inner = ctk.CTkFrame(center_frame, fg_color="transparent")
        center_inner.pack(expand=True)
        
        self.credits_label = ctk.CTkLabel(
            center_inner,
            text="Feito por Kazz",
            font=("Segoe UI", 11, "italic"),
            text_color=self.theme["text_muted"]
        )
        self.credits_label.pack()
        
        # ===== LADO DIREITO - Contador de eventos =====
        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        events_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        events_frame.pack(side="left")
        
        events_icon = ctk.CTkLabel(
            events_frame,
            text="📊",
            font=("Segoe UI Emoji", 14)
        )
        events_icon.pack(side="left", padx=(0, 5))
        
        self.count_label = ctk.CTkLabel(
            events_frame,
            text="0 eventos",
            font=("Segoe UI", 12),
            text_color=self.theme["text_secondary"]
        )
        self.count_label.pack(side="left")
    
    def _animate_pulse(self):
        """Animação de pulso no LED quando online."""
        if not self._pulse_running:
            return
        
        self._pulse_phase += 0.08
        
        base_size = 12
        size = int(base_size * (0.9 + 0.2 * math.sin(self._pulse_phase)))
        
        self.led_frame.configure(
            width=size,
            height=size,
            corner_radius=size // 2
        )
        
        self.after(50, self._animate_pulse)
    
    def set_status(self, status: str):
        """Define o status."""
        if status == "online":
            self.set_online()
        elif status == "offline":
            self.set_offline()
        elif status == "connecting":
            self.set_waiting()
        else:
            self.set_waiting()
    
    def set_online(self):
        """Define status como online."""
        self._current_status = "online"
        self.led_frame.configure(fg_color=self.theme["success"])
        self.status_label.configure(
            text="Albion Detectado",
            text_color=self.theme["success"]
        )
        
        if not self._pulse_running:
            self._pulse_running = True
            self._animate_pulse()
    
    def set_offline(self):
        """Define status como offline."""
        self._current_status = "offline"
        self._pulse_running = False
        
        self.led_frame.configure(
            fg_color=self.theme["error"],
            width=12,
            height=12,
            corner_radius=6
        )
        self.status_label.configure(
            text="Albion Não Detectado",
            text_color=self.theme["error"]
        )
    
    def set_waiting(self):
        """Define status como aguardando."""
        self._current_status = "waiting"
        self._pulse_running = False
        
        self.led_frame.configure(
            fg_color=self.theme["warning"],
            width=12,
            height=12,
            corner_radius=6
        )
        self.status_label.configure(
            text="Aguardando conexão...",
            text_color=self.theme["warning"]
        )
    
    def set_count(self, count: int):
        """Atualiza contador de eventos."""
        text = f"{count} evento" if count == 1 else f"{count} eventos"
        self.count_label.configure(text=text)
        
        if count > 0:
            self.count_label.configure(text_color=self.theme["accent"])
            self.after(500, lambda: self.count_label.configure(
                text_color=self.theme["text_secondary"]
            ))
