# 🎮 Loot Logger

**Loot Logger para Albion Online** - Captura e exibe em tempo real todos os itens coletados por jogadores, com suporte a filtros, exportação e notificações Discord.

> 🆓 **Versão Open Source** - Software livre para uso pessoal e educacional.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Funcionalidades

- 📡 Captura de loot em tempo real
- 🎯 Filtro por tier (T4-T8)
- 👥 Filtro por jogador
- ⭐ Filtro de itens raros
- 📱 Notificações Discord via webhook
- 💾 Exportação para JSON e CSV
- 🌐 Suporte a idiomas (PT-BR / EN-US)

## 📋 Requisitos

- Windows 10/11
- Python 3.10 ou superior
- [Npcap](https://npcap.com/#download) (para captura de pacotes)

## 🚀 Instalação

### 1. Instalar Npcap

Baixe e instale o Npcap em: https://npcap.com/#download

> ⚠️ Durante a instalação, marque a opção **"Install Npcap in WinPcap API-compatible Mode"**.

### 2. Clonar repositório

```bash
git clone https://github.com/Kazxye/ao-loot-logger.git
cd ao-loot-logger
```

### 3. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 4. Executar

```bash
python main_gui.py
```

> ⚠️ **Importante:** Execute como Administrador para permitir a captura de pacotes de rede.

## 📦 Dependências

| Pacote | Descrição |
|--------|-----------|
| customtkinter | Interface gráfica moderna |
| scapy | Captura de pacotes de rede |
| requests | Requisições HTTP |
| Pillow | Manipulação de imagens |

## 📁 Estrutura do Projeto

```
ao-loot-logger/
├── main_gui.py          # Ponto de entrada da aplicação
├── main.py              # Versão CLI (sem interface)
├── requirements.txt     # Dependências
├── core/                # Captura e parsing de pacotes
├── handlers/            # Processamento de eventos do jogo
├── services/            # Serviços (itens, discord, config)
├── storage/             # Armazenamento em memória
├── models/              # Modelos de dados
├── gui/                 # Interface gráfica
└── assets/              # Ícones e imagens
```

## ⚙️ Configuração

### Discord Webhook

1. Clique no botão de configurações (⚙️)
2. Cole a URL do webhook do Discord
3. Ative a opção "Ativado"
4. Clique em "Testar" para verificar
5. Clique em "Salvar"

### Idioma

1. Clique no botão de configurações
2. Selecione o idioma desejado (PT-BR ou EN-US)
3. Clique em "Salvar"

## 🙏 Créditos

- Baseado no projeto [ao-loot-logger](https://github.com/matheussampaio/ao-loot-logger) de matheussampaio
- Interface e melhorias por Kazz

## 📄 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido com ❤️ por **Kazz**

- GitHub: [@Kazxye](https://github.com/Kazxye)
