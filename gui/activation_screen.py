"""
Activation Screen - Tela de ativacao de licenca
"""

import customtkinter as ctk
import threading
from typing import Callable, Optional


class ActivationScreen:
    """Tela de ativacao de licenca."""
    
    def __init__(
        self,
        parent,
        theme: dict,
        on_success: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None
    ):
        self.parent = parent
        self.theme = theme
        self.on_success = on_success
        self.on_cancel = on_cancel
        self.frame: Optional[ctk.CTkFrame] = None
    
    def show(self):
        """Mostra a tela de ativacao."""
        print("[INFO] Abrindo tela de ativacao...")
        
        # Limpa qualquer conteudo anterior
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.frame = ctk.CTkFrame(self.parent, fg_color=self.theme["bg_primary"])
        self.frame.pack(fill="both", expand=True)
        
        # Container central
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo
        logo_label = ctk.CTkLabel(
            container,
            text="Loot Logger",
            font=("Segoe UI", 36, "bold"),
            text_color=self.theme["accent"]
        )
        logo_label.pack(pady=(0, 5))
        
        # Subtitulo
        subtitle = ctk.CTkLabel(
            container,
            text="by Kazz",
            font=("Segoe UI", 14),
            text_color=self.theme["text_muted"]
        )
        subtitle.pack(pady=(0, 30))
        
        # Card de ativacao
        card = ctk.CTkFrame(
            container,
            fg_color=self.theme["bg_secondary"],
            corner_radius=15,
            width=400
        )
        card.pack(padx=20, pady=10)
        
        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Titulo do card
        title = ctk.CTkLabel(
            card_inner,
            text="Ativacao de Licenca",
            font=("Segoe UI", 18, "bold"),
            text_color=self.theme["text_primary"]
        )
        title.pack(anchor="w", pady=(0, 5))
        
        # Descricao
        desc = ctk.CTkLabel(
            card_inner,
            text="Digite sua chave de licenca para continuar",
            font=("Segoe UI", 12),
            text_color=self.theme["text_secondary"]
        )
        desc.pack(anchor="w", pady=(0, 20))
        
        # Campo de licenca
        self.license_entry = ctk.CTkEntry(
            card_inner,
            placeholder_text="XXXX-XXXX-XXXX-XXXX",
            width=340,
            height=45,
            font=("Consolas", 14),
            fg_color=self.theme["bg_tertiary"],
            border_color=self.theme["border"],
            text_color=self.theme["text_primary"],
            justify="center"
        )
        self.license_entry.pack(pady=(0, 10))
        self.license_entry.bind("<Return>", lambda e: self._activate())
        
        # Mensagem de status
        self.status_label = ctk.CTkLabel(
            card_inner,
            text="",
            font=("Segoe UI", 11),
            text_color=self.theme["text_secondary"],
            wraplength=320
        )
        self.status_label.pack(pady=(0, 15))
        
        # Botao de ativar
        self.activate_btn = ctk.CTkButton(
            card_inner,
            text="Ativar Licenca",
            width=340,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_hover"],
            text_color="#FFFFFF",
            command=self._activate
        )
        self.activate_btn.pack(pady=(0, 10))
        
        # HWID info
        from services import license_service
        hwid = license_service.get_hwid()
        
        hwid_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        hwid_frame.pack(fill="x", pady=(10, 0))
        
        hwid_label = ctk.CTkLabel(
            hwid_frame,
            text=f"HWID: {hwid[:8]}...{hwid[-8:]}",
            font=("Consolas", 10),
            text_color=self.theme["text_muted"]
        )
        hwid_label.pack()
        
        # Verifica se tem licenca salva
        saved_key = license_service.get_saved_license()
        if saved_key:
            self.license_entry.insert(0, saved_key)
            self._set_status("Verificando licenca salva...", "warning")
            self.parent.after(500, self._auto_validate)
        
        # Verifica versao
        self._check_version()
        
        # Mostra janela
        print("[INFO] Configurando janela...")
        
        # Centraliza
        w, h = 500, 450
        x = (self.parent.winfo_screenwidth() - w) // 2
        y = (self.parent.winfo_screenheight() - h) // 2
        self.parent.geometry(f"{w}x{h}+{x}+{y}")
        
        # Força a janela a aparecer
        self.parent.deiconify()
        self.parent.lift()
        self.parent.focus_force()
        self.parent.update()
        
        print("[INFO] Tela de ativacao aberta!")
        
        # Foco no campo
        self.license_entry.focus_set()
    
    def _check_version(self):
        """Verifica se ha atualizacao."""
        def check():
            from services import license_service
            has_update, current, remote = license_service.check_version()
            if has_update:
                self.parent.after(0, lambda: self._show_update_notice(current, remote))
        
        threading.Thread(target=check, daemon=True).start()
    
    def _show_update_notice(self, current: str, remote: str):
        """Mostra aviso de atualizacao."""
        self._set_status(
            f"Nova versao disponivel: v{remote} (atual: v{current})",
            "warning"
        )
    
    def _auto_validate(self):
        """Valida licenca automaticamente."""
        self._activate()
    
    def _set_status(self, message: str, status_type: str = "info"):
        """Define mensagem de status."""
        colors = {
            "info": self.theme["text_secondary"],
            "success": self.theme["success"],
            "error": self.theme["error"],
            "warning": self.theme["warning"]
        }
        self.status_label.configure(
            text=message,
            text_color=colors.get(status_type, self.theme["text_secondary"])
        )
    
    def _activate(self):
        """Tenta ativar a licenca."""
        key = self.license_entry.get().strip()
        
        if not key:
            self._set_status("Digite uma chave de licenca.", "error")
            return
        
        # Desabilita botao
        self.activate_btn.configure(state="disabled", text="Verificando...")
        self._set_status("Verificando licenca...", "info")
        
        # Valida em thread separada
        def validate():
            from services import license_service
            success, message = license_service.validate_license(key)
            self.parent.after(0, lambda: self._on_validation_result(success, message))
        
        threading.Thread(target=validate, daemon=True).start()
    
    def _on_validation_result(self, success: bool, message: str):
        """Callback do resultado da validacao."""
        self.activate_btn.configure(state="normal", text="Ativar Licenca")
        
        if success:
            self._set_status("Licenca ativada com sucesso!", "success")
            self.activate_btn.configure(
                text="Entrando...",
                state="disabled",
                fg_color=self.theme["success"]
            )
            
            # Mostra info da licenca
            from services import license_service
            info = license_service.license_info
            if info:
                if info.days_remaining >= 0:
                    self._set_status(
                        f"Bem-vindo, {info.user}! ({info.days_remaining} dias restantes)",
                        "success"
                    )
                else:
                    self._set_status(f"Bem-vindo, {info.user}! (Licenca Vitalicia)", "success")
            
            # Aguarda e continua
            self.parent.after(1500, self._continue)
        else:
            self._set_status(message, "error")
    
    def _continue(self):
        """Continua para o app principal."""
        if self.frame:
            self.frame.destroy()
        if self.on_success:
            self.on_success()
    
    def hide(self):
        """Esconde a tela."""
        if self.frame:
            self.frame.destroy()
            self.frame = None


class ActivationManager:
    """Gerenciador da tela de ativacao."""
    
    def __init__(
        self,
        parent,
        theme: dict,
        on_success: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None
    ):
        self.screen = ActivationScreen(parent, theme, on_success, on_cancel)
    
    def show(self):
        self.screen.show()
    
    def hide(self):
        self.screen.hide()
