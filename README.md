<div align="center">

# 🎮 Albion Online Loot Logger

**Captura e visualiza loots em tempo real com interface moderna e estimativa de preços**

![Version](https://img.shields.io/badge/version-3.1-a855f7.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10+-3776ab.svg?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6.svg?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-22c55e.svg?style=for-the-badge)

<br/>

[📖 Sobre](#-sobre) •
[✨ Features](#-features) •
[🚀 Instalação](#-instalação) •
[💻 Uso](#-uso) •
[🔨 Build](#-gerando-executáveis) •
[📝 Changelog](#-changelog)

<br/>

<img src="https://render.albiononline.com/v1/item/T8_BAG@3.png?size=80" alt="Albion Item" />

</div>

---

## 📖 Sobre

O **Loot Logger** é uma ferramenta open-source que captura pacotes de rede do Albion Online para registrar todos os loots em tempo real. Oferece duas interfaces completas:

- 🖥️ **GUI Desktop** - Interface moderna com CustomTkinter
- 🌐 **Dashboard Web** - Visualização em tempo real via WebSocket

> ⚠️ **Aviso Legal**: Esta ferramenta apenas lê pacotes de rede (modo passivo) e não modifica o jogo. Use por sua conta e risco.

---

## ✨ Features

### 🌐 Dashboard Web (v3.1)

| Feature | Descrição |
|---------|-----------|
| **Tempo Real** | Atualização instantânea via WebSocket |
| **Imagens dos Itens** | Carregadas da API oficial do Albion |
| **Estimativa de Silver** | Preços via Albion Data Project API |
| **Filtros Avançados** | Tier, categoria, jogador, busca, apenas raros |
| **Valor por Filtro** | Total recalcula ao filtrar (ex: valor por jogador) |
| **Cores de Encantamento** | .1 🟢 .2 🔵 .3 🟣 .4 🟡 |
| **Splash Screen** | Animação moderna com partículas e progress bar |
| **Tooltips** | Preview ampliado do item ao passar o mouse |
| **Odômetro** | Animação nos contadores de estatísticas |
| **Hover Effects** | Efeitos visuais modernos na interface |

### 🖥️ GUI Desktop

| Feature | Descrição |
|---------|-----------|
| **Interface Moderna** | CustomTkinter com tema escuro |
| **Tabela de Loots** | Visualização organizada com filtros |
| **Discord Webhook** | Notificações automáticas no Discord |
| **Filtros de Tier** | T4 até T8 selecionáveis |
| **Exportação** | JSON e CSV |
| **Multi-idioma** | PT-BR e EN-US |

### 📊 Dados Capturados

```
┌─────────────────────────────────────────────────────────┐
│  📦 Item          │ Elder's Bag                         │
│  🆔 ID            │ T8_BAG@3                            │
│  📊 Quantidade    │ 1                                   │
│  ⚔️ Tier          │ T8.3 (Roxo)                         │
│  💰 Valor Est.    │ 2.5M Silver                         │
│  👤 Pegou         │ PlayerName [GuildTag]               │
│  🎯 Origem        │ MobName / ChestType / PlayerKilled  │
│  🕐 Horário       │ 14:32:15                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Preview

### Cores de Encantamento

| Encantamento | Cor | Hex | Exemplo |
|:------------:|:---:|:---:|:-------:|
| .0 (base) | ⚪ Cinza | `#94a3b8` | T6 |
| .1 | 🟢 Verde | `#22c55e` | T6.1 |
| .2 | 🔵 Azul | `#3b82f6` | T6.2 |
| .3 | 🟣 Roxo | `#a855f7` | T6.3 |
| .4 | 🟡 Dourado | `#eab308` | T6.4 |

### Ícone de Silver

O dashboard utiliza um ícone de moeda detalhado com:
- Gradiente dourado
- Letra "S" central
- Borda destacada

---

## 📋 Requisitos

### Sistema
- **Windows 10/11**
- **Python 3.10+**
- **Npcap** (driver de captura)

### Instalação do Npcap

1. Baixe em: https://npcap.com/#download
2. Durante instalação, marque: **"Install Npcap in WinPcap API-compatible Mode"**
3. Reinicie o computador

---

## 🚀 Instalação

### Opção 1: Executável (Recomendado)

Baixe o `.exe` pronto na [página de Releases](../../releases).

### Opção 2: Código Fonte

```bash
# Clone o repositório
git clone https://github.com/Kazxye/ao-loot-logger.git
cd ao-loot-logger

# Crie ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

---

## 💻 Uso

> ⚠️ **Importante**: Execute sempre como **Administrador** (necessário para captura de pacotes)

### Dashboard Web

```bash
python main_web.py
```

O navegador abrirá automaticamente em `http://localhost:5000`

### GUI Desktop

```bash
python main_gui.py
```

### Modos Disponíveis

| Arquivo | Interface | Executável |
|---------|-----------|------------|
| `main_web.py` | Dashboard Web | `LootLogger-Dashboard.exe` |
| `main_gui.py` | GUI Desktop | `LootLogger-GUI.exe` |
| `main.py` | CLI (terminal) | - |

---

## 💰 API de Preços (Silver)

O Dashboard utiliza a **Albion Data Project API** para estimar valores.

### Endpoint
```
https://west.albion-online-data.com/api/v2/stats/prices/{item_id}.json
```

### Cidades Consultadas
Caerleon, Bridgewatch, Martlock, Thetford, Fort Sterling, Lymhurst

### Cache
- TTL de 5 minutos para evitar rate limits
- Preços são média de venda das cidades

### Limitações
- Preços são **estimativas** baseadas no mercado
- Alguns itens podem não ter preço disponível
- Dados dependem de jogadores rodando o Albion Data Client

---

## 🖼️ API de Imagens

Imagens carregadas da **API oficial do Albion**:

```
https://render.albiononline.com/v1/item/{ITEM_ID}.png?size={SIZE}
```

| Parâmetro | Descrição | Valores |
|-----------|-----------|---------|
| `ITEM_ID` | ID do item | Ex: `T8_BAG@3` |
| `size` | Tamanho em px | 1-217 |
| `quality` | Qualidade | 1-5 |

---

## 📁 Estrutura do Projeto

```
ao-loot-logger/
│
├── 📂 core/                    # Captura e parsing
│   ├── buffer_reader.py        # Leitor de buffer binário
│   ├── photon_decoder.py       # Decoder protocolo Photon
│   ├── protocol16.py           # Implementação Protocol16
│   └── sniffer.py              # Captura de pacotes
│
├── 📂 dashboard/               # Dashboard Web
│   ├── server.py               # Flask + SocketIO
│   ├── templates/
│   │   └── index.html          # Template principal
│   └── static/                 # Assets estáticos
│
├── 📂 gui/                     # Interface Desktop
│   ├── app.py                  # App principal
│   ├── themes.py               # Temas e cores
│   ├── splash_screen.py        # Splash screen
│   └── components/             # Componentes UI
│       ├── filter_panel.py
│       ├── header.py
│       ├── loot_table.py
│       ├── settings_modal.py
│       └── status_bar.py
│
├── 📂 handlers/                # Event handlers
│   ├── data_handler.py         # Handler principal
│   ├── events/                 # Eventos do jogo
│   ├── requests/               # Requisições
│   └── responses/              # Respostas
│
├── 📂 models/                  # Modelos de dados
│   ├── container.py
│   ├── loot_event.py
│   └── player.py
│
├── 📂 services/                # Serviços
│   ├── config_service.py       # Configurações
│   ├── discord_service.py      # Discord webhook
│   ├── items_service.py        # Serviço de itens
│   └── tier_service.py         # Tiers e raridade
│
├── 📂 storage/                 # Armazenamento
│   ├── containers_storage.py
│   ├── loots_storage.py
│   ├── memory_storage.py
│   └── players_storage.py
│
├── 📂 assets/                  # Recursos
│   ├── icon.ico
│   └── logo.png
│
├── main.py                     # Entry CLI
├── main_gui.py                 # Entry GUI
├── main_web.py                 # Entry Web
├── build.py                    # Script de build
├── build.bat                   # Build Windows
├── requirements.txt            # Dependências
└── README.md                   # Documentação
```

---

## 🔨 Gerando Executáveis

### Método Fácil (Windows)
```bash
# Dê duplo clique em build.bat
```

### Via Python
```bash
# Buildar ambos
python build.py

# Ou individualmente
python build.py gui   # LootLogger-GUI.exe
python build.py web   # LootLogger-Dashboard.exe
```

### Manualmente (PyInstaller)

```bash
# Dashboard
pyinstaller --name=LootLogger-Dashboard --onefile --console ^
    --icon=assets/icon.ico ^
    --add-data "dashboard;dashboard" ^
    --add-data "core;core" ^
    --hidden-import=flask --hidden-import=flask_socketio ^
    --hidden-import=scapy.all main_web.py

# GUI
pyinstaller --name=LootLogger-GUI --onefile --windowed ^
    --icon=assets/icon.ico ^
    --add-data "gui;gui" ^
    --add-data "core;core" ^
    --hidden-import=customtkinter ^
    --hidden-import=scapy.all main_gui.py
```

Executáveis gerados em `dist/` e copiados para `release/`.

---

## ⚙️ Configuração

### Discord Webhook

1. Crie um webhook no Discord (Configurações do Canal → Integrações)
2. Na GUI: Configurações → Discord → Cole a URL
3. Configure tier mínimo para notificações
4. Teste e salve

### Arquivo de Config

Localização: `%APPDATA%/LootLogger/config.json`

```json
{
  "discord_webhook": "https://discord.com/api/webhooks/...",
  "min_tier": 6,
  "notify_rare_only": false,
  "language": "pt-br"
}
```

---

## 📦 Dependências

```txt
# Core
scapy>=2.5.0              # Captura de pacotes
requests>=2.31.0          # HTTP requests

# GUI
customtkinter>=5.2.0      # Interface moderna
pillow>=10.0.0            # Manipulação de imagens

# Dashboard
flask>=3.0.0              # Servidor web
flask-socketio>=5.3.0     # WebSocket
python-socketio>=5.10.0   # Cliente SocketIO

# Build
pyinstaller>=6.0.0        # Geração de .exe
```

---

## 📝 Changelog

### v3.1 (Atual)
- ✅ Ícone de silver melhorado (moeda detalhada com gradiente)
- ✅ Valor total recalcula com filtros ativos
- ✅ Fix: Preços atualizam em tempo real (sem precisar F5)
- ✅ Animação de loading ("...") enquanto busca preço

### v3.0
- ✅ Splash screen moderna com animações (grid, partículas, orbs)
- ✅ Estimativa de valor em Silver via Albion Data Project
- ✅ Coluna "Valor" na tabela
- ✅ Stat card "Valor Estimado" da sessão
- ✅ Progress bar animada no splash

### v2.3
- ✅ Imagens dos itens via API oficial do Albion
- ✅ Tooltips com preview ampliado
- ✅ Odômetro animado nos stats
- ✅ Efeitos de hover modernos

### v2.2
- ✅ Cores de encantamento (.1 verde, .2 azul, .3 roxo, .4 dourado)
- ✅ Splash screen inicial
- ✅ Remoção de emojis das categorias

### v2.0
- ✅ Dashboard Web com Flask + SocketIO
- ✅ Sidebar com filtros avançados
- ✅ Timer de sessão
- ✅ Destaque para itens raros
- ✅ Sistema de build para .exe

### v1.0
- ✅ GUI Desktop com CustomTkinter
- ✅ Captura de loots em tempo real
- ✅ Discord Webhook
- ✅ Filtros básicos

---

## 🛠️ Tecnologias

<div align="center">

| Backend | Frontend | Tools |
|:-------:|:--------:|:-----:|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | ![TailwindCSS](https://img.shields.io/badge/Tailwind-38B2AC?style=flat&logo=tailwind-css&logoColor=white) | ![PyInstaller](https://img.shields.io/badge/PyInstaller-FFCD00?style=flat&logo=python&logoColor=black) |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) | ![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0?style=flat&logo=alpine.js&logoColor=black) | ![Scapy](https://img.shields.io/badge/Scapy-2C2D72?style=flat&logo=wireshark&logoColor=white) |
| ![SocketIO](https://img.shields.io/badge/Socket.io-010101?style=flat&logo=socket.io&logoColor=white) | ![Lucide](https://img.shields.io/badge/Lucide-F56565?style=flat&logo=feather&logoColor=white) | ![Npcap](https://img.shields.io/badge/Npcap-00599C?style=flat&logo=wireshark&logoColor=white) |

</div>

---

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 🙏 Créditos

- **Albion Data Project** - API de preços de mercado
- **Albion Online** - API oficial de imagens
- Baseado no projeto [ao-loot-logger](https://github.com/matheussampaio/ao-loot-logger)

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja [LICENSE](LICENSE) para detalhes.

---

<div align="center">

## 👨‍💻 Autor

Desenvolvido com 💜 por **Kazz**

[![GitHub](https://img.shields.io/badge/GitHub-Kazxye-181717?style=for-the-badge&logo=github)](https://github.com/Kazxye)

<br/>

**⭐ Se este projeto te ajudou, considere dar uma estrela!**

<br/>

<sub>Made for the Albion Online community</sub>

</div>
