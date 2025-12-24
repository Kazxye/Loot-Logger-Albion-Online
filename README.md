# Loot Logger

Loot Logger para Albion Online. Captura e exibe em tempo real todos os itens coletados por jogadores, com suporte a filtros, exportacao e notificacoes Discord.

## Requisitos

- Windows 10/11
- Python 3.10 ou superior
- Npcap (para captura de pacotes)
- Conexao com internet

## Instalacao

### 1. Instalar Npcap

Baixe e instale o Npcap em: https://npcap.com/#download

Durante a instalacao, marque a opcao "Install Npcap in WinPcap API-compatible Mode".

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Executar

```bash
python main_gui.py
```

## Dependencias

- customtkinter - Interface grafica moderna
- scapy - Captura de pacotes de rede
- requests - Requisicoes HTTP
- Pillow - Manipulacao de imagens

## Estrutura do Projeto

```
ao-loot-logger/
├── main_gui.py          # Ponto de entrada da aplicacao
├── main.py              # Versao CLI (sem interface)
├── requirements.txt     # Dependencias
├── license.dat          # Licenca ativada (gerado automaticamente)
├── core/                # Captura e parsing de pacotes
├── handlers/            # Processamento de eventos do jogo
├── services/            # Servicos (itens, discord, licencas)
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
- Notificacoes Discord via webhook
- Exportacao para JSON e CSV
- Suporte a idiomas (PT-BR / EN-US)
- Sistema de licencas com HWID

## Configuracao

### Discord Webhook

1. Clique no botao de configuracoes (engrenagem)
2. Cole a URL do webhook do Discord
3. Ative a opcao "Ativado"
4. Clique em "Testar" para verificar
5. Clique em "Salvar"

### Idioma

1. Clique no botao de configuracoes
2. Selecione o idioma desejado (PT-BR ou EN-US)
3. Clique em "Salvar"

## Licenca

Este software requer uma licenca valida para funcionamento. Entre em contato com o desenvolvedor para adquirir uma licenca.

## Suporte

Para suporte tecnico ou aquisicao de licencas, entre em contato com o desenvolvedor.

## Autor

Desenvolvido por Kazz
