"""
Security Module - Protecoes contra engenharia reversa
Feito por Kazz
"""

import os
import sys
import ctypes
import hashlib
import threading
import time
from base64 import b64decode, b64encode

# ============================================
# OFUSCACAO DE STRINGS
# ============================================

def _d(s: str) -> str:
    """Decodifica string ofuscada."""
    try:
        return b64decode(s.encode()).decode()
    except:
        return s

def _e(s: str) -> str:
    """Codifica string (usar para preparar)."""
    return b64encode(s.encode()).decode()


# URLs ofuscadas (base64)
_GIST_URL = "aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9LYXp4eWUvNjQyMTNhM2E5NjEyMzEzNTY5YzdiOTI0NzMxOTgzNWEvcmF3L2xpY2Vuc2VzLnR4dA=="
_WEBHOOK_URL = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ1MDg4NTMwMjY4NzM2NzIxMi9scVByMnk3blR6ekZ0enRVN2xneGkyVjZMTmpqNDVOQURNcjZrX2xvd2d2NGJUNTQ4aHNqUUxicF9JTlc5clVrOFBERA=="


def get_gist_url() -> str:
    """Retorna URL do Gist."""
    return _d(_GIST_URL)


def get_webhook_url() -> str:
    """Retorna URL do Webhook."""
    return _d(_WEBHOOK_URL)


# ============================================
# ANTI-DEBUG (Windows)
# ============================================

def is_debugger_present() -> bool:
    """Verifica se um debugger esta anexado."""
    if sys.platform != 'win32':
        return False
    
    try:
        # Metodo 1: IsDebuggerPresent
        kernel32 = ctypes.windll.kernel32
        if kernel32.IsDebuggerPresent():
            return True
        
        # Metodo 2: CheckRemoteDebuggerPresent
        is_debugged = ctypes.c_bool(False)
        kernel32.CheckRemoteDebuggerPresent(
            kernel32.GetCurrentProcess(),
            ctypes.byref(is_debugged)
        )
        if is_debugged.value:
            return True
        
        # Metodo 3: NtGlobalFlag (PEB)
        # Valor 0x70 indica debugging
        
    except:
        pass
    
    return False


def check_vm_environment() -> bool:
    """Verifica se esta rodando em VM (opcional - pode dar falso positivo)."""
    vm_indicators = [
        "VBOX", "VMWARE", "VIRTUAL", "QEMU", "XEN"
    ]
    
    try:
        # Verifica nome do computador
        computer_name = os.environ.get("COMPUTERNAME", "").upper()
        for indicator in vm_indicators:
            if indicator in computer_name:
                return True
        
        # Verifica fabricante via WMI (Windows)
        if sys.platform == 'win32':
            import subprocess
            result = subprocess.run(
                ['wmic', 'computersystem', 'get', 'manufacturer'],
                capture_output=True, text=True, timeout=5
            )
            output = result.stdout.upper()
            for indicator in vm_indicators:
                if indicator in output:
                    return True
    except:
        pass
    
    return False


def check_analysis_tools() -> bool:
    """Verifica se ferramentas de analise estao rodando."""
    suspicious_processes = [
        "ollydbg", "x64dbg", "x32dbg", "ida", "ida64",
        "wireshark", "fiddler", "charles", "processhacker",
        "procmon", "procexp", "dnspy", "dotpeek", "ilspy",
        "cheatengine", "cheat engine"
    ]
    
    try:
        if sys.platform == 'win32':
            import subprocess
            result = subprocess.run(
                ['tasklist'], capture_output=True, text=True, timeout=10
            )
            output = result.stdout.lower()
            
            for proc in suspicious_processes:
                if proc in output:
                    return True
    except:
        pass
    
    return False


# ============================================
# VERIFICACAO DE INTEGRIDADE
# ============================================

_EXPECTED_FILES = {
    "main_gui.py": None,  # Hash sera calculado na primeira execucao
    "services/license_service.py": None,
}


def calculate_file_hash(filepath: str) -> str:
    """Calcula hash SHA256 de um arquivo."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except:
        return ""


def verify_integrity() -> bool:
    """Verifica integridade dos arquivos principais."""
    # Em producao, comparar com hashes conhecidos
    # Por enquanto, apenas verifica se arquivos existem
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    critical_files = [
        "main_gui.py",
        "services/license_service.py",
        "gui/app.py"
    ]
    
    for file in critical_files:
        full_path = os.path.join(base_path, file)
        if not os.path.exists(full_path):
            return False
    
    return True


# ============================================
# MONITORAMENTO EM BACKGROUND
# ============================================

class SecurityMonitor:
    """Monitor de seguranca em background."""
    
    def __init__(self):
        self._running = False
        self._thread = None
        self._violation_callback = None
    
    def start(self, on_violation=None):
        """Inicia monitoramento."""
        self._violation_callback = on_violation
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Para monitoramento."""
        self._running = False
    
    def _monitor_loop(self):
        """Loop de monitoramento."""
        check_count = 0
        
        while self._running:
            try:
                # Verifica a cada 30 segundos
                time.sleep(30)
                check_count += 1
                
                # Verifica debugger
                if is_debugger_present():
                    self._on_violation("debugger_detected")
                    break
                
                # Verifica ferramentas de analise (a cada 2 minutos)
                if check_count % 4 == 0:
                    if check_analysis_tools():
                        self._on_violation("analysis_tool_detected")
                        break
                
            except:
                pass
    
    def _on_violation(self, reason: str):
        """Chamado quando detecta violacao."""
        if self._violation_callback:
            self._violation_callback(reason)


# ============================================
# FUNCAO PRINCIPAL DE VERIFICACAO
# ============================================

def run_security_checks() -> tuple:
    """
    Executa todas as verificacoes de seguranca.
    
    Retorna: (passou: bool, motivo: str)
    """
    # 1. Verifica debugger
    if is_debugger_present():
        return False, "debugger"
    
    # 2. Verifica ferramentas de analise
    if check_analysis_tools():
        return False, "analysis_tools"
    
    # 3. Verifica integridade (opcional)
    # if not verify_integrity():
    #     return False, "integrity"
    
    return True, "ok"


def get_security_monitor() -> SecurityMonitor:
    """Retorna instancia do monitor de seguranca."""
    return SecurityMonitor()


# ============================================
# PROTECAO DE MEMORIA (Avancado)
# ============================================

def protect_memory():
    """Tenta proteger memoria do processo (Windows)."""
    if sys.platform != 'win32':
        return
    
    try:
        # Desabilita Windows Error Reporting para o processo
        kernel32 = ctypes.windll.kernel32
        kernel32.SetErrorMode(0x8003)  # SEM_NOGPFAULTERRORBOX | SEM_FAILCRITICALERRORS | SEM_NOOPENFILEERRORBOX
    except:
        pass
