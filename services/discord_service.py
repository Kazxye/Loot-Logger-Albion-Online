"""
Discord Service - Envia notificações para webhook do Discord
"""

import requests
import threading
from datetime import datetime
from typing import Optional


class DiscordService:
    """Serviço de notificações Discord."""
    
    def __init__(self):
        self._webhook_url: Optional[str] = None
        self._enabled = False
    
    @property
    def enabled(self) -> bool:
        return self._enabled and self._webhook_url is not None
    
    def set_webhook(self, url: str):
        """Define a URL do webhook."""
        if url and url.startswith("https://discord"):
            self._webhook_url = url
            self._enabled = True
    
    def disable(self):
        """Desabilita o serviço."""
        self._enabled = False
    
    def send_loot_event(self, event):
        """Envia evento de loot para o Discord."""
        if not self.enabled:
            return
        
        # Envia em thread separada
        thread = threading.Thread(target=self._send_loot_async, args=(event,))
        thread.daemon = True
        thread.start()
    
    def _send_loot_async(self, event):
        """Envia loot de forma assíncrona."""
        try:
            embed = {
                "title": "💰 Loot Detectado",
                "color": 0xFF6B35,
                "fields": [
                    {
                        "name": "Item",
                        "value": f"**{event.quantity}x** {event.item_name}",
                        "inline": True
                    },
                    {
                        "name": "Item ID",
                        "value": f"`{event.item_id}`",
                        "inline": True
                    },
                    {
                        "name": "Pegou",
                        "value": event.looted_by.format_name(),
                        "inline": True
                    },
                    {
                        "name": "De",
                        "value": event.looted_from.format_name(),
                        "inline": True
                    }
                ],
                "timestamp": event.timestamp.isoformat(),
                "footer": {"text": "Loot Logger by Kazz"}
            }
            
            payload = {"embeds": [embed]}
            
            requests.post(self._webhook_url, json=payload, timeout=10)
            
        except Exception as e:
            print(f"[AVISO] Erro ao enviar para Discord: {e}")
    
    def send_status(self, message: str, is_online: bool = True):
        """Envia status para o Discord."""
        if not self.enabled:
            return
        
        thread = threading.Thread(target=self._send_status_async, args=(message, is_online))
        thread.daemon = True
        thread.start()
    
    def _send_status_async(self, message: str, is_online: bool):
        """Envia status de forma assíncrona."""
        try:
            color = 0x22C55E if is_online else 0xEF4444
            
            embed = {
                "description": message,
                "color": color,
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {"text": "Loot Logger by Kazz"}
            }
            
            payload = {"embeds": [embed]}
            
            requests.post(self._webhook_url, json=payload, timeout=10)
            
        except Exception:
            pass


# Instância global
discord_service = DiscordService()
