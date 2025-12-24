@echo off
REM ============================================
REM Build Script para AO Loot Logger
REM Usa Nuitka para compilar Python para C
REM Feito por Kazz
REM ============================================

echo.
echo ========================================
echo   AO Loot Logger - Build Script
echo   Compilando com Nuitka...
echo ========================================
echo.

REM Verifica se Nuitka esta instalado
python -m nuitka --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Nuitka nao encontrado!
    echo.
    echo Instale com: pip install nuitka
    echo.
    pause
    exit /b 1
)

REM Verifica se tem compilador C
where cl >nul 2>&1
if errorlevel 1 (
    where gcc >nul 2>&1
    if errorlevel 1 (
        echo [AVISO] Compilador C nao encontrado no PATH.
        echo Nuitka vai tentar usar MinGW64 automaticamente.
        echo.
    )
)

echo [INFO] Iniciando compilacao...
echo [INFO] Isso pode demorar varios minutos...
echo.

REM Comando Nuitka com todas as opcoes
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=attach ^
    --windows-icon-from-ico=assets/icon.ico ^
    --company-name="Kazz" ^
    --product-name="Loot Logger" ^
    --file-version=1.0.0 ^
    --product-version=1.0.0 ^
    --file-description="Albion Online Loot Logger" ^
    --copyright="2024 Kazz" ^
    --enable-plugin=tk-inter ^
    --include-data-dir=assets=assets ^
    --include-package=customtkinter ^
    --include-package=scapy ^
    --include-package=PIL ^
    --include-module=security ^
    --nofollow-import-to=tkinter.test ^
    --nofollow-import-to=unittest ^
    --nofollow-import-to=pytest ^
    --remove-output ^
    --assume-yes-for-downloads ^
    --output-filename=LootLogger.exe ^
    main_gui.py

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na compilacao!
    echo Verifique os erros acima.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Compilacao concluida com sucesso!
echo ========================================
echo.
echo O arquivo LootLogger.exe foi criado.
echo.

pause
