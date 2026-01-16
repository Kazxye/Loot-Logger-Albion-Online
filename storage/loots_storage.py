"""
Loots Storage - Armazena itens de loot detectados
Baseado em loots-storage.js
"""

from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class Loot:
    """Representa um item de loot."""
    object_id: int
    item_id: str
    item_name: str
    quantity: int
    owner: Optional[str] = None


class LootsStorage:
    """Armazena loots detectados."""
    
    def __init__(self):
        self.loots: Dict[int, Loot] = {}
    
    def add(self, object_id: int, item_id: str, item_name: str, quantity: int, owner: str = None) -> Loot:
        """Adiciona um loot."""
        loot = Loot(
            object_id=object_id,
            item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            owner=owner
        )
        self.loots[object_id] = loot
        return loot
    
    def get_by_id(self, object_id: int) -> Optional[Loot]:
        """Busca loot pelo objectId."""
        return self.loots.get(object_id)
    
    def delete_by_id(self, object_id: int):
        """Remove loot pelo objectId."""
        if object_id in self.loots:
            del self.loots[object_id]
    
    def clear(self):
        """Limpa todos os loots."""
        self.loots.clear()
