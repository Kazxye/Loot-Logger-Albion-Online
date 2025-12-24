"""
Icons - Gerenciador de ícones (Emojis)
Feito por Kazz
"""

# Mapeamento de ícones: nome -> emoji
ICON_MAP = {
    # Controles principais
    "play": "▶",
    "stop": "⏹",
    "download": "📥",
    "export": "📤",
    
    # Tema
    "moon": "🌙",
    "sun": "☀",
    
    # Filtros e busca
    "search": "🔍",
    "filter": "⚙",
    "users": "👥",
    "user": "👤",
    "times": "✕",
    "check": "✓",
    
    # Status
    "circle": "●",
    
    # Loot
    "box": "📦",
    "sack": "💰",
    "skull": "💀",
    
    # Navegação
    "arrow-left": "←",
    "arrow-right": "→",
    
    # Ações
    "refresh": "🔄",
    "trash": "🗑",
    "gear": "⚙",
    "info": "ℹ",
    
    # App
    "backpack": "🎒",
    "gamepad": "🎮",
}


def get_icon(name: str, color: str = None, size: int = None):
    """
    Retorna None - não usamos mais FontAwesome.
    Mantido para compatibilidade.
    """
    return None


def get_emoji(name: str) -> str:
    """Obtém o emoji para um ícone."""
    return ICON_MAP.get(name, "?")


def is_fontawesome_available() -> bool:
    """FontAwesome não está mais disponível."""
    return False
