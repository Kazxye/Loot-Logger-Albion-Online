"""
Sniffer - Captura de pacotes UDP do Albion Online
Baseado no albion-network.js do projeto original
"""

import threading
import time
from typing import Callable, Optional
from scapy.all import sniff, UDP, IP, conf

from .photon_decoder import PhotonDecoder


# Portas do Albion Online
ALBION_PORTS = [5056, 5055, 4535]

# Tempo máximo sem pacotes para considerar offline (segundos)
MAX_SECONDS_BETWEEN_PACKETS = 5


class AlbionSniffer:
    """Sniffer de pacotes UDP do Albion Online."""
    
    def __init__(self):
        self.decoder = PhotonDecoder()
        self.running = False
        self.is_online = False
        self.last_packet_time: Optional[float] = None
        
        self._sniff_thread: Optional[threading.Thread] = None
        self._monitor_thread: Optional[threading.Thread] = None
        
        # Callbacks
        self._on_online: Optional[Callable[[], None]] = None
        self._on_offline: Optional[Callable[[], None]] = None
    
    def on_event(self, callback: Callable[[dict], None]):
        """Registra callback para eventos Photon."""
        self.decoder.on_event(callback)
    
    def on_request(self, callback: Callable[[dict], None]):
        """Registra callback para requests Photon."""
        self.decoder.on_request(callback)
    
    def on_response(self, callback: Callable[[dict], None]):
        """Registra callback para responses Photon."""
        self.decoder.on_response(callback)
    
    def on_online(self, callback: Callable[[], None]):
        """Registra callback para quando Albion é detectado."""
        self._on_online = callback
    
    def on_offline(self, callback: Callable[[], None]):
        """Registra callback para quando Albion não é mais detectado."""
        self._on_offline = callback
    
    def start(self):
        """Inicia a captura de pacotes."""
        if self.running:
            return
        
        self.running = True
        self.is_online = False
        self.last_packet_time = None
        
        # Thread de captura
        self._sniff_thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self._sniff_thread.start()
        
        # Thread de monitoramento
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Para a captura de pacotes."""
        self.running = False
        
        if self._sniff_thread:
            self._sniff_thread.join(timeout=2)
        
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)
    
    def _sniff_loop(self):
        """Loop de captura de pacotes."""
        # Filtro BPF para UDP nas portas do Albion
        port_filter = " or ".join([f"port {p}" for p in ALBION_PORTS])
        bpf_filter = f"udp and ({port_filter})"
        
        try:
            # Desabilita verbose do scapy
            conf.verb = 0
            
            sniff(
                filter=bpf_filter,
                prn=self._handle_packet,
                store=False,
                stop_filter=lambda x: not self.running
            )
        except Exception as e:
            print(f"[ERRO] Falha na captura: {e}")
            print("[DICA] Execute como administrador/root")
    
    def _handle_packet(self, packet):
        """Processa um pacote capturado."""
        try:
            if UDP in packet and packet[UDP].payload:
                # Extrai payload UDP
                payload = bytes(packet[UDP].payload)
                
                # Atualiza tempo do último pacote
                self.last_packet_time = time.time()
                
                # Verifica se ficou online
                if not self.is_online:
                    self.is_online = True
                    if self._on_online:
                        self._on_online()
                
                # Processa pacote Photon
                self.decoder.handle_packet(payload)
        
        except Exception as e:
            # Ignora erros de pacotes malformados
            pass
    
    def _monitor_loop(self):
        """Loop de monitoramento de status online/offline."""
        while self.running:
            time.sleep(1)
            
            if self.last_packet_time is None:
                continue
            
            elapsed = time.time() - self.last_packet_time
            
            if elapsed > MAX_SECONDS_BETWEEN_PACKETS:
                if self.is_online:
                    self.is_online = False
                    if self._on_offline:
                        self._on_offline()
