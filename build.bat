@echo off
chcp 65001 >nul
title Loot Logger - Build Script

echo.
echo ══════════════════════════════════════════════════════════════
echo              Loot Logger - Build Script
echo                       by Kazz
echo ══════════════════════════════════════════════════════════════
echo.

:: Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado! Instale Python 3.10+
    pause
    exit /b 1
)

:: Instala dependências se necessário
echo [INFO] Verificando dependências...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando PyInstaller...
    pip install pyinstaller
)

:: Menu
echo.
echo Escolha o que buildar:
echo.
echo   [1] Ambos (GUI + Dashboard)
echo   [2] Apenas GUI (LootLogger-GUI.exe)
echo   [3] Apenas Dashboard (LootLogger-Dashboard.exe)
echo   [4] Sair
echo.
set /p choice="Opção: "

if "%choice%"=="1" goto build_all
if "%choice%"=="2" goto build_gui
if "%choice%"=="3" goto build_web
if "%choice%"=="4" goto end

:build_all
python build.py all
goto done

:build_gui
python build.py gui
goto done

:build_web
python build.py web
goto done

:done
echo.
echo ══════════════════════════════════════════════════════════════
echo  Build finalizado! Verifique a pasta 'release'
echo ══════════════════════════════════════════════════════════════
echo.
pause
goto end

:end
