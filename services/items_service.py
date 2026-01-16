"""
Items Service - Carrega e gerencia lista de itens do Albion
Baseado em items.js - usa items.json com fallback para items.txt
Suporta múltiplos idiomas (PT-BR, EN-US)
"""

import requests
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class Item:
    """Representa um item do Albion."""
    item_num_id: int        # Index numérico
    item_id: str            # UniqueName (ex: T8_2H_BOW_AVALON@1)
    names: Dict[str, str]   # Nomes por idioma {"PT-BR": "...", "EN-US": "..."}
    
    def get_name(self, locale: str = "PT-BR") -> str:
        """Retorna nome no idioma especificado."""
        return self.names.get(locale) or self.names.get("EN-US") or self.item_id


class ItemsService:
    """Serviço de gerenciamento de itens."""
    
    # URLs
    ITEMS_JSON_URL = "https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.json"
    ITEMS_TXT_URL = "https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.txt"
    
    # Idiomas suportados
    SUPPORTED_LOCALES = ["PT-BR", "EN-US"]
    
    def __init__(self):
        self.items: Dict[int, Item] = {}
        self._loaded = False
        self._current_locale = "PT-BR"
    
    @property
    def locale(self) -> str:
        return self._current_locale
    
    @locale.setter
    def locale(self, value: str):
        if value in self.SUPPORTED_LOCALES:
            self._current_locale = value
    
    def init(self) -> bool:
        """Inicializa carregando a lista de itens."""
        return self.load()
    
    def load(self) -> bool:
        """Carrega a lista de itens."""
        # Tenta JSON primeiro
        if self._load_json():
            return True
        
        # Fallback para TXT
        print("[INFO] Tentando fallback para items.txt...")
        return self._load_txt()
    
    def _load_json(self) -> bool:
        """Carrega itens do JSON."""
        try:
            print("[INFO] Carregando lista de itens...")
            response = requests.get(self.ITEMS_JSON_URL, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            for item_data in data:
                try:
                    # Index pode ser string ou int
                    index = item_data.get("Index")
                    if index is None:
                        continue
                    item_num_id = int(index)
                    
                    # UniqueName
                    item_id = item_data.get("UniqueName", "")
                    if not item_id:
                        continue
                    
                    # LocalizedNames - pega todos os idiomas
                    localized = item_data.get("LocalizedNames") or {}
                    names = {}
                    
                    for locale in self.SUPPORTED_LOCALES:
                        name = localized.get(locale, "")
                        if name:
                            names[locale] = name
                    
                    # Se não tem nenhum nome, usa item_id
                    if not names:
                        names["EN-US"] = item_id
                    
                    self.items[item_num_id] = Item(
                        item_num_id=item_num_id,
                        item_id=item_id,
                        names=names
                    )
                except:
                    continue
            
            self._loaded = True
            print(f"[INFO] {len(self.items)} itens carregados!")
            return True
            
        except Exception as e:
            print(f"[AVISO] Falha ao carregar JSON: {e}")
            return False
    
    def _load_txt(self) -> bool:
        """Carrega itens do TXT (formato: index:itemId:itemName)."""
        try:
            print("[INFO] Carregando lista de itens (TXT)...")
            response = requests.get(self.ITEMS_TXT_URL, timeout=60)
            response.raise_for_status()
            
            data = response.text
            
            for line in data.strip().split('\n'):
                try:
                    parts = line.split(':')
                    if len(parts) < 2:
                        continue
                    
                    item_num_id = int(parts[0].strip())
                    item_id = parts[1].strip()
                    item_name = parts[2].strip() if len(parts) > 2 else item_id
                    
                    self.items[item_num_id] = Item(
                        item_num_id=item_num_id,
                        item_id=item_id,
                        names={"EN-US": item_name, "PT-BR": item_name}
                    )
                except:
                    continue
            
            self._loaded = True
            print(f"[INFO] {len(self.items)} itens carregados!")
            return True
            
        except Exception as e:
            print(f"[ERRO] Falha ao carregar itens: {e}")
            return False
    
    def get(self, item_num_id: int) -> Optional[Item]:
        """Busca item pelo ID numérico."""
        return self.items.get(item_num_id)
    
    def get_name(self, item_num_id: int, locale: str = None) -> str:
        """Retorna nome do item no idioma atual."""
        item = self.get(item_num_id)
        if item:
            return item.get_name(locale or self._current_locale)
        return f"Unknown ({item_num_id})"


# Instância global
items_service = ItemsService()
