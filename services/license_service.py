"""
License Service - Sistema de licencas via GitHub Gist (formato TXT)

Formato do arquivo:
CHAVE|USUARIO|HWID|EXPIRA|ATIVO
XXXX-XXXX-XXXX-XXXX|Cliente 1||2025-12-31|true
"""

import os
import hashlib
import requests
import subprocess
from datetime import datetime
from typing import Optional, Tuple, Set
from dataclasses import dataclass

# Importa URLs ofuscadas do modulo de seguranca
try:
    from security import get_gist_url, get_webhook_url
    LICENSES_URL = get_gist_url()
    ADMIN_WEBHOOK_URL = get_webhook_url()
except:
    # Fallback (nao deve acontecer em producao)
    LICENSES_URL = "https://gist.githubusercontent.com/Kazxye/64213a3a9612313569c7b9247319835a/raw/licenses.txt"
    ADMIN_WEBHOOK_URL = "https://discord.com/api/webhooks/1450885302687367212/lqPr2y7nTzzFtztU7lgxi2V6LNjj45NADMr6k_lowgv4bT548hsjQLbp_INW9rUk8PDD"

# Versao atual do software
CURRENT_VERSION = "1.0.0"

# Arquivo local para salvar a licenca ativada
LICENSE_FILE = "license.dat"

# Arquivo para rastrear se já notificou primeiro uso
FIRST_USE_FILE = "first_use.dat"


@dataclass
class LicenseInfo:
    """Informacoes da licenca."""
    key: str
    user: str
    expires: str
    license_type: str
    days_remaining: int
    hwid: str


