"""
Filter Panel - Painel de filtros moderno e compacto
Feito por Kazz
v3.1 - Cores padrão Albion Online, sem emojis extras
"""

import customtkinter as ctk
from typing import Callable, Optional, Set, Dict


# ============================================
# PADRÕES DE CATEGORIAS DE ITENS
# ============================================

CATEGORY_PATTERNS = {
    "equipment": {
        "name": "Equipamentos",
        "patterns": ["_HEAD", "_ARMOR", "_SHOES", "_BAG", "_CAPE", "_2H_", "_MAIN_", "_OFF_", "_CAPEITEM", "MOUNT_"],
    },
    "consumable": {
        "name": "Consumíveis", 
        "patterns": ["POTION", "FOOD", "MEAL", "FISH", "COOKED", "PIE", "SOUP", "STEW", "SALAD", "SANDWICH", "BREW"],
    },
    "resource": {
        "name": "Recursos",
        "patterns": ["_ORE", "_HIDE", "_FIBER", "_WOOD", "_ROCK", "_LEATHER", "_CLOTH", "_METALBAR", "_PLANKS", "_STONEBLOCK"],
    },
    "rune": {
        "name": "Runas/Almas",
        "patterns": ["RUNE", "SOUL", "RELIC", "SHARD_AVALON"],
    },
    "other": {
        "name": "Outros",
        "patterns": [],
    }
}


def get_item_category(item_id: str) -> str:
    """Retorna a categoria de um item."""
    if not item_id:
        return "other"
    
    item_upper = item_id.upper()
    
    for category, data in CATEGORY_PATTERNS.items():
        if category == "other":
            continue
        for pattern in data["patterns"]:
            if pattern in item_upper:
                return category
    
    return "other"


def is_category_match(item_id: str, category: str) -> bool:
    """Verifica se item pertence a uma categoria."""
    return get_item_category(item_id) == category


# ============================================
# CORES DOS TIERS (Padrão Albion Online)
# ============================================

TIER_COLORS = {
    4: {"bg": "#3B82F6", "text": "#FFFFFF", "name": "T4"},   # Azul
    5: {"bg": "#EF4444", "text": "#FFFFFF", "name": "T5"},   # Vermelho
    6: {"bg": "#F97316", "text": "#000000", "name": "T6"},   # Laranja
    7: {"bg": "#EAB308", "text": "#000000", "name": "T7"},   # Amarelo
    8: {"bg": "#FFFFFF", "text": "#000000", "name": "T8"},   # Branco
}


