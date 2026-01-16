"""
EvNewCharacter - Evento quando um novo personagem aparece
Baseado em ev-new-character.js
"""

from storage import storage


def handle(event: dict):
    """
    Processa evento EvNewCharacter.
    
    Parâmetros:
    - [0] = id (int)
    - [1] = playerName (string)
    - [8] = guildName (string, opcional)
    - [43] = allianceName (string, opcional)
    """
    params = event.get('parameters', {})
    
    player_id = params.get(0)
    if not isinstance(player_id, int):
        return
    
    player_name = params.get(1)
    if not isinstance(player_name, str):
        return
    
    guild_name = params.get(8, "")
    alliance_name = params.get(43, "")
    
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
    
    # Debug (comentado para não poluir)
    # print(f"[DEBUG] EvNewCharacter: {player.format_name()}")
