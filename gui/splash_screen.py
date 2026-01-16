"""
Splash Screen - Tela de introdução
Feito por Kazz
"""

import customtkinter as ctk
import math
from typing import Callable, Optional
from PIL import Image
import os


class SplashScreen(ctk.CTkToplevel):
    """Tela de introdução."""
    
    def __init__(
        self,
        master,
        theme: dict,
        on_enter: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.theme = theme
        self.on_enter = on_enter
        self._animation_running = True
        self._glow_phase = 0
        
        # Para arrastar a janela
        self._drag_data = {"x": 0, "y": 0}
        
        # Configurações da janela
        self.title("Loot Logger")
        self.geometry("520x480")
        self.resizable(False, False)
        
        # Centraliza na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 520) // 2
        y = (self.winfo_screenheight() - 480) // 2
        self.geometry(f"520x480+{x}+{y}")
        
        # Remove decorações e configura
        self.overrideredirect(True)
        self.configure(fg_color=theme["splash_bg"])
        
        # Faz a janela ficar no topo
        self.attributes("-topmost", True)
        
        # Carrega logo
        self._load_logo()
        
        # Cria widgets
        self._create_widgets()
        
        # Bind para arrastar janela
        self.bind("<Button-1>", self._on_drag_start)
        self.bind("<B1-Motion>", self._on_drag_motion)
        
        # Inicia animação da barra
        self._animate_glow()
        
        # Bind para fechar com Escape ou Enter
        self.bind("<Escape>", lambda e: self._on_enter_click())
        self.bind("<Return>", lambda e: self._on_enter_click())
    
    def _load_logo(self):
        """Carrega a imagem do logo."""
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logo_path = os.path.join(base_path, "assets", "logo.png")
            
            if os.path.exists(logo_path):
                self.logo_image = ctk.CTkImage(
                    light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path),
                    size=(220, 220)
                )
            else:
                self.logo_image = None
        except Exception as e:
            print(f"[AVISO] Não foi possível carregar logo: {e}")
            self.logo_image = None
    
    def _on_drag_start(self, event):
        """Início do arraste."""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
    
    def _on_drag_motion(self, event):
        """Durante o arraste."""
        x = self.winfo_x() + (event.x - self._drag_data["x"])
        y = self.winfo_y() + (event.y - self._drag_data["y"])
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Cria os widgets da splash screen."""
        
        # Container principal com borda
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg_secondary"],
            corner_radius=20,
            border_width=2,
            border_color=self.theme["border"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Espaçador superior
        ctk.CTkFrame(self.main_frame, fg_color="transparent", height=35).pack()
        
        # Logo
        if self.logo_image:
            self.logo_label = ctk.CTkLabel(
                self.main_frame,
                image=self.logo_image,
                text=""
            )
        else:
            self.logo_label = ctk.CTkLabel(
                self.main_frame,
                text="🎒",
                font=("Segoe UI Emoji", 80),
                text_color=self.theme["text_primary"]
            )
        self.logo_label.pack()
        
        # Título "AO LOOT LOGGER"
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="AO LOOT LOGGER",
            font=("Segoe UI", 28, "bold"),
            text_color=self.theme["text_primary"]
        )
        self.title_label.pack(pady=(15, 8))
        
        # Linha decorativa ANIMADA
        self.line_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.theme["accent"],
            height=4,
            width=180,
            corner_radius=2
        )
        self.line_frame.pack(pady=(0, 35))
        
        # Botão ENTRAR
        self.enter_btn = ctk.CTkButton(
            self.main_frame,
            text="▶  ENTRAR",
            font=("Segoe UI", 16, "bold"),
            width=180,
            height=52,
            corner_radius=12,
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_hover"],
            text_color="#FFFFFF",
            command=self._on_enter_click
        )
        self.enter_btn.pack(pady=(0, 25))
        
        # Espaçador
        ctk.CTkFrame(self.main_frame, fg_color="transparent").pack(fill="both", expand=True)
        
        # Créditos
        self.credits_label = ctk.CTkLabel(
            self.main_frame,
            text="Feito por Kazz",
            font=("Segoe UI", 12, "italic"),
            text_color=self.theme["text_muted"]
        )
        self.credits_label.pack(pady=(0, 25))
    
    def _animate_glow(self):
        """Animação da linha decorativa (inspira/exala)."""
        if not self._animation_running:
            return
        
        self._glow_phase += 0.05
        
        # Varia a largura (efeito de respiração)
        width = 180 + 40 * math.sin(self._glow_phase * 2)
        self.line_frame.configure(width=int(width))
        
        # Continua animação
        self.after(30, self._animate_glow)
    
    def _on_enter_click(self):
        """Callback quando clica em ENTRAR."""
        self._animation_running = False
        
        # Fade out effect
        self._fade_out(1.0)
    
    def _fade_out(self, alpha: float):
        """Efeito de fade out."""
        if alpha <= 0:
            self.destroy()
            if self.on_enter:
                self.on_enter()
            return
        
        try:
            self.attributes("-alpha", alpha)
        except:
            pass
        
        self.after(20, lambda: self._fade_out(alpha - 0.1))


class SplashManager:
    """Gerenciador da splash screen."""
    
    def __init__(self, root, theme: dict, on_complete: Callable):
        self.root = root
        self.theme = theme
        self.on_complete = on_complete
        self.splash = None
    
    def show(self):
        """Mostra a splash screen."""
        # Esconde janela principal
        self.root.withdraw()
        
        # Cria splash
        self.splash = SplashScreen(
            self.root,
            self.theme,
            on_enter=self._on_splash_complete
        )
        
        # Garante que splash apareça
        self.splash.focus_force()
    
    def _on_splash_complete(self):
        """Callback quando splash fecha."""
        # Mostra janela principal
        self.root.deiconify()
        self.root.focus_force()
        
        # Callback
        if self.on_complete:
            self.on_complete()
