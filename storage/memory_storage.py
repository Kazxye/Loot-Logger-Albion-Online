"""
Memory Storage - Storage central em memória
Baseado em memory-storage.js
"""

from .players_storage import PlayersStorage
from .loots_storage import LootsStorage
from .containers_storage import ContainersStorage


class MemoryStorage:
    """Storage central em memória."""
    
    def __init__(self):
        self.players = PlayersStorage()
        self.loots = LootsStorage()
        self.containers = ContainersStorage()
    
    def clear(self):
        """Limpa todos os storages."""
        self.players.clear()
        self.loots.clear()
        self.containers.clear()


# Instância global
storage = MemoryStorage()
