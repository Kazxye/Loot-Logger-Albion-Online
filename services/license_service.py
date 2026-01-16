"""
License Service - Open Source Version
Feito por Kazz

Este módulo foi simplificado para a versão open source.
Sistema de licença removido - software livre para uso.
"""

from dataclasses import dataclass
from typing import Optional

# Versão atual do software
CURRENT_VERSION = "1.0.0"


@dataclass
class LicenseInfo:
    """Informações da licença (mantido para compatibilidade)."""
    key: str = "OPEN-SOURCE"
    user: str = "Open Source User"
    expires: str = "Never"
    license_type: str = "open_source"
    days_remaining: int = -1
    hwid: str = ""


class LicenseService:
    """Serviço de licença simplificado para versão open source."""
    
    def __init__(self):
        self._license_info = LicenseInfo()
    
    @property
    def license_info(self) -> Optional[LicenseInfo]:
        return self._license_info
    
    @property
    def current_version(self) -> str:
        return CURRENT_VERSION
    
    def check_version(self):
        """Verifica versão (sempre retorna que está atualizado)."""
        return False, CURRENT_VERSION, CURRENT_VERSION


# Instância global
license_service = LicenseService()
