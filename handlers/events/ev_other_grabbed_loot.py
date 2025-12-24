"""
EvOtherGrabbedLoot - Evento quando OUTRO jogador pega um loot
Este é o evento PRINCIPAL para capturar loot de outros jogadores!
Baseado em ev-other-grabbed-loot.js
"""

from datetime import datetime
from typing import Optional, Callable

from storage import storage
from services import items_service


def handle(event: dict, on_loot: Optional[Callable] = None):
    """
    Processa evento EvOtherGrabbedLoot.
    
    Parâmetros:
    - [1] = lootedFrom (string) - nome do dono original
    - [2] = lootedBy (string) - nome de quem pegou
    - [3] = isSilver (bool) - se é prata
    - [4] = itemNumId (int) - ID numérico do item
    - [5] = quantity (int) - quantidade
    """
    params = event.get('parameters', {})
    
    is_silver = params.get(3, False)
    if is_silver:
        return
    
    looted_from_name = params.get(1)
    if not is_silver and not isinstance(looted_from_name, str):
        return
    
    looted_by_name = params.get(2)
    if not isinstance(looted_by_name, str):
        return
    
    item_num_id = params.get(4)
    if not is_silver and not isinstance(item_num_id, int):
        return
    
    quantity = params.get(5)
    if not isinstance(quantity, int):
        return
    
    # Busca info do item
    item = items_service.get(item_num_id)
    
    if item is None:
        item_id = f"UNKNOWN_{item_num_id}"
        item_name = f"Item Desconhecido ({item_num_id})"
    else:
        item_id = item.item_id
        item_name = item.get_name(items_service.locale)
    
    # Busca ou cria jogadores
    looted_by = storage.players.get_by_name(looted_by_name)
    if looted_by is None:
        looted_by = storage.players.add(looted_by_name)
    
    looted_from = storage.players.get_by_name(looted_from_name)
    if looted_from is None:
        looted_from = storage.players.add(looted_from_name)
    
    print(f"[LOOT] {looted_by.format_name()} pegou {quantity}x {item_name} de {looted_from.format_name()}")
    
    # Callback para GUI/Discord
    if on_loot:
        from models import LootEvent
        loot_event = LootEvent(
            timestamp=datetime.utcnow(),
            item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            looted_by=looted_by,
            looted_from=looted_from
        )
        on_loot(loot_event)
