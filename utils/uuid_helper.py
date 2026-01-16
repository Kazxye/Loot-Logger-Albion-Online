"""UUID Helper - converte array de bytes para UUID string."""

from typing import List


def uuid_stringify(arr: List[int], offset: int = 0) -> str:
    """
    Converte array de 16 bytes para formato UUID string.
    Formato: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    """
    if len(arr) < offset + 16:
        raise ValueError("Array deve ter pelo menos 16 bytes")
    
    hex_bytes = [f"{arr[offset + i]:02x}" for i in range(16)]
    
    uuid = (
        "".join(hex_bytes[0:4]) + "-" +
        "".join(hex_bytes[4:6]) + "-" +
        "".join(hex_bytes[6:8]) + "-" +
        "".join(hex_bytes[8:10]) + "-" +
        "".join(hex_bytes[10:16])
    )
    
    return uuid.lower()
