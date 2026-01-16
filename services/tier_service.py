"""
Tier Service - Detecção de tier e identificação de loot raro
"""

import re
from typing import Optional
from dataclasses import dataclass


@dataclass
class TierInfo:
    """Informações do tier de um item."""
    tier: int
    enchant: int
    tier_str: str
    is_rare: bool
    display_name: str


class TierService:
    """Serviço de detecção de tier."""
    
    # Regex para extrair tier: T4_xxx ou T4_xxx@2
    TIER_PATTERN = re.compile(r'^T(\d)_.*?(?:@(\d))?$', re.IGNORECASE)
    
    # Tiers considerados raros (configurado por Kazz)
    # 4.4, 5.3, 5.4, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3, 7.4, 8.0, 8.1, 8.2, 8.3, 8.4
    RARE_TIERS = {
        (4, 4),
        (5, 3), (5, 4),
        (6, 2), (6, 3), (6, 4),
        (7, 1), (7, 2), (7, 3), (7, 4),
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
    }
    
    # Cores dos TIERS (padrão Albion Online)
    TIER_COLORS = {
        4: "#3B82F6",  # Azul
        5: "#EF4444",  # Vermelho
        6: "#F97316",  # Laranja
        7: "#EAB308",  # Amarelo
        8: "#FFFFFF",  # Branco
    }
    
    # Cores dos ENCANTAMENTOS (padrão Albion Online)
    ENCHANT_COLORS = {
        0: None,       # Sem encantamento - usa cor do tier
        1: "#22C55E",  # Verde
        2: "#3B82F6",  # Azul
        3: "#A855F7",  # Roxo
        4: "#FFD700",  # Dourado
    }
    
    def parse_tier(self, item_id: str) -> Optional[TierInfo]:
        """Extrai informações de tier do item_id."""
        if not item_id:
            return None
        
        match = self.TIER_PATTERN.match(item_id)
        if not match:
            return None
        
        tier = int(match.group(1))
        enchant = int(match.group(2)) if match.group(2) else 0
        
        return TierInfo(
            tier=tier,
            enchant=enchant,
            tier_str=f"{tier}.{enchant}",
            is_rare=self._is_rare(tier, enchant),
            display_name=f"T{tier}.{enchant}"
        )
    
    def _is_rare(self, tier: int, enchant: int) -> bool:
        """Verifica se é raro baseado na configuração."""
        return (tier, enchant) in self.RARE_TIERS
    
    def is_item_rare(self, item_id: str) -> bool:
        """Verifica se item é raro."""
        info = self.parse_tier(item_id)
        return info.is_rare if info else False
    
    def get_tier_color(self, item_id: str) -> str:
        """Retorna cor baseada no tier e encantamento (padrão Albion)."""
        info = self.parse_tier(item_id)
        if not info:
            return "#FFFFFF"
        
        # Se tem encantamento, usa cor do encantamento
        if info.enchant > 0:
            return self.ENCHANT_COLORS.get(info.enchant, "#FFFFFF")
        
        # Senão usa cor do tier
        return self.TIER_COLORS.get(info.tier, "#FFFFFF")
    
    def get_tier_base_color(self, tier: int) -> str:
        """Retorna cor base do tier (sem encantamento)."""
        return self.TIER_COLORS.get(tier, "#FFFFFF")
    
    def get_enchant_color(self, enchant: int) -> str:
        """Retorna cor do encantamento."""
        return self.ENCHANT_COLORS.get(enchant, "#FFFFFF")


# Instância global
tier_service = TierService()
