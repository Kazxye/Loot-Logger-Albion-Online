"""
Config Service - Gerencia configurações do usuário
Salva em arquivo JSON local
"""

import json
import os
from typing import Optional
from dataclasses import dataclass, asdict


CONFIG_FILE = "loot_logger_config.json"


@dataclass
class UserConfig:
    """Configurações do usuário."""
    language: str = "PT-BR"  # PT-BR ou EN-US
    discord_webhook: str = ""
    discord_enabled: bool = False


class ConfigService:
    """Serviço de configurações."""
    
    def __init__(self):
        self._config = UserConfig()
        self._config_path = self._get_config_path()
    
    def _get_config_path(self) -> str:
        """Retorna caminho do arquivo de config."""
        # Tenta salvar no mesmo diretório do executável
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            parent_path = os.path.dirname(base_path)
            return os.path.join(parent_path, CONFIG_FILE)
        except:
            return CONFIG_FILE
    
    def load(self) -> bool:
        """Carrega configurações do arquivo."""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._config = UserConfig(
                        language=data.get('language', 'PT-BR'),
                        discord_webhook=data.get('discord_webhook', ''),
                        discord_enabled=data.get('discord_enabled', False)
                    )
                print(f"[INFO] Configurações carregadas")
                return True
        except Exception as e:
            print(f"[AVISO] Erro ao carregar config: {e}")
        return False
    
    def save(self) -> bool:
        """Salva configurações no arquivo."""
        try:
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._config), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[AVISO] Erro ao salvar config: {e}")
            return False
    
    @property
    def language(self) -> str:
        return self._config.language
    
    @language.setter
    def language(self, value: str):
        if value in ('PT-BR', 'EN-US'):
            self._config.language = value
    
    @property
    def discord_webhook(self) -> str:
        return self._config.discord_webhook
    
    @discord_webhook.setter
    def discord_webhook(self, value: str):
        self._config.discord_webhook = value.strip()
    
    @property
    def discord_enabled(self) -> bool:
        return self._config.discord_enabled
    
    @discord_enabled.setter
    def discord_enabled(self, value: bool):
        self._config.discord_enabled = value
    
    def is_webhook_valid(self) -> bool:
        """Verifica se webhook é válido."""
        url = self._config.discord_webhook
        return url.startswith('https://discord.com/api/webhooks/') or \
               url.startswith('https://discordapp.com/api/webhooks/')


# Instância global
config_service = ConfigService()
