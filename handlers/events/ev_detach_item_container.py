"""
EvDetachItemContainer - Evento quando um container é desanexado (fecha)
Baseado em ev-detach-item-container.js
"""

from storage import storage
from utils import uuid_stringify


def handle(event: dict):
    """
    Processa evento EvDetachItemContainer.
    
    Parâmetros:
    - [0] = encodedUuid (array de 16 bytes)
    """
    params = event.get('parameters', {})
    
    encoded_uuid = params.get(0)
    if not isinstance(encoded_uuid, list) or len(encoded_uuid) != 16:
        return
    
    uuid = uuid_stringify(encoded_uuid)
    storage.containers.delete_by_uuid(uuid)
