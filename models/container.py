"""Container model - representa um loot bag ou chest."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class LootItem:
    """Representa um item de loot."""
    object_id: int
    item_id: str
    item_name: str
    quantity: int
    owner: Optional[str] = None


@dataclass
class Container:
    """Representa um container (loot bag, chest, etc)."""
    id: int
    uuid: Optional[str] = None
    type: str = "unknown"  # "player", "monster", "chest"
    owner: Optional[str] = None
    items: Dict[int, LootItem] = field(default_factory=dict)
