"""
Loot Table - Tabela de eventos de loot em tempo real
Com filtro por item, tier e destaque para loot raro
Feito por Kazz
v2.0 - Badge de tier moderno com cores Albion Online
"""

import customtkinter as ctk
from typing import List, Optional
from datetime import datetime
import math

from gui.icons import get_emoji


# Cores padrão Albion Online
TIER_COLORS = {
    4: "#3B82F6",  # Azul
    5: "#EF4444",  # Vermelho
    6: "#F97316",  # Laranja
    7: "#EAB308",  # Amarelo
    8: "#FFFFFF",  # Branco
}

ENCHANT_COLORS = {
    0: None,       # Sem encantamento
    1: "#22C55E",  # Verde
    2: "#3B82F6",  # Azul
    3: "#A855F7",  # Roxo
    4: "#FFD700",  # Dourado
}


class TierBadge(ctk.CTkFrame):
    """Badge moderno de tier com cor do tier + borda do encantamento."""
    
    def __init__(self, master, tier: int, enchant: int, theme: dict, is_rare: bool = False, **kwargs):
        self.tier = tier
        self.enchant = enchant
        self.theme = theme
        self.is_rare = is_rare
        
        # Cores
        tier_color = TIER_COLORS.get(tier, "#FFFFFF")
        enchant_color = ENCHANT_COLORS.get(enchant, None)
        
        # Cor do texto (preto para cores claras, branco para escuras)
        text_color = "#000000" if tier in [6, 7, 8] else "#FFFFFF"
        
        # Se tem encantamento, usa borda colorida
        if enchant > 0 and enchant_color:
            border_width = 3
            border_color = enchant_color
        else:
            border_width = 0
            border_color = tier_color  # Usa mesma cor do fundo quando não há borda
        
        super().__init__(
            master,
            fg_color=tier_color,
            corner_radius=8,
            border_width=border_width,
            border_color=border_color,
            height=28,
            **kwargs
        )
        
        self.pack_propagate(False)
        
        # Container interno para centralizar
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(expand=True)
        
        # Texto do tier
        tier_text = f"T{tier}.{enchant}"
        
        label = ctk.CTkLabel(
            inner,
            text=tier_text,
            font=("Segoe UI", 11, "bold"),
            text_color=text_color
        )
        label.pack(padx=10, pady=2)
        
        # Efeito de brilho para raros
        if is_rare and enchant >= 3 and enchant_color:
            self._add_glow_effect(enchant_color)
    
    def _add_glow_effect(self, color: str):
        """Adiciona efeito de brilho sutil."""
        # Implementado via borda mais grossa para raros
        self.configure(border_width=4)


