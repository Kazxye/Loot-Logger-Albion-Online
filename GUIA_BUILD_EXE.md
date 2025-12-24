# 📦 Guia Completo - Gerando o Executável (.exe)

## 📋 Pré-requisitos

### 1. Python 3.10+ instalado
Verifique com:
```cmd
python --version
```

### 2. Instalar Nuitka
```cmd
pip install nuitka
```

### 3. Instalar dependências do projeto
```cmd
pip install customtkinter scapy requests pillow
```

### 4. Compilador C (Escolha UMA opção)

#### Opção A: MinGW64 (Recomendado - Mais fácil)
O Nuitka baixa automaticamente se não encontrar compilador.

#### Opção B: Visual Studio Build Tools
1. Baixe: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Instale selecionando "Desenvolvimento para desktop com C++"

---

## 🚀 Gerando o Executável

### Método 1: Script Automático (Recomendado)

1. Abra o **Prompt de Comando como Administrador**

2. Navegue até a pasta do projeto:
```cmd
cd C:\caminho\para\ao-loot-logger
```

3. Execute o script de build:
```cmd
build.bat
```

4. Aguarde (pode demorar 5-15 minutos na primeira vez)

5. O arquivo `LootLogger.exe` será criado na pasta

---

### Método 2: Comando Manual

Se o script não funcionar, use diretamente:

```cmd
python -m nuitka --standalone --onefile --windows-console-mode=attach --windows-icon-from-ico=assets/icon.ico --enable-plugin=tk-inter --include-data-dir=assets=assets --assume-yes-for-downloads --output-filename=LootLogger.exe main_gui.py
```

---

### Método 3: Build Simples

Se ainda tiver problemas:
```cmd
build_simple.bat
```

---

## ⚠️ Problemas Comuns

### Erro: "Nuitka não encontrado"
```cmd
pip install nuitka --upgrade
```

### Erro: "No C compiler found"
O Nuitka vai perguntar se pode baixar MinGW64. Digite `yes`.

### Erro: "ModuleNotFoundError"
Instale o módulo que falta:
```cmd
pip install nome_do_modulo
```

### Antivírus bloqueia o .exe
- Adicione exceção no antivírus para a pasta do projeto
- Ou desative temporariamente durante o build

### Build muito lento
- Normal na primeira vez (baixa compilador)
- Builds seguintes são mais rápidos

---

## 📁 Estrutura Final

Após o build, você terá:
```
ao-loot-logger/
├── LootLogger.exe      ← Executável final
├── main_gui.py
├── build.bat
├── assets/
│   ├── icon.ico
│   └── logo.png
└── ... outros arquivos
```

---

## 🔒 Proteções Incluídas

O executável gerado inclui:

| Proteção | Descrição |
|----------|-----------|
| ✅ Código compilado para C | Não é bytecode Python |
| ✅ URLs ofuscadas | Gist e Webhook em base64 |
| ✅ Anti-debug | Detecta debuggers |
| ✅ Anti-análise | Detecta ferramentas como x64dbg, IDA |
| ✅ Monitor em background | Verifica ambiente a cada 30s |
| ✅ Sistema de licenças | HWID + validação online |

---

## 📤 Distribuindo

### O que enviar para clientes:
1. `LootLogger.exe` - O executável
2. Instruções de uso (precisa de Npcap instalado)

### O que NÃO enviar:
- Código fonte (.py)
- Scripts de build
- Arquivos de configuração sensíveis

---

## 🔧 Atualizando a Versão

1. Edite `services/license_service.py`:
```python
CURRENT_VERSION = "1.1.0"  # Nova versão
```

2. Edite `build.bat` (opcional):
```batch
--file-version=1.1.0
--product-version=1.1.0
```

3. Execute `build.bat` novamente

---

## ✅ Checklist Antes de Distribuir

- [ ] Testou o .exe em máquina limpa?
- [ ] Webhook do Discord está funcionando?
- [ ] Licenças estão configuradas no Gist?
- [ ] Npcap está instalado na máquina de teste?
- [ ] Executou como Administrador?

---

## 📞 Suporte

Se tiver problemas durante o build, verifique:
1. Python está no PATH do sistema
2. Todas as dependências estão instaladas
3. Está executando como Administrador
4. Antivírus não está bloqueando

---

**Feito por Kazz** 🎮
