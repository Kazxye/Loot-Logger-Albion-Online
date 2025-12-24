"""
Buffer Reader - Leitor de bytes com suporte a Big Endian
Baseado no buffer-reader.js do projeto original
"""

import struct
from typing import Optional


class BufferReader:
    """Leitor de buffer binário com métodos para leitura Big Endian."""
    
    def __init__(self, data: bytes):
        self.buffer = data
        self.position = 0
    
    @property
    def length(self) -> int:
        return len(self.buffer)
    
    @property
    def remaining(self) -> int:
        return self.length - self.position
    
    def _check_bounds(self, size: int):
        if self.position < 0 or self.position + size > self.length:
            raise BufferError(f"Out of bounds read: position={self.position}, size={size}, length={self.length}")
    
    def read_int8(self) -> int:
        """Lê 1 byte como signed int."""
        self._check_bounds(1)
        value = struct.unpack_from('>b', self.buffer, self.position)[0]
        self.position += 1
        return value
    
    def read_uint8(self) -> int:
        """Lê 1 byte como unsigned int."""
        self._check_bounds(1)
        value = struct.unpack_from('>B', self.buffer, self.position)[0]
        self.position += 1
        return value
    
    def read_int16_be(self) -> int:
        """Lê 2 bytes como signed int Big Endian."""
        self._check_bounds(2)
        value = struct.unpack_from('>h', self.buffer, self.position)[0]
        self.position += 2
        return value
    
    def read_uint16_be(self) -> int:
        """Lê 2 bytes como unsigned int Big Endian."""
        self._check_bounds(2)
        value = struct.unpack_from('>H', self.buffer, self.position)[0]
        self.position += 2
        return value
    
    def read_int32_be(self) -> int:
        """Lê 4 bytes como signed int Big Endian."""
        self._check_bounds(4)
        value = struct.unpack_from('>i', self.buffer, self.position)[0]
        self.position += 4
        return value
    
    def read_uint32_be(self) -> int:
        """Lê 4 bytes como unsigned int Big Endian."""
        self._check_bounds(4)
        value = struct.unpack_from('>I', self.buffer, self.position)[0]
        self.position += 4
        return value
    
    def read_int64_be(self) -> int:
        """Lê 8 bytes como signed int Big Endian."""
        self._check_bounds(8)
        value = struct.unpack_from('>q', self.buffer, self.position)[0]
        self.position += 8
        return value
    
    def read_float_be(self) -> float:
        """Lê 4 bytes como float Big Endian."""
        self._check_bounds(4)
        value = struct.unpack_from('>f', self.buffer, self.position)[0]
        self.position += 4
        return value
    
    def read_double_be(self) -> float:
        """Lê 8 bytes como double Big Endian."""
        self._check_bounds(8)
        value = struct.unpack_from('>d', self.buffer, self.position)[0]
        self.position += 8
        return value
    
    def read_bytes(self, length: Optional[int] = None) -> bytes:
        """Lê N bytes do buffer."""
        if length is None:
            length = self.remaining
        
        self._check_bounds(length)
        data = self.buffer[self.position:self.position + length]
        self.position += length
        return data
    
    def read_string(self, length: int) -> str:
        """Lê N bytes e converte para string UTF-8."""
        data = self.read_bytes(length)
        return data.decode('utf-8', errors='replace')
    
    def skip(self, length: int):
        """Pula N bytes."""
        self._check_bounds(length)
        self.position += length
    
    def slice(self, end: Optional[int] = None) -> bytes:
        """Retorna slice do buffer da posição atual até end."""
        if end is None:
            end = self.length
        return self.buffer[self.position:end]
