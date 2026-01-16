"""
EvNewSimpleItem - Evento quando um item simples aparece
Baseado em ev-new-simple-item.js
"""

from storage import storage
from services import items_service


def handle(event: dict):
    """
    Processa evento EvNewSimpleItem.
    
    Parâmetros:
    - [0] = objectId (int)
    - [1] = itemNumId (int)
    - [2] = quantity (int)
    - [5] = craftedBy (NÃO deve existir para simple items)
    """
    params = event.get('parameters', {})
    
    object_id = params.get(0)
    if not isinstance(object_id, int):
        return
    
    item_num_id = params.get(1)
    if not isinstance(item_num_id, int):
        return
    
    quantity = params.get(2)
    if not isinstance(quantity, int):
        return
    
    # IMPORTANTE: Simple items NÃO devem ter craftedBy
    crafted_by = params.get(5)
    if isinstance(crafted_by, str):
        return
    
    # Busca info do item
    item = items_service.get(item_num_id)
    if item is None:
        return
    
    item_id = item.item_id
    item_name = item.get_name(items_service.locale)
    
    # Busca ou cria loot
    loot = storage.loots.get_by_id(object_id)
    
    if loot is None:
        storage.loots.add(
            object_id=object_id,
            item_id=item_id,
            item_name=item_name,
            quantity=quantity
        )
    else:
        loot.item_id = item_id
        loot.item_name = item_name
        loot.quantity = quantity
