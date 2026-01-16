"""
Players Storage - Armazena informações dos jogadores
Baseado em players-storage.js
"""

from typing import Optional, Dict
from dataclasses import dataclass, field


@dataclass
class Player:
    """Representa um jogador."""
    name: str
    guild: str = ""
    alliance: str = ""
    
    def format_name(self) -> str:
        """Formata nome com guild/alliance."""
        parts = []
        if self.alliance:
            parts.append(f"{{{self.alliance}}}")
        if self.guild:
            parts.append(f"[{self.guild}]")
        parts.append(self.name)
        return " ".join(parts)


class PlayersStorage:
    """Armazena jogadores detectados."""
    
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.self_player: Optional[Player] = None
    
    def add(self, player_name: str, guild_name: str = "", alliance_name: str = "") -> Player:
        """Adiciona um jogador."""
        player = Player(
            name=player_name,
            guild=guild_name or "",
            alliance=alliance_name or ""
        )
        self.players[player_name] = player
        return player
    
    def get_by_name(self, player_name: str) -> Optional[Player]:
        """Busca jogador pelo nome."""
        return self.players.get(player_name)
    
    def get_or_create(self, player_name: str, guild_name: str = "", alliance_name: str = "") -> Player:
        """Busca ou cria jogador."""
        player = self.get_by_name(player_name)
        if player is None:
            player = self.add(player_name, guild_name, alliance_name)
        return player
    
    def set_self(self, player: Player):
        """Define o jogador atual (self)."""
        self.self_player = player
        print(f"[INFO] Jogador identificado: {player.format_name()}")
    
    def clear(self):
        """Limpa todos os jogadores."""
        self.players.clear()
        self.self_player = None