class FilterPanel(ctk.CTkFrame):
    """Painel lateral com filtros modernos."""
    
    def __init__(
        self, 
        master, 
        theme: dict,
        on_filter_change: Optional[Callable[[Set[str]], None]] = None,
        on_tier_filter_change: Optional[Callable[[Set[int], bool], None]] = None,
        on_item_filter_change: Optional[Callable[[dict], None]] = None,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=theme["bg_secondary"],
            corner_radius=0,
            width=320,
            **kwargs
        )
        self.theme = theme
        self.on_filter_change = on_filter_change
        self.on_tier_filter_change = on_tier_filter_change
        self.on_item_filter_change = on_item_filter_change
        
        # Estado dos filtros
        self.selected_tiers: Set[int] = {4, 5, 6, 7, 8}
        self.show_rare_only: bool = False
        self.selected_categories: Set[str] = {"equipment", "consumable", "resource", "rune", "other"}
        
        # Jogadores (looters)
        self.looters: Set[str] = set()
        self.selected_looters: Set[str] = set()
        self.looter_widgets: Dict[str, dict] = {}
        self.looter_loot_count: Dict[str, int] = {}
        
        # Widgets
        self.tier_buttons: Dict[int, ctk.CTkButton] = {}
        self.category_buttons: Dict[str, ctk.CTkButton] = {}
        
        self.pack_propagate(False)
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets com design moderno."""
        
        # Container com scroll
        self.main_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.theme["scrollbar_fg"],
            scrollbar_button_hover_color=self.theme["scrollbar_hover"]
        )
        self.main_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # ===== HEADER =====
        self._create_header()
        
        # ===== SEÇÃO: TIERS RAROS (DESTAQUE) =====
        self._create_rare_section()
        
        # ===== SEÇÃO: TIERS (BADGES) =====
        self._create_tier_section()
        
        # ===== SEÇÃO: CATEGORIAS =====
        self._create_category_section()
        
        # ===== SEÇÃO: JOGADORES =====
        self._create_players_section()
    
    def _create_header(self):
        """Cria o cabeçalho."""
        header = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        header.pack(fill="x", pady=(10, 15))
        
        # Título sem emoji
        ctk.CTkLabel(
            header,
            text="Filtros",
            font=("Segoe UI", 18, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(side="left", padx=10)
        
        # Botão Reset
        reset_btn = ctk.CTkButton(
            header,
            text="↺",
            width=32,
            height=32,
            corner_radius=8,
            fg_color=self.theme["bg_tertiary"],
            hover_color=self.theme["bg_hover"],
            text_color=self.theme["text_secondary"],
            font=("Segoe UI", 14),
            command=self._reset_filters
        )
        reset_btn.pack(side="right", padx=10)
    
    def _create_rare_section(self):
        """Cria seção de filtro de raros com destaque."""
        # Container com borda destacada
        rare_container = ctk.CTkFrame(
            self.main_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=12,
            border_width=2,
            border_color=self.theme["warning"]
        )
        rare_container.pack(fill="x", padx=10, pady=(0, 15))
        
        inner = ctk.CTkFrame(rare_container, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=12)
        
        # Checkbox grande e destacado
        self.rare_var = ctk.BooleanVar(value=False)
        
        rare_frame = ctk.CTkFrame(inner, fg_color="transparent")
        rare_frame.pack(fill="x")
        
        # Texto (sem emoji)
        text_frame = ctk.CTkFrame(rare_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            text_frame,
            text="Tiers Raros",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme["warning"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame,
            text="T4.4, T5.3+, T6.2+, T7.1+, T8",
            font=("Segoe UI", 10),
            text_color=self.theme["text_muted"]
        ).pack(anchor="w")
        
        # Switch
        self.rare_switch = ctk.CTkSwitch(
            rare_frame,
            text="",
            variable=self.rare_var,
            width=50,
            height=26,
            fg_color=self.theme["bg_secondary"],
            progress_color=self.theme["warning"],
            button_color=self.theme["text_secondary"],
            button_hover_color=self.theme["text_primary"],
            command=self._on_rare_change
        )
        self.rare_switch.pack(side="right")
    
    def _create_tier_section(self):
        """Cria seção de filtro por tier com badges coloridos."""
        # Header da seção (sem emoji)
        section_header = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section_header.pack(fill="x", padx=10, pady=(0, 8))
        
        ctk.CTkLabel(
            section_header,
            text="Filtrar por Tier",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(side="left")
        
        # Container dos badges
        tier_container = ctk.CTkFrame(
            self.main_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=10
        )
        tier_container.pack(fill="x", padx=10, pady=(0, 15))
        
        # Badges de tier em uma linha
        badges_frame = ctk.CTkFrame(tier_container, fg_color="transparent")
        badges_frame.pack(fill="x", padx=8, pady=10)
        
        for tier in [4, 5, 6, 7, 8]:
            colors = TIER_COLORS[tier]
            
            btn = ctk.CTkButton(
                badges_frame,
                text=colors["name"],
                width=45,
                height=34,
                corner_radius=8,
                fg_color=colors["bg"],
                hover_color=colors["bg"],
                text_color=colors["text"],
                font=("Segoe UI", 12, "bold"),
                command=lambda t=tier: self._toggle_tier(t)
            )
            btn.pack(side="left", padx=2, expand=True)
            self.tier_buttons[tier] = btn
    
    def _create_category_section(self):
        """Cria seção de filtro por categoria."""
        # Header da seção (sem emoji)
        section_header = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section_header.pack(fill="x", padx=10, pady=(0, 8))
        
        ctk.CTkLabel(
            section_header,
            text="Categorias",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(side="left")
        
        # Container das categorias
        cat_container = ctk.CTkFrame(
            self.main_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=10
        )
        cat_container.pack(fill="x", padx=10, pady=(0, 15))
        
        inner = ctk.CTkFrame(cat_container, fg_color="transparent")
        inner.pack(fill="x", padx=8, pady=8)
        
        # Lista de categorias (sem emojis)
        categories = ["equipment", "consumable", "resource", "rune", "other"]
        
        for i, cat_key in enumerate(categories):
            cat_data = CATEGORY_PATTERNS[cat_key]
            
            btn = ctk.CTkButton(
                inner,
                text=cat_data['name'],
                height=32,
                corner_radius=8,
                fg_color=self.theme["accent"],
                hover_color=self.theme["accent_hover"],
                text_color="#FFFFFF",
                font=("Segoe UI", 11, "bold"),
                anchor="center",
                command=lambda c=cat_key: self._toggle_category(c)
            )
            btn.pack(fill="x", pady=2)
            self.category_buttons[cat_key] = btn
    
    def _create_players_section(self):
        """Cria seção de filtro por jogadores."""
        # Header da seção
        section_header = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        section_header.pack(fill="x", padx=10, pady=(5, 8))
        
        ctk.CTkLabel(
            section_header,
            text="👥 Looters",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(side="left")
        
        self.player_count_label = ctk.CTkLabel(
            section_header,
            text="0",
            font=("Segoe UI", 11),
            text_color=self.theme["text_muted"]
        )
        self.player_count_label.pack(side="right")
        
        # Busca
        search_frame = ctk.CTkFrame(
            self.main_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=8,
            height=38
        )
        search_frame.pack(fill="x", padx=10, pady=(0, 8))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Segoe UI Emoji", 12)
        ).pack(side="left", padx=(10, 5))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar...",
            height=34,
            border_width=0,
            fg_color="transparent",
            text_color=self.theme["text_primary"],
            placeholder_text_color=self.theme["text_muted"],
            font=("Segoe UI", 11)
        )
        self.search_entry.pack(side="left", fill="both", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Botões de ação
        action_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        ctk.CTkButton(
            action_frame,
            text="✓ Todos",
            height=30,
            corner_radius=6,
            fg_color=self.theme["success"],
            hover_color=self.theme["success_hover"],
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self._select_all_players
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))
        
        ctk.CTkButton(
            action_frame,
            text="✕ Nenhum",
            height=30,
            corner_radius=6,
            fg_color=self.theme["error"],
            hover_color=self.theme["error_hover"],
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self._select_no_players
        ).pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        # Lista de jogadores
        self.players_container = ctk.CTkFrame(
            self.main_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=10
        )
        self.players_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self._create_players_placeholder()
    
    def _create_players_placeholder(self):
        """Cria placeholder quando não há jogadores."""
        self.placeholder = ctk.CTkFrame(self.players_container, fg_color="transparent")
        self.placeholder.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            self.placeholder,
            text="🎮",
            font=("Segoe UI Emoji", 28)
        ).pack(pady=(0, 8))
        
        ctk.CTkLabel(
            self.placeholder,
            text="Aguardando looters...",
            font=("Segoe UI", 11),
            text_color=self.theme["text_muted"]
        ).pack()
    
    # ============================================
    # CALLBACKS E LÓGICA
    # ============================================
    
    def _toggle_tier(self, tier: int):
        """Alterna seleção de um tier."""
        if tier in self.selected_tiers:
            self.selected_tiers.discard(tier)
            # Visual: desativado
            self.tier_buttons[tier].configure(
                fg_color=self.theme["bg_secondary"],
                text_color=self.theme["text_muted"]
            )
        else:
            self.selected_tiers.add(tier)
            # Visual: ativado
            colors = TIER_COLORS[tier]
            self.tier_buttons[tier].configure(
                fg_color=colors["bg"],
                text_color=colors["text"]
            )
        
        self._notify_tier_change()
    
    def _toggle_category(self, category: str):
        """Alterna seleção de uma categoria."""
        if category in self.selected_categories:
            self.selected_categories.discard(category)
            # Visual: desativado
            self.category_buttons[category].configure(
                fg_color=self.theme["bg_secondary"],
                text_color=self.theme["text_muted"]
            )
        else:
            self.selected_categories.add(category)
            # Visual: ativado
            self.category_buttons[category].configure(
                fg_color=self.theme["accent"],
                text_color="#FFFFFF"
            )
        
        self._notify_item_filter_change()
    
    def _on_rare_change(self):
        """Callback quando filtro de raros muda."""
        self.show_rare_only = self.rare_var.get()
        self._notify_tier_change()
    
    def _notify_tier_change(self):
        """Notifica mudança nos filtros de tier."""
        if self.on_tier_filter_change:
            self.on_tier_filter_change(self.selected_tiers, self.show_rare_only)
    
    def _notify_item_filter_change(self):
        """Notifica mudança nos filtros de categoria."""
        if self.on_item_filter_change:
            self.on_item_filter_change({
                "categories": self.selected_categories.copy()
            })
    
    def _reset_filters(self):
        """Reseta todos os filtros para padrão."""
        # Reset tiers
        self.selected_tiers = {4, 5, 6, 7, 8}
        for tier, btn in self.tier_buttons.items():
            colors = TIER_COLORS[tier]
            btn.configure(fg_color=colors["bg"], text_color=colors["text"])
        
        # Reset categorias
        self.selected_categories = {"equipment", "consumable", "resource", "rune", "other"}
        for cat, btn in self.category_buttons.items():
            btn.configure(fg_color=self.theme["accent"], text_color="#FFFFFF")
        
        # Reset raros
        self.rare_var.set(False)
        self.show_rare_only = False
        
        # Reset jogadores
        self._select_all_players()
        
        # Notifica
        self._notify_tier_change()
        self._notify_item_filter_change()
    
    # ============================================
    # GERENCIAMENTO DE JOGADORES
    # ============================================
    
    def add_player(self, player_name: str):
        """Adiciona um looter à lista."""
        if not player_name:
            return
        
        # Atualiza contador se já existe
        if player_name in self.looter_loot_count:
            self.looter_loot_count[player_name] += 1
            if player_name in self.looter_widgets:
                count = self.looter_loot_count[player_name]
                self.looter_widgets[player_name]["count"].configure(text=str(count))
            return
        
        # Remove placeholder
        if hasattr(self, 'placeholder') and self.placeholder.winfo_exists():
            self.placeholder.destroy()
        
        self.looter_loot_count[player_name] = 1
        self.looters.add(player_name)
        self.selected_looters.add(player_name)
        
        # Cria widget do jogador
        player_frame = ctk.CTkFrame(
            self.players_container,
            fg_color="transparent",
            height=36
        )
        player_frame.pack(fill="x", padx=5, pady=2)
        player_frame.pack_propagate(False)
        
        var = ctk.BooleanVar(value=True)
        
        cb = ctk.CTkCheckBox(
            player_frame,
            text="",
            variable=var,
            width=20,
            height=20,
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_hover"],
            border_color=self.theme["border"],
            command=lambda p=player_name: self._on_player_toggle(p)
        )
        cb.pack(side="left", padx=(8, 6))
        
        display_name = player_name[:16] + "..." if len(player_name) > 16 else player_name
        name_lbl = ctk.CTkLabel(
            player_frame,
            text=display_name,
            font=("Segoe UI", 11),
            text_color=self.theme["text_primary"],
            anchor="w"
        )
        name_lbl.pack(side="left", fill="x", expand=True)
        
        count_lbl = ctk.CTkLabel(
            player_frame,
            text="1",
            font=("Segoe UI", 10, "bold"),
            text_color=self.theme["accent"],
            width=30
        )
        count_lbl.pack(side="right", padx=(0, 8))
        
        self.looter_widgets[player_name] = {
            "frame": player_frame,
            "var": var,
            "checkbox": cb,
            "name": name_lbl,
            "count": count_lbl
        }
        
        self._update_player_count()
    
    def _on_player_toggle(self, player_name: str):
        """Callback quando checkbox de jogador muda."""
        if player_name not in self.looter_widgets:
            return
        
        var = self.looter_widgets[player_name]["var"]
        
        if var.get():
            self.selected_looters.add(player_name)
        else:
            self.selected_looters.discard(player_name)
        
        if self.on_filter_change:
            self.on_filter_change(self.selected_looters)
    
    def _on_search(self, event=None):
        """Filtra jogadores por busca."""
        search = self.search_entry.get().lower().strip()
        
        for name, widgets in self.looter_widgets.items():
            if not search or search in name.lower():
                widgets["frame"].pack(fill="x", padx=5, pady=2)
            else:
                widgets["frame"].pack_forget()
    
    def _select_all_players(self):
        """Seleciona todos os jogadores."""
        for name, widgets in self.looter_widgets.items():
            widgets["var"].set(True)
            self.selected_looters.add(name)
        
        if self.on_filter_change:
            self.on_filter_change(self.selected_looters)
    
    def _select_no_players(self):
        """Deseleciona todos os jogadores."""
        for name, widgets in self.looter_widgets.items():
            widgets["var"].set(False)
        
        self.selected_looters.clear()
        
        if self.on_filter_change:
            self.on_filter_change(self.selected_looters)
    
    def _update_player_count(self):
        """Atualiza contador de jogadores."""
        self.player_count_label.configure(text=str(len(self.looters)))
    
    # ============================================
    # MÉTODOS PÚBLICOS
    # ============================================
    
    def get_selected_players(self) -> Optional[Set[str]]:
        """Retorna jogadores selecionados."""
        if not self.looters:
            return None
        if not self.selected_looters or self.selected_looters == self.looters:
            return None
        return self.selected_looters.copy()
    
    def get_item_filters(self) -> dict:
        """Retorna filtros de itens."""
        return {
            "categories": self.selected_categories.copy()
        }
    
    def get_tier_filter(self) -> tuple:
        """Retorna filtros de tier."""
        return (self.selected_tiers.copy(), self.show_rare_only)
    
    def clear_players(self):
        """Limpa lista de jogadores."""
        for widgets in self.looter_widgets.values():
            try:
                widgets["frame"].destroy()
            except:
                pass
        
        self.looters.clear()
        self.selected_looters.clear()
        self.looter_widgets.clear()
        self.looter_loot_count.clear()
        
        self._update_player_count()
        self._create_players_placeholder()
    
    def clear(self):
        """Alias para clear_players."""
        self.clear_players()
