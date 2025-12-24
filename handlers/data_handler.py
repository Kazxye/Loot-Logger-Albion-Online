"""
Data Handler - Dispatcher principal de eventos Photon
Baseado em data-handler.js
"""

from typing import Optional, Callable, List

from services import events_config

from .events import (
    ev_new_loot,
    ev_new_simple_item,
    ev_new_equipment_item,
    ev_attach_item_container,
    ev_detach_item_container,
    ev_other_grabbed_loot,
    ev_new_character,
    ev_character_stats
)
from .responses import op_join
from .requests import op_inventory_move_item


class DataHandler:
    """Handler central de dados Photon."""
    
    def __init__(self):
        self._on_loot_callbacks: List[Callable] = []
    
    def on_loot(self, callback: Callable):
        """Registra callback para eventos de loot."""
        if callback not in self._on_loot_callbacks:
            self._on_loot_callbacks.append(callback)
    
    def clear_callbacks(self):
        """Limpa todos os callbacks."""
        self._on_loot_callbacks.clear()
    
    def _emit_loot(self, event):
        """Emite evento de loot para todos os callbacks."""
        for callback in self._on_loot_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"[ERRO] Callback de loot falhou: {e}")
    
    def handle_event(self, event: dict):
        """
        Processa um Event Data do Photon.
        
        No Albion, eventos relevantes têm eventCode = 1
        O tipo real está em parameters[252]
        """
        try:
            if not event or event.get('event_code') != 1:
                return
            
            params = event.get('parameters', {})
            event_id = params.get(252)
            
            if event_id is None:
                return
            
            codes = events_config.events
            
            # Dispatch baseado no event ID
            if event_id == codes.EvNewCharacter:
                return ev_new_character.handle(event)
            
            if event_id == codes.EvNewEquipmentItem:
                return ev_new_equipment_item.handle(event)
            
            if event_id == codes.EvNewSiegeBannerItem:
                return ev_new_equipment_item.handle(event)  # Tratamos igual
            
            if event_id == codes.EvNewSimpleItem:
                return ev_new_simple_item.handle(event)
            
            if event_id == codes.EvNewLoot:
                return ev_new_loot.handle(event)
            
            if event_id == codes.EvAttachItemContainer:
                return ev_attach_item_container.handle(event)
            
            if event_id == codes.EvDetachItemContainer:
                return ev_detach_item_container.handle(event)
            
            if event_id == codes.EvCharacterStats:
                return ev_character_stats.handle(event)
            
            if event_id == codes.EvOtherGrabbedLoot:
                return ev_other_grabbed_loot.handle(event, self._emit_loot)
        
        except Exception as e:
            print(f"[ERRO] handle_event: {e}")
    
    def handle_request(self, event: dict):
        """Processa um Operation Request do Photon."""
        try:
            params = event.get('parameters', {})
            event_id = params.get(253)
            
            if event_id is None:
                return
            
            codes = events_config.events
            
            if event_id == codes.OpInventoryMoveItem:
                return op_inventory_move_item.handle(event, self._emit_loot)
        
        except Exception as e:
            print(f"[ERRO] handle_request: {e}")
    
    def handle_response(self, event: dict):
        """Processa um Operation Response do Photon."""
        try:
            params = event.get('parameters', {})
            event_id = params.get(253)
            
            if event_id is None:
                return
            
            codes = events_config.events
            
            if event_id == codes.OpJoin:
                return op_join.handle(event)
        
        except Exception as e:
            print(f"[ERRO] handle_response: {e}")


# Instância global
data_handler = DataHandler()
