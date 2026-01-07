"""Loot Event model."""

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from storage import Player


@dataclass
class LootEvent:
    """Representa um evento de loot."""
    timestamp: datetime
    item_id: str
    item_name: str
    quantity: int
    looted_by: 'Player'
    looted_from: 'Player'
    
    def to_dict(self) -> dict:
        """Converte para dicionário (para JSON export)."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'item_id': self.item_id,
            'item_name': self.item_name,
            'quantity': self.quantity,
            'looted_by': {
                'name': self.looted_by.name,
                'guild': self.looted_by.guild,
                'alliance': self.looted_by.alliance
            },
            'looted_from': {
                'name': self.looted_from.name,
                'guild': self.looted_from.guild,
                'alliance': self.looted_from.alliance
            }
        }
    
    def format_log(self) -> str:
        """Formata o evento para exibição no log."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        return (
            f"{time_str} UTC: {self.looted_by.format_name()} looted "
            f"{self.quantity}x {self.item_name} from {self.looted_from.format_name()}"
        )
    
    def __str__(self) -> str:
        return self.format_log()