class LootEntry(ctk.CTkFrame):
    """Uma entrada individual de loot."""
    
    def __init__(self, master, theme: dict, loot_data: dict, is_rare: bool = False, **kwargs):
        super().__init__(
            master,
            fg_color=theme["bg_tertiary"],
            corner_radius=12,
            border_width=1,
            border_color=theme["accent"] if is_rare else theme["border"],
            height=80,
            **kwargs
        )
        self.theme = theme
        self.loot_data = loot_data
        self.is_rare = is_rare
        
        # Animação para loot raro
        self._pulse_running = False
        self._pulse_phase = 0
        
        self.pack_propagate(False)
        self._create_widgets()
        
        # Hover effect
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Inicia animação se for raro
        if is_rare:
            self._start_pulse()
    
    def _create_widgets(self):
        """Cria os widgets."""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Barra de destaque para loot raro (na lateral esquerda)
        if self.is_rare:
            self.rare_bar = ctk.CTkFrame(
                main_container,
                fg_color=self.theme["accent"],
                width=4,
                corner_radius=2
            )
            self.rare_bar.pack(side="left", fill="y", padx=(0, 0))
        
        # Container do conteúdo
        container = ctk.CTkFrame(main_container, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=15, pady=12)
        
        # ===== COLUNA ESQUERDA =====
        left_frame = ctk.CTkFrame(container, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Linha 1: Hora + Quantidade + Item + Tier Badge
        top_line = ctk.CTkFrame(left_frame, fg_color="transparent")
        top_line.pack(fill="x", anchor="w")
        
        # Hora com background
        time_str = self.loot_data.get("time", "00:00:00")
        time_frame = ctk.CTkFrame(
            top_line,
            fg_color=self.theme["bg_secondary"],
            corner_radius=6
        )
        time_frame.pack(side="left", padx=(0, 12))
        
        time_label = ctk.CTkLabel(
            time_frame,
            text=time_str,
            font=("Consolas", 11),
            text_color=self.theme["text_muted"]
        )
        time_label.pack(padx=8, pady=3)
        
        # Badge de Tier MODERNO (antes da quantidade)
        tier = self.loot_data.get("tier", 0)
        enchant = self.loot_data.get("enchant", 0)
        
        if tier >= 4:
            tier_badge = TierBadge(
                top_line,
                tier=tier,
                enchant=enchant,
                theme=self.theme,
                is_rare=self.is_rare
            )
            tier_badge.pack(side="left", padx=(0, 10))
        
        # Quantidade com destaque
        qty = self.loot_data.get("quantity", 1)
        qty_label = ctk.CTkLabel(
            top_line,
            text=f"{qty}x",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme["loot_quantity"]
        )
        qty_label.pack(side="left", padx=(0, 8))
        
        # Nome do item
        item_name = self.loot_data.get("item_name", "Unknown Item")
        if len(item_name) > 28:
            item_name = item_name[:28] + "..."
        
        # Cor do item baseada no encantamento ou tier
        item_color = self.loot_data.get("tier_color", self.theme["loot_item"])
        
        item_label = ctk.CTkLabel(
            top_line,
            text=item_name,
            font=("Segoe UI", 14, "bold"),
            text_color=item_color
        )
        item_label.pack(side="left")
        
        # Valor em silver (se disponível)
        silver_value = self.loot_data.get("silver_value", "")
        if silver_value:
            silver_label = ctk.CTkLabel(
                top_line,
                text=f"  💰 {silver_value}",
                font=("Segoe UI", 12, "bold"),
                text_color=self.theme["warning"]
            )
            silver_label.pack(side="left", padx=(10, 0))
        
        # Linha 2: Jogadores
        bottom_line = ctk.CTkFrame(left_frame, fg_color="transparent")
        bottom_line.pack(fill="x", anchor="w", pady=(8, 0))
        
        # Quem pegou (verde)
        looted_by = self.loot_data.get("looted_by", "Unknown")
        if len(looted_by) > 25:
            looted_by = looted_by[:25] + "..."
        
        by_label = ctk.CTkLabel(
            bottom_line,
            text=looted_by,
            font=("Segoe UI", 12),
            text_color=self.theme["loot_by"]
        )
        by_label.pack(side="left")
        
        # Seta
        arrow_label = ctk.CTkLabel(
            bottom_line,
            text="  ←  ",
            font=("Segoe UI", 12),
            text_color=self.theme["text_muted"]
        )
        arrow_label.pack(side="left")
        
        # De quem (vermelho)
        looted_from = self.loot_data.get("looted_from", "Unknown")
        if len(looted_from) > 25:
            looted_from = looted_from[:25] + "..."
        
        from_label = ctk.CTkLabel(
            bottom_line,
            text=looted_from,
            font=("Segoe UI", 12),
            text_color=self.theme["loot_from"]
        )
        from_label.pack(side="left")
        
        # ===== COLUNA DIREITA - Item ID =====
        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        item_id = self.loot_data.get("item_id", "")
        if len(item_id) > 25:
            item_id = item_id[:25] + "..."
        
        id_label = ctk.CTkLabel(
            right_frame,
            text=item_id,
            font=("Consolas", 9),
            text_color=self.theme["text_muted"]
        )
        id_label.pack(anchor="e")
    
    def _start_pulse(self):
        """Inicia animação de pulso para loot raro."""
        self._pulse_running = True
        self._animate_pulse()
    
    def _animate_pulse(self):
        """Animação de pulso na barra lateral."""
        if not self._pulse_running or not hasattr(self, 'rare_bar'):
            return
        
        self._pulse_phase += 0.1
        
        # Varia a largura da barra
        width = 4 + 3 * abs(math.sin(self._pulse_phase))
        
        try:
            self.rare_bar.configure(width=int(width))
        except:
            return
        
        # Para animação após 5 segundos (100 iterações * 50ms)
        if self._pulse_phase < 10:
            self.after(50, self._animate_pulse)
        else:
            self._pulse_running = False
            try:
                self.rare_bar.configure(width=4)
            except:
                pass
    
    def _on_enter(self, event):
        """Hover enter."""
        border_color = self.theme["accent"] if self.is_rare else self.theme["border_light"]
        self.configure(
            fg_color=self.theme["bg_hover"],
            border_color=border_color
        )
    
    def _on_leave(self, event):
        """Hover leave."""
        border_color = self.theme["accent"] if self.is_rare else self.theme["border"]
        self.configure(
            fg_color=self.theme["bg_tertiary"],
            border_color=border_color
        )
    
    def matches_filter(self, filter_text: str) -> bool:
        """Verifica se a entrada corresponde ao filtro."""
        if not filter_text:
            return True
        
        filter_text = filter_text.lower()
        item_name = self.loot_data.get("item_name", "").lower()
        item_id = self.loot_data.get("item_id", "").lower()
        looted_by = self.loot_data.get("looted_by", "").lower()
        looted_from = self.loot_data.get("looted_from", "").lower()
        tier_display = self.loot_data.get("tier_display", "").lower()
        
        return (filter_text in item_name or 
                filter_text in item_id or
                filter_text in looted_by or
                filter_text in looted_from or
                filter_text in tier_display)
    
    def destroy(self):
        """Para animação ao destruir."""
        self._pulse_running = False
        super().destroy()


class LootTable(ctk.CTkFrame):
    """Container com busca e tabela scrollável."""
    
    def __init__(self, master, theme: dict, **kwargs):
        super().__init__(
            master,
            fg_color=theme["bg_primary"],
            corner_radius=0,
            **kwargs
        )
        self.theme = theme
        self.entries: List[LootEntry] = []
        self.all_loots: List[dict] = []
        self.max_entries = 100
        self._filter_text = ""
        self._placeholder = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets."""
        # ===== BARRA DE BUSCA =====
        search_container = ctk.CTkFrame(self, fg_color=self.theme["bg_secondary"])
        search_container.pack(fill="x", padx=0, pady=0)
        
        search_inner = ctk.CTkFrame(search_container, fg_color="transparent")
        search_inner.pack(fill="x", padx=15, pady=12)
        
        # Ícone de busca
        search_icon = ctk.CTkLabel(
            search_inner,
            text=get_emoji("search"),
            font=("Segoe UI Emoji", 14)
        )
        search_icon.pack(side="left", padx=(0, 10))
        
        # Campo de busca
        self.search_entry = ctk.CTkEntry(
            search_inner,
            placeholder_text="Filtrar por item, jogador, tier...",
            height=40,
            border_width=1,
            border_color=self.theme["border"],
            fg_color=self.theme["bg_tertiary"],
            text_color=self.theme["text_primary"],
            placeholder_text_color=self.theme["text_muted"],
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Botão limpar
        self.clear_btn = ctk.CTkButton(
            search_inner,
            text="✕",
            width=40,
            height=40,
            corner_radius=8,
            fg_color=self.theme["bg_tertiary"],
            hover_color=self.theme["bg_hover"],
            text_color=self.theme["text_muted"],
            font=("Segoe UI", 14),
            command=self._clear_search
        )
        self.clear_btn.pack(side="left", padx=(10, 0))
        
        # Separador
        sep = ctk.CTkFrame(self, fg_color=self.theme["border"], height=1)
        sep.pack(fill="x")
        
        # ===== TABELA SCROLLABLE =====
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.theme["bg_primary"],
            scrollbar_button_color=self.theme["scrollbar_fg"],
            scrollbar_button_hover_color=self.theme["scrollbar_hover"]
        )
        self.scroll_frame.pack(fill="both", expand=True)
        
        # Mostra placeholder inicial
        self._show_placeholder()
    
    def _show_placeholder(self):
        """Mostra placeholder quando vazio."""
        self._hide_placeholder()
        
        self._placeholder = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self._placeholder.pack(expand=True, pady=100)
        
        # Ícone
        icon_label = ctk.CTkLabel(
            self._placeholder,
            text="🎮",
            font=("Segoe UI Emoji", 52)
        )
        icon_label.pack(pady=(0, 20))
        
        # Título
        title_label = ctk.CTkLabel(
            self._placeholder,
            text="Aguardando eventos de loot...",
            font=("Segoe UI", 18, "bold"),
            text_color=self.theme["text_secondary"]
        )
        title_label.pack(pady=(0, 8))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            self._placeholder,
            text="Inicie a captura e entre no Albion Online",
            font=("Segoe UI", 13),
            text_color=self.theme["text_muted"]
        )
        subtitle_label.pack()
    
    def _hide_placeholder(self):
        """Remove o placeholder."""
        if self._placeholder is not None:
            try:
                self._placeholder.destroy()
            except:
                pass
            self._placeholder = None
    
    def _on_search(self, event=None):
        """Callback quando busca muda."""
        self._filter_text = self.search_entry.get().strip()
        self._rebuild_view()
    
    def _clear_search(self):
        """Limpa busca."""
        self.search_entry.delete(0, "end")
        self._filter_text = ""
        self._rebuild_view()
    
    def _rebuild_view(self):
        """Reconstrói a view com base no filtro atual."""
        for entry in self.entries:
            entry.pack_forget()
        
        visible_count = 0
        for entry in self.entries:
            if entry.matches_filter(self._filter_text):
                entry.pack(fill="x", padx=10, pady=(10, 0))
                visible_count += 1
        
        if visible_count == 0 and len(self.entries) == 0:
            self._show_placeholder()
    
    def add_loot(self, loot_event, silver_value: str = "", is_rare: bool = False, tier_display: str = "", tier_color: str = "", tier: int = 0, enchant: int = 0):
        """Adiciona um novo evento de loot."""
        try:
            self._hide_placeholder()
            
            # Prepara dados
            loot_data = {
                "time": loot_event.timestamp.strftime("%H:%M:%S"),
                "item_name": loot_event.item_name,
                "item_id": loot_event.item_id,
                "quantity": loot_event.quantity,
                "looted_by": self._format_player(loot_event.looted_by),
                "looted_from": self._format_player(loot_event.looted_from),
                "silver_value": silver_value,
                "tier_display": tier_display,
                "tier_color": tier_color or self.theme["loot_item"],
                "tier": tier,
                "enchant": enchant
            }
            
            self.all_loots.insert(0, loot_data)
            
            # Cria entry
            entry = LootEntry(self.scroll_frame, self.theme, loot_data, is_rare=is_rare)
            self.entries.insert(0, entry)
            
            # Remove entries antigas
            while len(self.entries) > self.max_entries:
                old = self.entries.pop()
                old.destroy()
                if self.all_loots:
                    self.all_loots.pop()
            
            self._rebuild_view()
            
            # Scroll para o topo
            try:
                self.scroll_frame._parent_canvas.yview_moveto(0)
            except:
                pass
        except Exception as e:
            print(f"[ERRO] add_loot: {e}")
            import traceback
            traceback.print_exc()
    
    def _format_player(self, player) -> str:
        """Formata nome do jogador."""
        parts = []
        if player.alliance:
            parts.append(f"{{{player.alliance}}}")
        if player.guild:
            parts.append(f"[{player.guild}]")
        parts.append(player.name)
        return " ".join(parts)
    
    def clear(self):
        """Limpa todos os eventos."""
        for entry in self.entries:
            entry.destroy()
        self.entries.clear()
        self.all_loots.clear()
        
        self._show_placeholder()
