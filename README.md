# Loot Logger

Loot Logger para Albion Online. Captura e exibe em tempo real todos os itens coletados por jogadores, com suporte a filtros, exportação e notificações Discord.

## Requisitos

- Windows 10/11
- Python 3.10 ou superior
- Npcap (para captura de pacotes)
- Conexao com internet

## Instalação

### 1. Instalar Npcap

Baixe e instale o Npcap em: https://npcap.com/#download

Durante a instalação, marque a opção "Install Npcap in WinPcap API-compatible Mode".

### 2. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 3. Executar

```bash
python main_gui.py
```

## Dependências

- customtkinter - Interface gráfica moderna
- scapy - Captura de pacotes de rede
- requests - Requisições HTTP
- Pillow - Manipulação de imagens

## Estrutura do Projeto

```
ao-loot-logger/
├── main_gui.py          # Ponto de entrada da aplicação
├── main.py              # Versao CLI (sem interface)
├── requirements.txt     # Dependências
├── license.dat          # Licença ativada (gerado automaticamente)
├── core/                # Captura e parsing de pacotes
├── handlers/            # Processamento de eventos do jogo
├── services/            # Serviços (itens, discord, licencas)
├── storage/             # Armazenamento em memoria
├── models/              # Modelos de dados
├── gui/                 # Interface grafica
└── assets/              # Icones e imagens
```

## Funcionalidades

- Captura de loot em tempo real
- Filtro por tier (T4-T8)
- Filtro por jogador
- Filtro de itens raros
- Notificações Discord via webhook
- Exportação para JSON e CSV
- Suporte a idiomas (PT-BR / EN-US)
- Sistema de licenças com HWID

## Configuração

### Discord Webhook

1. Clique no botão de configurações (engrenagem)
2. Cole a URL do webhook do Discord
3. Ative a opção "Ativado"
4. Clique em "Testar" para verificar
5. Clique em "Salvar"

### Idioma

1. Clique no botão de configurações
2. Selecione o idioma desejado (PT-BR ou EN-US)
3. Clique em "Salvar"

