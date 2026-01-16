"""
EvNewLoot - Evento quando um loot bag aparece no chão
Baseado em ev-new-loot.js
"""

from storage import storage


def handle(event: dict):
    """
    Processa evento EvNewLoot.
    
    Parâmetros:
    - [0] = id (int) - ID do container
    - [3] = owner (string) - nome do dono
    - [4] = position (array) - posição [x, y]
    """
    params = event.get('parameters', {})
    
    container_id = params.get(0)
    if not isinstance(container_id, int):
        return
    
    owner = params.get(3)
    if not isinstance(owner, str):
        return
    
    # Verifica position (opcional mas ajuda debug)
    position = params.get(4)
    if not isinstance(position, list) or len(position) != 2:
        pass  # Não é crítico
    
    # Tipo baseado no owner
    container_type = "monster" if owner.startswith("@MOB") else "player"
    
    # Busca ou cria container
    container = storage.containers.get_by_id(container_id)
    
    if container is None:
        container = storage.containers.add(
            id=container_id,
            owner=owner,
            type=container_type
        )
    else:
        if container.owner != owner:
            container.owner = owner
        if container.type != container_type:
            container.type = container_type
