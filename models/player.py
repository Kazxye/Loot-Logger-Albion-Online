"""Player model."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Player:
    """Representa um jogador no jogo."""
    name: str
    guild: str = ""
    alliance: str = ""
    
    def format_name(self, include_tags: bool = True) -> str:
        """Formata o nome do jogador com guild e alliance."""
        parts = []
        
        if include_tags:
            if self.alliance:
                parts.append(f"{{{self.alliance}}}")
            if self.guild:
                parts.append(f"[{self.guild}]")
        
        parts.append(self.name)
        return " ".join(parts)
    
    def __str__(self) -> str:
        return self.format_name()
