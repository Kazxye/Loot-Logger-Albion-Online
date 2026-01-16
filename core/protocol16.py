"""
Protocol16 - Deserializador do protocolo de serialização Photon
Baseado no protocol16.js do projeto original
"""

from enum import IntEnum
from typing import Any, Dict, Optional, List, Union
from .buffer_reader import BufferReader


class DataType(IntEnum):
    """Tipos de dados do Protocol16."""
    NIL = 0x2A
    DICTIONARY = 0x44
    STRING_SLICE = 0x61
    INT8 = 0x62
    CUSTOM = 0x63
    DOUBLE = 0x64
    EVENT_DATE = 0x65
    FLOAT32 = 0x66
    HASHTABLE = 0x68
    INT32 = 0x69
    INT16 = 0x6B
    INT64 = 0x6C
    INT32_SLICE = 0x6E
    BOOLEAN = 0x6F
    OPERATION_RESPONSE = 0x70
    OPERATION_REQUEST = 0x71
    STRING = 0x73
    INT8_SLICE = 0x78
    SLICE = 0x79
    OBJECT_SLICE = 0x7A


class Protocol16:
    """Decodificador Protocol16 para mensagens Photon."""
    
    @staticmethod
    def decode_operation_request(reader: BufferReader) -> Dict[str, Any]:
        """Decodifica uma Operation Request."""
        operation_code = reader.read_uint8()
        parameters = Protocol16.decode_parameter_table(reader)
        
        return {
            'operation_code': operation_code,
            'parameters': parameters
        }
    
    @staticmethod
    def decode_operation_response(reader: BufferReader) -> Dict[str, Any]:
        """Decodifica uma Operation Response."""
        operation_code = reader.read_uint8()
        return_code = reader.read_uint16_be()
        
        param_type = reader.read_uint8()
        debug_message = Protocol16.read_param(param_type, reader)
        
        parameters = Protocol16.decode_parameter_table(reader)
        
        return {
            'operation_code': operation_code,
            'return_code': return_code,
            'debug_message': debug_message,
            'parameters': parameters
        }
    
    @staticmethod
    def decode_event_data(reader: BufferReader) -> Dict[str, Any]:
        """Decodifica um Event Data."""
        event_code = reader.read_uint8()
        parameters = Protocol16.decode_parameter_table(reader)
        
        return {
            'event_code': event_code,
            'parameters': parameters
        }
    
    @staticmethod
    def decode_parameter_table(reader: BufferReader) -> Dict[int, Any]:
        """Decodifica uma tabela de parâmetros."""
        parameters = {}
        
        parameters_count = reader.read_int16_be()
        
        for _ in range(parameters_count):
            param_id = reader.read_uint8()
            param_type = reader.read_uint8()
            parameters[param_id] = Protocol16.read_param(param_type, reader)
        
        return parameters
    
    @staticmethod
    def read_param(param_type: int, reader: BufferReader) -> Any:
        """Lê um parâmetro baseado no seu tipo."""
        
        # Nil / Unknown
        if param_type == 0 or param_type == DataType.NIL:
            return None
        
        # Int8
        if param_type == DataType.INT8:
            return reader.read_uint8()
        
        # Float32
        if param_type == DataType.FLOAT32:
            return reader.read_float_be()
        
        # Double
        if param_type == DataType.DOUBLE:
            return reader.read_double_be()
        
        # Int32
        if param_type == DataType.INT32:
            return reader.read_int32_be()
        
        # Int16 (também aceita type 7 por compatibilidade)
        if param_type == 7 or param_type == DataType.INT16:
            return reader.read_uint16_be()
        
        # Int64
        if param_type == DataType.INT64:
            return reader.read_int64_be()
        
        # String
        if param_type == DataType.STRING:
            length = reader.read_uint16_be()
            return reader.read_string(length)
        
        # Boolean
        if param_type == DataType.BOOLEAN:
            value = reader.read_uint8()
            if value == 0:
                return False
            elif value == 1:
                return True
            else:
                raise ValueError(f"Invalid boolean value: {value}")
        
        # Int8 Slice (byte array)
        if param_type == DataType.INT8_SLICE:
            size = reader.read_uint32_be()
            return list(reader.read_bytes(size))
        
        # Slice (array tipado)
        if param_type == DataType.SLICE:
            length = reader.read_uint16_be()
            slice_type = reader.read_uint8()
            return [Protocol16.read_param(slice_type, reader) for _ in range(length)]
        
        # Object Slice (array de objetos mistos)
        if param_type == DataType.OBJECT_SLICE:
            length = reader.read_uint16_be()
            result = []
            for _ in range(length):
                item_type = reader.read_uint8()
                result.append(Protocol16.read_param(item_type, reader))
            return result
        
        # Dictionary
        if param_type == DataType.DICTIONARY:
            key_type = reader.read_uint8()
            value_type = reader.read_uint8()
            length = reader.read_uint16_be()
            
            result = {}
            for _ in range(length):
                key = Protocol16.read_param(key_type, reader)
                value = Protocol16.read_param(value_type, reader)
                result[key] = value
            
            return result
        
        # Hashtable (similar ao dictionary mas com tipos por item)
        if param_type == DataType.HASHTABLE:
            length = reader.read_uint16_be()
            
            result = {}
            for _ in range(length):
                key_type = reader.read_uint8()
                key = Protocol16.read_param(key_type, reader)
                value_type = reader.read_uint8()
                value = Protocol16.read_param(value_type, reader)
                result[key] = value
            
            return result
        
        # Int32 Slice
        if param_type == DataType.INT32_SLICE:
            size = reader.read_uint32_be()
            return [reader.read_int32_be() for _ in range(size)]
        
        # String Slice
        if param_type == DataType.STRING_SLICE:
            length = reader.read_uint16_be()
            return [Protocol16.read_param(DataType.STRING, reader) for _ in range(length)]
        
        # Tipo desconhecido
        raise ValueError(f"Unknown param type: 0x{param_type:02X} at position {reader.position - 1}")
