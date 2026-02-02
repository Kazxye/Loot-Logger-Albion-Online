<div align="center">

<img src="assets/banner.png" alt="Albion Online Loot Logger" width="100%" />

<br/>

![Version](https://img.shields.io/badge/version-3.3-e85a1b.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10+-3776ab.svg?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6.svg?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-22c55e.svg?style=for-the-badge)

**Captura e visualiza loots em tempo real com interface moderna e estimativa de preços**

<br/>

[📖 Sobre](#-sobre) •
[✨ Features](#-features) •
[🚀 Instalação](#-instalação) •
[💻 Uso](#-uso) •
[🔨 Build](#-gerando-executáveis) •
[📝 Changelog](#-changelog)

</div>

---

## 📖 Sobre

O **Loot Logger** é uma ferramenta open-source que captura pacotes de rede do Albion Online para registrar todos os loots em tempo real. Oferece duas interfaces completas:

- 🖥️ **GUI Desktop** - Interface moderna com CustomTkinter
- 🌐 **Dashboard Web** - Visualização em tempo real via WebSocket

> ⚠️ **Aviso Legal**: Esta ferramenta apenas lê pacotes de rede (modo passivo) e não modifica o jogo. Use por sua conta e risco.

---

## ✨ Features

### 🌐 Dashboard Web (v3.3)

| Feature | Descrição |
|---------|-----------|
| **Tempo Real** | Atualização instantânea via WebSocket |
| **2 Temas** | Royal Purple 💜 e Outlands Orange 🔥 |
| **Imagens dos Itens** | Carregadas da API oficial do Albion |
| **Estimativa de Silver** | Preços via Albion Data Project API |
| **Seletor de Servidor** | Americas, Europe, Asia |
| **Discord Webhook** | Notificações automáticas de itens raros |
| **Filtros Avançados** | Tier, categoria, jogador, busca, apenas raros |
| **Valor por Filtro** | Total recalcula ao filtrar |
| **Cores de Tier** | T4 🔵 T5 🔴 T6 🟠 T7 🟡 T8 ⚪ |
| **Cores de Encantamento** | .1 🟢 .2 🔵 .3 🟣 .4 🟡 |
| **Splash Inteligente** | Pula splash ao dar F5 |

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

## 🎨 Temas

O Dashboard possui 2 temas que podem ser alternados pelo botão na header:

### 💜 Royal Purple (Padrão)
- Roxo como cor primária
- Pretos frios com tom azulado
- Visual elegante e moderno

### 🔥 Outlands Orange
- Laranja vibrante como cor primária
- Pretos quentes com tom marrom
- Inspirado nas Outlands/Red Zones do Albion

A preferência é salva automaticamente no navegador.

---

## 🎨 Preview

### Cores dos Tiers (Filtros)

| Tier | Cor | Estilo |
|:----:|:---:|:------:|
| T4 | 🔵 Azul | Glass |
| T5 | 🔴 Vermelho | Glass |
| T6 | 🟠 Laranja | Glass |
| T7 | 🟡 Amarelo | Glass |
| T8 | ⚪ Branco | Glass |

### Cores na Tabela

Os itens na tabela mostram **duas informações de cor**:
- **Fundo**: Cor do tier base (T4 azul, T5 vermelho, etc)
- **Borda esquerda**: Cor do encantamento (.1 verde, .2 azul, .3 roxo, .4 dourado)

Exemplo: Um item **T4.3** terá fundo azul (T4) com borda roxa (.3)

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

## 🌎 Servidores de Preço

O Dashboard permite escolher o servidor para busca de preços:

| Servidor | Região | API |
|----------|--------|-----|
| **Americas** | Brasil, EUA, etc | `west.albion-online-data.com` |
| **Europe** | Europa | `europe.albion-online-data.com` |
| **Asia** | Ásia | `east.albion-online-data.com` |

A preferência é salva automaticamente no navegador.

---

## 💬 Discord Webhook

Configure notificações automáticas para o Discord:

1. Crie um webhook no seu servidor Discord (Configurações do Canal → Integrações → Webhooks)
2. No Dashboard, clique no ícone do Discord na header
3. Cole a URL do webhook
4. Clique em **Testar** para verificar
5. Clique em **Salvar**

**Itens enviados automaticamente:**
- Itens marcados como **raros**
- Itens com valor estimado **acima de 100k silver**

---

## 📁 Estrutura do Projeto

```
ao-loot-logger/
│
├── 📂 core/                    # Captura e parsing
│   ├── buffer_reader.py
│   ├── photon_decoder.py
│   ├── protocol16.py
│   └── sniffer.py
│
├── 📂 dashboard/               # Dashboard Web
│   ├── server.py               # Flask + SocketIO
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   ├── base.css        # Reset, variáveis
│       │   ├── splash.css      # Splash screen
│       │   ├── layout.css      # Header, sidebar
│       │   ├── table.css       # Tabela de loots
│       │   └── components.css  # Botões, modal, etc
│       └── js/
│           ├── app.js          # Alpine.js + lógica
│           └── splash.js       # Controller splash
│
├── 📂 gui/                     # Interface Desktop
│   ├── app.py
│   ├── themes.py
│   ├── splash_screen.py
│   └── components/
│
├── 📂 handlers/                # Event handlers
├── 📂 models/                  # Modelos de dados
├── 📂 services/                # Serviços
├── 📂 storage/                 # Armazenamento
├── 📂 assets/                  # Recursos
│
├── main.py                     # Entry CLI
├── main_gui.py                 # Entry GUI
├── main_web.py                 # Entry Web
├── build.py                    # Script de build
├── requirements.txt
└── README.md
```

---

## 🔨 Gerando Executáveis

### Método Fácil (Windows)
```bash
# Dê duplo clique em build.bat
```

### Via Python
```bash
# Instalar dependências
pip install -r requirements.txt

# Buildar Dashboard
python build.py web

# Buildar GUI
python build.py gui

# Buildar ambos
python build.py
```

Executáveis gerados em `release/`.

---

## 📦 Dependências

```txt
# Core
scapy>=2.5.0
requests>=2.31.0

# GUI
customtkinter>=5.2.0
pillow>=10.0.0

# Dashboard
flask>=3.0.0
flask-socketio>=5.3.0
python-socketio>=5.10.0

# Build
pyinstaller>=6.0.0
```

---

## 📝 Changelog

### v3.3 (Atual)
- ✅ Sistema de temas (Royal Purple e Outlands Orange)
- ✅ Botão de troca de tema na header
- ✅ Transições suaves entre temas
- ✅ Cores quentes no tema Outlands

### v3.2
- ✅ Seletor de servidor (Americas/Europe/Asia)
- ✅ Discord Webhook integrado no Dashboard
- ✅ Cores dos tiers nos filtros (T4 azul, T5 vermelho, etc)
- ✅ Cores na tabela: tier base + borda de encantamento
- ✅ Skip splash ao dar F5 (sessionStorage)
- ✅ Fix reatividade Alpine.js nos preços
- ✅ Preços atualizam em tempo real

### v3.1
- ✅ Ícone de silver melhorado
- ✅ Valor total recalcula com filtros
- ✅ Fix preços em tempo real

### v3.0
- ✅ Splash screen moderna
- ✅ Estimativa de valor em Silver
- ✅ Coluna "Valor" na tabela

### v2.0
- ✅ Dashboard Web com Flask + SocketIO
- ✅ Imagens dos itens via API oficial
- ✅ Filtros avançados
- ✅ Cores de encantamento

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
