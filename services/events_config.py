"""
Events Config - Carrega configuração de códigos de eventos
Baseado em config.js
"""

import requests
from typing import Optional
from dataclasses import dataclass


@dataclass
class EventCodes:
    """Códigos dos eventos do Photon."""
    EvNewCharacter: int = 0
    EvNewEquipmentItem: int = 0
    EvNewSiegeBannerItem: int = 0
    EvNewSimpleItem: int = 0
    EvNewLoot: int = 0
    EvAttachItemContainer: int = 0
    EvDetachItemContainer: int = 0
    EvCharacterStats: int = 0
    EvOtherGrabbedLoot: int = 0
    EvNewLootChest: int = 0
    EvInventoryPutItem: int = 0
    OpJoin: int = 0
    OpInventoryMoveItem: int = 0


class EventsConfigService:
    """Serviço de configuração de eventos."""
    
    CONFIG_URL = "https://matheus.sampaio.us/ao-loot-logger-configs/events-v9.0.0.json"
    
    def __init__(self):
        self.events = EventCodes()
        self._loaded = False
    
    def load(self) -> bool:
        """Carrega configuração de eventos da URL."""
        try:
            print("[INFO] Carregando configuração de eventos...")
            response = requests.get(self.CONFIG_URL, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Mapeia os códigos
            self.events.EvNewCharacter = data.get("EvNewCharacter", 0)
            self.events.EvNewEquipmentItem = data.get("EvNewEquipmentItem", 0)
            self.events.EvNewSiegeBannerItem = data.get("EvNewSiegeBannerItem", 0)
            self.events.EvNewSimpleItem = data.get("EvNewSimpleItem", 0)
            self.events.EvNewLoot = data.get("EvNewLoot", 0)
            self.events.EvAttachItemContainer = data.get("EvAttachItemContainer", 0)
            self.events.EvDetachItemContainer = data.get("EvDetachItemContainer", 0)
            self.events.EvCharacterStats = data.get("EvCharacterStats", 0)
            self.events.EvOtherGrabbedLoot = data.get("EvOtherGrabbedLoot", 0)
            self.events.EvNewLootChest = data.get("EvNewLootChest", 0)
            self.events.EvInventoryPutItem = data.get("EvInventoryPutItem", 0)
            self.events.OpJoin = data.get("OpJoin", 0)
            self.events.OpInventoryMoveItem = data.get("OpInventoryMoveItem", 0)
            
            self._loaded = True
            print("[INFO] Configuração de eventos carregada!")
            return True
            
        except Exception as e:
            print(f"[ERRO] Falha ao carregar configuração: {e}")
            return False


# Instância global
events_config = EventsConfigService()
