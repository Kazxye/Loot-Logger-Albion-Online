"""
EvAttachItemContainer - Evento quando um container é anexado (abre)
Baseado em ev-attach-item-container.js
"""

from storage import storage
from utils import uuid_stringify


def handle(event: dict):
    """
    Processa evento EvAttachItemContainer.
    
    Parâmetros:
    - [0] = id (int)
    - [1] = encodedUuid (array de 16 bytes)
    - [3] = inventory (array de objectIds)
    - [4] = slots (int)
    """
    params = event.get('parameters', {})
    
    container_id = params.get(0)
    if not isinstance(container_id, int):
        return
    
    encoded_uuid = params.get(1)
    if not isinstance(encoded_uuid, list) or len(encoded_uuid) != 16:
        return
    
    inventory = params.get(3)
    if not isinstance(inventory, list):
        return
    
    slots = params.get(4)
    if not isinstance(slots, int):
        return
    
    uuid = uuid_stringify(encoded_uuid)
    
    # Busca container por UUID ou ID
    container = storage.containers.get_by_uuid(uuid)
    if container is None:
        container = storage.containers.get_by_id(container_id)
    
    if container is None:
        container = storage.containers.add(id=container_id, uuid=uuid)
    else:
        if container.uuid != uuid:
            container.uuid = uuid
        if container.id != container_id:
            container.id = container_id
    
    # Associa items ao container
    for position, object_id in enumerate(inventory):
        if not isinstance(object_id, int) or object_id == 0:
            continue
        
        loot = storage.loots.get_by_id(object_id)
        if loot is None:
            continue
        
        if not loot.owner and container.owner:
            loot.owner = container.owner
        
        container.items[position] = loot
