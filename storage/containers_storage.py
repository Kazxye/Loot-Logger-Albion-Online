"""
Containers Storage - Armazena containers (loot bags, chests)
Baseado em containers-storage.js
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Container:
    """Representa um container (loot bag, chest)."""
    id: int
    uuid: Optional[str] = None
    type: Optional[str] = None  # 'monster', 'player', 'chest'
    owner: Optional[str] = None
    items: Dict[int, Any] = field(default_factory=dict)  # position -> Loot


class ContainersStorage:
    """Armazena containers detectados."""
    
    def __init__(self):
        self.containers: Dict[int, Container] = {}
    
    def add(self, id: int, uuid: str = None, type: str = None, owner: str = None) -> Container:
        """Adiciona um container."""
        container = Container(
            id=id,
            uuid=uuid,
            type=type,
            owner=owner,
            items={}
        )
        self.containers[id] = container
        return container
    
    def get_by_id(self, id: int) -> Optional[Container]:
        """Busca container pelo id."""
        return self.containers.get(id)
    
    def get_by_uuid(self, uuid: str) -> Optional[Container]:
        """Busca container pelo uuid."""
        for container in self.containers.values():
            if container.uuid == uuid:
                return container
        return None
    
    def delete_by_id(self, id: int):
        """Remove container pelo id."""
        if id in self.containers:
            del self.containers[id]
    
    def delete_by_uuid(self, uuid: str) -> Optional[Container]:
        """Remove container pelo uuid."""
        container = self.get_by_uuid(uuid)
        if container:
            del self.containers[container.id]
        return container
    
    def clear(self):
        """Limpa todos os containers."""
        self.containers.clear()
