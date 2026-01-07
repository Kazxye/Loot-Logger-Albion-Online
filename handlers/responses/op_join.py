"""
OpJoin - Response quando você entra no jogo
Identifica o próprio jogador (self)
Baseado em op-join.js
"""

from storage import storage


def handle(event: dict):
    """
    Processa response OpJoin.
    
    Parâmetros:
    - [2] = playerName (string)
    - [57] = guildName (string, opcional)
    - [77] = allianceName (string, opcional)
    """
    params = event.get('parameters', {})
    
    player_name = params.get(2)
    if not isinstance(player_name, str):
        return
    
    guild_name = params.get(57, "")
    alliance_name = params.get(77, "")
    
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
    
    # Define como o próprio jogador (SELF)
    storage.players.set_self(player)
    print(f"[INFO] Jogador identificado: {player.format_name()}")
