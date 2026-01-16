"""
Photon Decoder - Parser do protocolo de rede Photon
Baseado no photon-parser.js do projeto original
"""

from enum import IntEnum
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from .buffer_reader import BufferReader
from .protocol16 import Protocol16


class CommandType(IntEnum):
    """Tipos de comando Photon."""
    ACKNOWLEDGE = 0x01
    CONNECT = 0x02
    VERIFY_CONNECT = 0x03
    DISCONNECT = 0x04
    PING = 0x05
    SEND_RELIABLE = 0x06
    SEND_UNRELIABLE = 0x07
    SEND_RELIABLE_FRAGMENT = 0x08


class MessageType(IntEnum):
    """Tipos de mensagem Photon."""
    OPERATION_REQUEST = 0x02
    OPERATION_RESPONSE = 0x03
    EVENT_DATA = 0x04
    INTERNAL_OPERATION_REQUEST = 0x06
    INTERNAL_OPERATION_RESPONSE = 0x07


# Constantes de tamanho de header
PHOTON_HEADER_LENGTH = 12
PHOTON_COMMAND_HEADER_LENGTH = 12
PHOTON_FRAGMENT_HEADER_LENGTH = 20


@dataclass
class FragmentedPacket:
    """Representa um pacote fragmentado sendo reassemblado."""
    bytes_written: int = 0
    total_length: int = 0
    payload: bytearray = field(default_factory=bytearray)


class PhotonDecoder:
    """Decodificador de pacotes Photon."""
    
    def __init__(self):
        self.pending_fragments: Dict[int, FragmentedPacket] = {}
        
        # Callbacks para eventos
        self._on_event: Optional[Callable[[Dict], None]] = None
        self._on_request: Optional[Callable[[Dict], None]] = None
        self._on_response: Optional[Callable[[Dict], None]] = None
    
    def on_event(self, callback: Callable[[Dict], None]):
        """Registra callback para eventos."""
        self._on_event = callback
    
    def on_request(self, callback: Callable[[Dict], None]):
        """Registra callback para requests."""
        self._on_request = callback
    
    def on_response(self, callback: Callable[[Dict], None]):
        """Registra callback para responses."""
        self._on_response = callback
    
    def handle_packet(self, data: bytes) -> None:
        """Processa um pacote Photon completo."""
        if len(data) < PHOTON_HEADER_LENGTH:
            return
        
        reader = BufferReader(data)
        
        # Lê header Photon
        peer_id = reader.read_uint16_be()
        flags = reader.read_uint8()
        command_count = reader.read_uint8()
        timestamp = reader.read_uint32_be()
        challenge = reader.read_int32_be()
        
        # Verifica flags
        is_encrypted = flags == 1
        is_crc_enabled = flags == 0xCC
        
        # Pacotes encriptados não são suportados
        if is_encrypted:
            return
        
        # Pacotes com CRC - pular por enquanto (como o original)
        if is_crc_enabled:
            # TODO: Implementar validação CRC se necessário
            return
        
        # Processa cada comando
        for _ in range(command_count):
            if reader.position >= reader.length:
                break
            
            # Lê header do comando
            command_type = reader.read_uint8()
            channel_id = reader.read_uint8()
            command_flags = reader.read_uint8()
            reserved_byte = reader.read_uint8()
            command_length = reader.read_int32_be()
            sequence_number = reader.read_int32_be()
            
            # Ajusta tamanho do payload (remove header)
            payload_length = command_length - PHOTON_COMMAND_HEADER_LENGTH
            
            if payload_length < 0:
                continue
            
            # Processa baseado no tipo de comando
            if command_type == CommandType.DISCONNECT:
                return
            
            elif command_type == CommandType.SEND_UNRELIABLE:
                # SEND_UNRELIABLE tem 4 bytes extras no header
                reader.skip(4)
                payload_length -= 4
                if payload_length > 0:
                    payload = reader.read_bytes(payload_length)
                    self._handle_reliable(payload)
            
            elif command_type == CommandType.SEND_RELIABLE:
                payload = reader.read_bytes(payload_length)
                self._handle_reliable(payload)
            
            elif command_type == CommandType.SEND_RELIABLE_FRAGMENT:
                payload = reader.read_bytes(payload_length)
                self._handle_fragment(payload, payload_length, sequence_number)
            
            else:
                # Pula comandos desconhecidos
                if payload_length > 0:
                    reader.skip(payload_length)
    
    def _handle_fragment(self, data: bytes, fragment_length: int, seq_number: int) -> None:
        """Processa um fragmento de pacote."""
        reader = BufferReader(data)
        
        sequence_number = reader.read_int32_be()
        fragment_count = reader.read_int32_be()
        fragment_number = reader.read_int32_be()
        total_length = reader.read_int32_be()
        fragment_offset = reader.read_int32_be()
        
        # Ajusta tamanho do fragmento
        fragment_data_length = fragment_length - PHOTON_FRAGMENT_HEADER_LENGTH
        
        # Cria entrada se não existe
        if sequence_number not in self.pending_fragments:
            self.pending_fragments[sequence_number] = FragmentedPacket(
                bytes_written=0,
                total_length=total_length,
                payload=bytearray(total_length)
            )
        
        fragment_packet = self.pending_fragments[sequence_number]
        
        # Copia fragmento para a posição correta
        fragment_data = reader.read_bytes(fragment_data_length)
        fragment_packet.payload[fragment_offset:fragment_offset + fragment_data_length] = fragment_data
        fragment_packet.bytes_written += fragment_data_length
        
        # Verifica se pacote está completo
        if fragment_packet.bytes_written >= fragment_packet.total_length:
            del self.pending_fragments[sequence_number]
            self._handle_reliable(bytes(fragment_packet.payload))
    
    def _handle_reliable(self, data: bytes) -> None:
        """Processa dados confiáveis (reliable)."""
        if len(data) < 2:
            return
        
        reader = BufferReader(data)
        
        flag = reader.read_uint8()
        
        # Verifica flag válido (243 = 0xF3, 253 = 0xFD)
        if flag != 243 and flag != 253:
            return
        
        message_type = reader.read_uint8()
        
        # Mensagens encriptadas não são suportadas
        is_encrypted = message_type > 128
        if is_encrypted:
            return
        
        try:
            if message_type == MessageType.OPERATION_REQUEST:
                request_data = Protocol16.decode_operation_request(reader)
                if self._on_request:
                    self._on_request(request_data)
            
            elif message_type == MessageType.OPERATION_RESPONSE:
                response_data = Protocol16.decode_operation_response(reader)
                if self._on_response:
                    self._on_response(response_data)
            
            elif message_type == MessageType.EVENT_DATA:
                event_data = Protocol16.decode_event_data(reader)
                if self._on_event:
                    self._on_event(event_data)
            
            elif message_type == MessageType.INTERNAL_OPERATION_REQUEST:
                request_data = Protocol16.decode_operation_request(reader)
                if self._on_request:
                    self._on_request(request_data)
            
            elif message_type == MessageType.INTERNAL_OPERATION_RESPONSE:
                response_data = Protocol16.decode_operation_response(reader)
                if self._on_response:
                    self._on_response(response_data)
        
        except Exception as e:
            # Silenciosamente ignora erros de parsing (como o original)
            pass
