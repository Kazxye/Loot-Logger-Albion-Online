"""
Settings Modal - Modal de configurações
"""

import customtkinter as ctk
from typing import Callable, Optional


class SettingsModal(ctk.CTkToplevel):
    """Modal de configurações."""
    
    def __init__(self, parent, theme: dict, on_save: Optional[Callable] = None):
        super().__init__(parent)
        
        self.theme = theme
        self.on_save = on_save
        
        # Configuração da janela
        self.title("Configurações")
        self.geometry("550x450")
        self.resizable(False, False)
        self.configure(fg_color=self.theme["bg_primary"])
        
        # Centraliza na tela
        self.transient(parent)
        self.grab_set()
        
        # Importa config_service
        from services import config_service
        self.config_service = config_service
        
        self._create_widgets()
        self._load_values()
        
        # Foco na janela
        self.focus_force()
        
        # Centraliza
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 550) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 450) // 2
        self.geometry(f"550x450+{x}+{y}")
    
    def _create_widgets(self):
        """Cria widgets do modal."""
        # Container principal
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            container,
            text="⚙️ Configurações",
            font=("Segoe UI", 20, "bold"),
            text_color=self.theme["text_primary"]
        )
        title.pack(pady=(0, 20))
        
        # === IDIOMA ===
        lang_frame = ctk.CTkFrame(container, fg_color=self.theme["bg_secondary"], corner_radius=10)
        lang_frame.pack(fill="x", pady=(0, 15))
        
        lang_inner = ctk.CTkFrame(lang_frame, fg_color="transparent")
        lang_inner.pack(fill="x", padx=15, pady=15)
        
        lang_label = ctk.CTkLabel(
            lang_inner,
            text="🌐 Idioma dos Itens",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme["text_primary"]
        )
        lang_label.pack(anchor="w")
        
        lang_desc = ctk.CTkLabel(
            lang_inner,
            text="Selecione o idioma para os nomes dos itens",
            font=("Segoe UI", 11),
            text_color=self.theme["text_secondary"]
        )
        lang_desc.pack(anchor="w", pady=(2, 10))
        
        self.lang_var = ctk.StringVar(value="PT-BR")
        self.lang_dropdown = ctk.CTkOptionMenu(
            lang_inner,
            variable=self.lang_var,
            values=["PT-BR", "EN-US"],
            width=200,
            height=35,
            font=("Segoe UI", 13),
            fg_color=self.theme["bg_tertiary"],
            button_color=self.theme["accent"],
            button_hover_color=self.theme["accent_hover"],
            dropdown_fg_color=self.theme["bg_secondary"],
            dropdown_hover_color=self.theme["accent"]
        )
        self.lang_dropdown.pack(anchor="w")
        
        # === DISCORD WEBHOOK ===
        discord_frame = ctk.CTkFrame(container, fg_color=self.theme["bg_secondary"], corner_radius=10)
        discord_frame.pack(fill="x", pady=(0, 15))
        
        discord_inner = ctk.CTkFrame(discord_frame, fg_color="transparent")
        discord_inner.pack(fill="x", padx=15, pady=15)
        
        # Header com checkbox
        discord_header = ctk.CTkFrame(discord_inner, fg_color="transparent")
        discord_header.pack(fill="x")
        
        discord_label = ctk.CTkLabel(
            discord_header,
            text="📨 Discord Webhook",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme["text_primary"]
        )
        discord_label.pack(side="left")
        
        self.discord_enabled_var = ctk.BooleanVar(value=False)
        self.discord_enabled_cb = ctk.CTkSwitch(
            discord_header,
            text="Ativado",
            variable=self.discord_enabled_var,
            font=("Segoe UI", 12),
            fg_color=self.theme["bg_tertiary"],
            progress_color=self.theme["success"],
            button_color=self.theme["text_secondary"],
            button_hover_color=self.theme["text_primary"],
            text_color=self.theme["text_secondary"],
            command=self._on_switch_change
        )
        self.discord_enabled_cb.pack(side="right")
        
        discord_desc = ctk.CTkLabel(
            discord_inner,
            text="Cole a URL do webhook para receber loots no Discord",
            font=("Segoe UI", 11),
            text_color=self.theme["text_secondary"]
        )
        discord_desc.pack(anchor="w", pady=(5, 10))
        
        # Frame do input com indicador
        input_frame = ctk.CTkFrame(discord_inner, fg_color="transparent")
        input_frame.pack(fill="x")
        
        self.webhook_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="https://discord.com/api/webhooks/...",
            width=400,
            height=38,
            font=("Segoe UI", 12),
            fg_color=self.theme["bg_tertiary"],
            border_color=self.theme["border"],
            text_color=self.theme["text_primary"]
        )
        self.webhook_entry.pack(side="left", fill="x", expand=True)
        
        # Indicador de status (✓ ou ✗)
        self.status_label = ctk.CTkLabel(
            input_frame,
            text="",
            font=("Segoe UI", 16),
            width=30
        )
        self.status_label.pack(side="left", padx=(10, 0))
        
        # Bind para verificar URL em tempo real
        self.webhook_entry.bind("<KeyRelease>", self._on_webhook_change)
        
        # === BOTÕES ===
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=100,
            height=40,
            font=("Segoe UI", 13),
            fg_color=self.theme["bg_tertiary"],
            hover_color=self.theme["bg_secondary"],
            text_color=self.theme["text_primary"],
            command=self.destroy
        )
        cancel_btn.pack(side="left")
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            width=130,
            height=40,
            font=("Segoe UI", 13, "bold"),
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_hover"],
            text_color="#FFFFFF",
            command=self._save
        )
        self.save_btn.pack(side="right")
        
        self.test_btn = ctk.CTkButton(
            btn_frame,
            text="🧪 Testar",
            width=100,
            height=40,
            font=("Segoe UI", 13),
            fg_color=self.theme["bg_tertiary"],
            hover_color=self.theme["bg_secondary"],
            text_color=self.theme["text_primary"],
            command=self._test_webhook
        )
        self.test_btn.pack(side="right", padx=(0, 10))
    
    def _load_values(self):
        """Carrega valores atuais."""
        self.lang_var.set(self.config_service.language)
        self.discord_enabled_var.set(self.config_service.discord_enabled)
        
        if self.config_service.discord_webhook:
            self.webhook_entry.insert(0, self.config_service.discord_webhook)
            self._update_status_indicator()
    
    def _on_switch_change(self):
        """Callback quando switch muda."""
        self._update_status_indicator()
    
    def _on_webhook_change(self, event=None):
        """Callback quando URL muda."""
        self._update_status_indicator()
    
    def _update_status_indicator(self):
        """Atualiza indicador de status do webhook."""
        url = self.webhook_entry.get().strip()
        enabled = self.discord_enabled_var.get()
        
        if not enabled:
            self.status_label.configure(text="", text_color=self.theme["text_muted"])
            self.webhook_entry.configure(border_color=self.theme["border"])
        elif not url:
            self.status_label.configure(text="", text_color=self.theme["text_muted"])
            self.webhook_entry.configure(border_color=self.theme["border"])
        elif self._is_valid_webhook(url):
            self.status_label.configure(text="✓", text_color=self.theme["success"])
            self.webhook_entry.configure(border_color=self.theme["success"])
        else:
            self.status_label.configure(text="✗", text_color=self.theme["error"])
            self.webhook_entry.configure(border_color=self.theme["error"])
    
    def _is_valid_webhook(self, url: str) -> bool:
        """Verifica se URL é válida."""
        return (url.startswith('https://discord.com/api/webhooks/') or 
                url.startswith('https://discordapp.com/api/webhooks/'))
    
    def _save(self):
        """Salva configurações."""
        # Validação
        webhook_url = self.webhook_entry.get().strip()
        enabled = self.discord_enabled_var.get()
        
        if enabled and webhook_url and not self._is_valid_webhook(webhook_url):
            self._show_message("Erro", "URL do webhook inválida!\n\nDeve começar com:\nhttps://discord.com/api/webhooks/")
            return
        
        # Atualiza valores
        self.config_service.language = self.lang_var.get()
        self.config_service.discord_webhook = webhook_url
        self.config_service.discord_enabled = enabled
        
        # Salva em arquivo
        if self.config_service.save():
            # Feedback visual
            self.save_btn.configure(text="✓ Salvo!", fg_color=self.theme["success"])
            self.after(1000, self._close_after_save)
        else:
            self._show_message("Erro", "Não foi possível salvar as configurações.")
    
    def _close_after_save(self):
        """Fecha após salvar."""
        if self.on_save:
            self.on_save()
        self.destroy()
    
    def _test_webhook(self):
        """Testa o webhook do Discord."""
        webhook_url = self.webhook_entry.get().strip()
        
        if not webhook_url:
            self._show_message("Aviso", "Digite uma URL de webhook primeiro!")
            return
        
        if not self._is_valid_webhook(webhook_url):
            self._show_message("Erro", "URL de webhook inválida!")
            return
        
        # Feedback visual
        self.test_btn.configure(text="⏳ Enviando...", state="disabled")
        
        # Envia mensagem de teste
        import requests
        import threading
        
        def send_test():
            try:
                payload = {
                    "embeds": [{
                        "title": "🧪 Teste de Webhook",
                        "description": "Se você está vendo isso, o webhook está funcionando corretamente!",
                        "color": 0x22C55E,
                        "footer": {"text": "Loot Logger by Kazz"}
                    }]
                }
                
                response = requests.post(webhook_url, json=payload, timeout=10)
                
                if response.status_code in (200, 204):
                    self.after(0, lambda: self._test_success())
                else:
                    self.after(0, lambda: self._test_fail(f"Erro HTTP: {response.status_code}"))
            except Exception as e:
                self.after(0, lambda: self._test_fail(str(e)))
        
        threading.Thread(target=send_test, daemon=True).start()
    
    def _test_success(self):
        """Webhook testado com sucesso."""
        self.test_btn.configure(text="✓ Sucesso!", fg_color=self.theme["success"], state="normal")
        self.after(2000, lambda: self.test_btn.configure(
            text="🧪 Testar", 
            fg_color=self.theme["bg_tertiary"]
        ))
    
    def _test_fail(self, error: str):
        """Webhook falhou no teste."""
        self.test_btn.configure(text="✗ Falhou", fg_color=self.theme["error"], state="normal")
        self._show_message("Erro", f"Falha ao testar webhook:\n{error}")
        self.after(2000, lambda: self.test_btn.configure(
            text="🧪 Testar", 
            fg_color=self.theme["bg_tertiary"]
        ))
    
    def _show_message(self, title: str, message: str):
        """Mostra mensagem."""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