class LicenseService:
    """Servico de gerenciamento de licencas."""
    
    def __init__(self):
        self._license_info: Optional[LicenseInfo] = None
        self._hwid: Optional[str] = None
        self._first_use_notified: Set[str] = set()
        self._load_first_use_cache()
    
    def _load_first_use_cache(self):
        """Carrega cache de chaves que já notificaram primeiro uso."""
        try:
            if os.path.exists(FIRST_USE_FILE):
                with open(FIRST_USE_FILE, 'r') as f:
                    for line in f:
                        key = line.strip()
                        if key:
                            self._first_use_notified.add(key)
        except:
            pass
    
    def _save_first_use(self, key: str):
        """Salva que já notificou primeiro uso para esta chave."""
        try:
            self._first_use_notified.add(key)
            with open(FIRST_USE_FILE, 'a') as f:
                f.write(key + "\n")
        except:
            pass
    
    def _was_first_use_notified(self, key: str) -> bool:
        """Verifica se já notificou primeiro uso para esta chave."""
        return key.upper() in self._first_use_notified
    
    def get_hwid(self) -> str:
        """Obtem o HWID da maquina."""
        if self._hwid:
            return self._hwid
        
        try:
            # Windows - usa WMIC para pegar o serial do disco
            if os.name == 'nt':
                result = subprocess.check_output(
                    'wmic diskdrive get serialnumber',
                    shell=True,
                    stderr=subprocess.DEVNULL
                ).decode()
                
                lines = [l.strip() for l in result.split('\n') if l.strip()]
                if len(lines) > 1:
                    serial = lines[1]
                else:
                    serial = "UNKNOWN"
            else:
                # Linux/Mac
                serial = subprocess.check_output(
                    ['cat', '/etc/machine-id'],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
        except:
            serial = "FALLBACK_ID"
        
        # Gera hash do serial
        self._hwid = hashlib.md5(serial.encode()).hexdigest().upper()
        return self._hwid
    
    def get_saved_license(self) -> Optional[str]:
        """Retorna licenca salva localmente."""
        try:
            if os.path.exists(LICENSE_FILE):
                with open(LICENSE_FILE, 'r') as f:
                    return f.read().strip()
        except:
            pass
        return None
    
    def save_license(self, key: str):
        """Salva licenca localmente."""
        try:
            with open(LICENSE_FILE, 'w') as f:
                f.write(key)
        except:
            pass
    
    def clear_license(self):
        """Remove licenca local."""
        try:
            if os.path.exists(LICENSE_FILE):
                os.remove(LICENSE_FILE)
        except:
            pass
    
    def _notify_admin(self, event_type: str, key: str, user: str, hwid: str, message: str = ""):
        """Envia notificacao para webhook do admin."""
        if not ADMIN_WEBHOOK_URL:
            return
        
        try:
            colors = {
                "new_hwid": 0x22C55E,      # Verde - novo HWID
                "login": 0x3B82F6,          # Azul - login normal
                "invalid_key": 0xEF4444,    # Vermelho - chave invalida
                "expired": 0xF59E0B,        # Amarelo - expirada
                "hwid_mismatch": 0xEF4444,  # Vermelho - HWID diferente
                "disabled": 0x6B7280,       # Cinza - desativada
            }
            
            titles = {
                "new_hwid": "Novo HWID - Primeiro Uso",
                "login": "Login Realizado",
                "invalid_key": "Tentativa de Chave Invalida",
                "expired": "Licenca Expirada",
                "hwid_mismatch": "HWID Nao Corresponde",
                "disabled": "Licenca Desativada",
            }
            
            embed = {
                "title": titles.get(event_type, "Evento"),
                "color": colors.get(event_type, 0x6B7280),
                "fields": [
                    {"name": "Chave", "value": f"`{key}`", "inline": True},
                    {"name": "Usuario", "value": user or "N/A", "inline": True},
                    {"name": "HWID", "value": f"`{hwid}`", "inline": False},
                ],
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {"text": "Loot Logger Admin"}
            }
            
            if message:
                embed["fields"].append({"name": "Info", "value": message, "inline": False})
            
            # Adiciona campo para copiar facil se for novo HWID
            if event_type == "new_hwid":
                linha_pronta = f"{key}|{user}|{hwid}|2025-12-31|true"
                embed["fields"].append({
                    "name": "Linha pronta para o Gist",
                    "value": f"```{linha_pronta}```",
                    "inline": False
                })
            
            payload = {"embeds": [embed]}
            requests.post(ADMIN_WEBHOOK_URL, json=payload, timeout=10)
            
        except:
            pass  # Falha silenciosa
    
    def fetch_licenses(self) -> Optional[dict]:
        """Busca licencas do servidor e converte para dict."""
        try:
            # Adiciona cache-busting para evitar cache do GitHub
            url = f"{LICENSES_URL}?t={datetime.now().timestamp()}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            text = response.text.strip()
            licenses = {}
            
            for line in text.split('\n'):
                line = line.strip()
                if not line or line.startswith('CHAVE'):
                    continue  # Pula cabecalho e linhas vazias
                
                parts = line.split('|')
                if len(parts) >= 5:
                    key = parts[0].strip().upper()
                    licenses[key] = {
                        'user': parts[1].strip(),
                        'hwid': parts[2].strip(),
                        'expires': parts[3].strip(),
                        'active': parts[4].strip().lower() == 'true'
                    }
            
            return {'licenses': licenses, 'version': CURRENT_VERSION}
            
        except Exception as e:
            print(f"[ERRO] Falha ao buscar licencas: {e}")
            return None
    
    def validate_license(self, key: str) -> Tuple[bool, str]:
        """
        Valida uma chave de licenca.
        
        Retorna: (sucesso, mensagem)
        """
        key = key.strip().upper()
        
        if not key:
            return False, "Chave de licenca nao informada."
        
        # Busca licencas online
        data = self.fetch_licenses()
        if data is None:
            return False, "Nao foi possivel conectar ao servidor.\nVerifique sua conexao."
        
        licenses = data.get("licenses", {})
        current_hwid = self.get_hwid()
        
        # Verifica se a chave existe
        if key not in licenses:
            self._notify_admin("invalid_key", key, "", current_hwid, "Chave nao encontrada")
            return False, "Chave de licenca invalida."
        
        license_data = licenses[key]
        user_name = license_data.get("user", "Usuario")
        
        # Verifica se esta ativa
        if not license_data.get("active", False):
            self._notify_admin("disabled", key, user_name, current_hwid)
            return False, "Esta licenca foi desativada.\nEntre em contato com o suporte."
        
        # Verifica expiracao
        expires_str = license_data.get("expires", "")
        if expires_str:
            try:
                expires_date = datetime.strptime(expires_str, "%Y-%m-%d")
                if datetime.now() > expires_date:
                    self._notify_admin("expired", key, user_name, current_hwid, f"Expirou em {expires_str}")
                    return False, f"Licenca expirada em {expires_str}.\nRenove sua licenca."
            except:
                pass
        
        # Verifica HWID
        stored_hwid = license_data.get("hwid", "")
        
        if stored_hwid and stored_hwid != current_hwid:
            self._notify_admin("hwid_mismatch", key, user_name, current_hwid, f"HWID esperado: {stored_hwid}")
            return False, "Esta licenca esta vinculada a outro computador.\nEntre em contato com o suporte."
        
        # Se HWID vazio, e primeiro uso - notifica admin apenas UMA VEZ
        if not stored_hwid:
            if not self._was_first_use_notified(key):
                print(f"[INFO] Primeiro uso detectado!")
                print(f"[INFO] HWID: {current_hwid}")
                self._notify_admin("new_hwid", key, user_name, current_hwid, "Primeiro uso - vincular HWID")
                self._save_first_use(key)
            else:
                # Já notificou antes, apenas faz login silencioso
                print(f"[INFO] Login com chave pendente de vinculacao HWID")
        else:
            # Login normal
            self._notify_admin("login", key, user_name, current_hwid)
        
        # Calcula dias restantes
        days_remaining = -1  # -1 = vitalicio
        if expires_str:
            try:
                expires_date = datetime.strptime(expires_str, "%Y-%m-%d")
                delta = expires_date - datetime.now()
                days_remaining = max(0, delta.days)
            except:
                pass
        
        # Salva informacoes
        self._license_info = LicenseInfo(
            key=key,
            user=license_data.get("user", "Usuario"),
            expires=expires_str if expires_str else "Vitalicio",
            license_type="standard",
            days_remaining=days_remaining,
            hwid=current_hwid
        )
        
        # Salva localmente
        self.save_license(key)
        
        return True, "Licenca valida!"
    
    def check_version(self) -> Tuple[bool, str, str]:
        """
        Verifica se ha atualizacao disponivel.
        
        Retorna: (tem_update, versao_atual, versao_nova)
        """
        # Por enquanto, versao e fixa no codigo
        # Pode ser expandido para ler do Gist se necessario
        return False, CURRENT_VERSION, CURRENT_VERSION
    
    @property
    def license_info(self) -> Optional[LicenseInfo]:
        return self._license_info
    
    @property
    def current_version(self) -> str:
        return CURRENT_VERSION


# Instancia global
license_service = LicenseService()
