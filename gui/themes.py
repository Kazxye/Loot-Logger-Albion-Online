"""
Themes - Tema Dark + Laranja para a GUI
Design profissional para Loot Logger
Feito por Kazz
"""

# Tema Dark + Laranja (Único tema)
DARK_THEME = {
    "name": "dark",
    
    # Cores de fundo (muito escuro)
    "bg_primary": "#0A0A0B",      # Quase preto
    "bg_secondary": "#111114",    # Cinza muito escuro
    "bg_tertiary": "#18181B",     # Cards/Painéis
    "bg_hover": "#222228",        # Hover
    "bg_active": "#2A2A32",       # Active/Pressed
    
    # Bordas
    "border": "#2A2A30",          # Borda padrão
    "border_light": "#3A3A42",    # Borda clara
    "border_focus": "#FF6B35",    # Borda com foco (laranja)
    
    # Texto
    "text_primary": "#F5F5F5",    # Branco suave
    "text_secondary": "#A1A1AA",  # Cinza claro
    "text_muted": "#71717A",      # Cinza médio
    
    # Accent - LARANJA (principal)
    "accent": "#FF6B35",          # Laranja principal
    "accent_hover": "#FF8C5A",    # Laranja hover
    "accent_dark": "#E55A25",     # Laranja escuro
    "accent_muted": "#CC5529",    # Laranja muted
    "accent_glow": "#FF6B3530",   # Glow transparente
    
    # Status (apenas para Start/Stop)
    "success": "#22C55E",         # Verde
    "success_hover": "#2DD468",   # Verde hover
    "error": "#EF4444",           # Vermelho
    "error_hover": "#F87171",     # Vermelho hover
    "warning": "#F59E0B",         # Amarelo/Laranja
    "info": "#FF6B35",            # Laranja (info = accent)
    
    # Loot colors
    "loot_by": "#22C55E",         # Verde - quem pegou
    "loot_from": "#EF4444",       # Vermelho - de quem
    "loot_item": "#FF6B35",       # Laranja - nome do item
    "loot_quantity": "#F59E0B",   # Amarelo - quantidade
    
    # Scrollbar
    "scrollbar_bg": "#18181B",
    "scrollbar_fg": "#3A3A42",
    "scrollbar_hover": "#52525B",
    
    # Splash/Login
    "splash_bg": "#0A0A0B",
    "splash_glow": "#FF6B35",
    
    # Botões
    "btn_primary_bg": "#FF6B35",
    "btn_primary_hover": "#FF8C5A",
    "btn_secondary_bg": "#18181B",
    "btn_secondary_hover": "#222228",
}

# Alias para compatibilidade
LIGHT_THEME = DARK_THEME


def get_theme(name: str = "dark") -> dict:
    """Retorna o tema (sempre dark)."""
    return DARK_THEME
