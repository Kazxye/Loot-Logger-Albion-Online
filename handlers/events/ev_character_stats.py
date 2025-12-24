"""
EvCharacterStats - Evento de estatísticas do personagem
Baseado em ev-characters-stats.js
"""

from storage import storage


def handle(event: dict):
    """
    Processa evento EvCharacterStats.
    
    Parâmetros:
    - [0] = id (int)
    - [2] = guildName (string, opcional)
    - [4] = allianceName (string, opcional)
    - [5] = playerName (string)
    """
    params = event.get('parameters', {})
    
    player_id = params.get(0)
    if not isinstance(player_id, int):
        return
    
    player_name = params.get(5)
    if not isinstance(player_name, str):
        return
    
    guild_name = params.get(2, "")
    alliance_name = params.get(4, "")
    
    if not isinstance(guild_name, str):
        guild_name = ""
    if not isinstance(alliance_name, str):
        alliance_name = ""
    
    # Busca ou cria jogador
    player = storage.players.get_by_name(player_name)
    
    if player is None:
        player = storage.players.add(player_name, guild_name, alliance_name)
    else:
        if guild_name:
            player.guild = guild_name
        if alliance_name:
            player.alliance = alliance_name
