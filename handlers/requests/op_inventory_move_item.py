"""
OpInventoryMoveItem - Request quando você move um item de container
Usado para detectar loot que VOCÊ pega
Baseado em op-inventory-move-item.js
"""

from datetime import datetime
from typing import Optional, Callable

from storage import storage
from utils import uuid_stringify


def handle(event: dict, on_loot: Optional[Callable] = None):
    """
    Processa request OpInventoryMoveItem.
    
    Parâmetros:
    - [0] = fromSlot (int)
    - [1] = fromEncodedUuid (array de 16 bytes)
    - [3] = toSlot (int)
    - [4] = toEncodedUuid (array de 16 bytes)
    """
    params = event.get('parameters', {})
    
    from_slot = params.get(0, 0)
    if not isinstance(from_slot, int):
        from_slot = 0
    
    from_encoded_uuid = params.get(1)
    if not isinstance(from_encoded_uuid, list) or len(from_encoded_uuid) != 16:
        return
    
    to_slot = params.get(3, 0)
    if not isinstance(to_slot, int):
        to_slot = 0
    
    to_encoded_uuid = params.get(4)
    if not isinstance(to_encoded_uuid, list) or len(to_encoded_uuid) != 16:
        return
    
    from_uuid = uuid_stringify(from_encoded_uuid)
    to_uuid = uuid_stringify(to_encoded_uuid)
    
    # Se movendo dentro do mesmo container, ignora
    if from_uuid == to_uuid:
        return
    
    # Busca container de origem
    container = storage.containers.get_by_uuid(from_uuid)
    if container is None:
        return
    
    # Não loga de chests
    if container.type == "chest":
        return
    
    # Busca o loot no slot
    loot = container.items.get(from_slot)
    if loot is None:
        return
    
    # Remove do storage
    storage.loots.delete_by_id(loot.object_id)
    del container.items[from_slot]
    
    # Se não tem owner, usa o owner do container
    if not loot.owner and container.owner:
        loot.owner = container.owner
    
    if not loot.owner:
        return
    
    # Verifica se temos o self player
    self_player = storage.players.self_player
    if self_player is None:
        print("[AVISO] Jogador não identificado ainda. Pulando evento de loot próprio.")
        return
    
    # Busca ou cria o jogador de quem veio o loot
    looted_from = storage.players.get_by_name(loot.owner)
    if looted_from is None:
        looted_from = storage.players.add(loot.owner)
    
    print(f"[LOOT] {self_player.format_name()} pegou {loot.quantity}x {loot.item_name} de {looted_from.format_name()}")
    
    # Callback para GUI/Discord
    if on_loot:
        from models import LootEvent
        loot_event = LootEvent(
            timestamp=datetime.utcnow(),
            item_id=loot.item_id,
            item_name=loot.item_name,
            quantity=loot.quantity,
            looted_by=self_player,
            looted_from=looted_from
        )
        on_loot(loot_event)
