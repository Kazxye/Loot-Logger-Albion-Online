@echo off
REM ============================================
REM Build Script SIMPLES para AO Loot Logger
REM Use este se o build.bat der problemas
REM ============================================

echo.
echo ========================================
echo   AO Loot Logger - Build Simples
echo ========================================
echo.

echo [INFO] Compilando com Nuitka (modo simples)...
echo [INFO] Isso pode demorar 5-15 minutos...
echo.

python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=attach ^
    --windows-icon-from-ico=assets/icon.ico ^
    --enable-plugin=tk-inter ^
    --include-data-dir=assets=assets ^
    --assume-yes-for-downloads ^
    --output-filename=LootLogger.exe ^
    main_gui.py

echo.
if exist LootLogger.exe (
    echo [OK] LootLogger.exe criado com sucesso!
) else (
    echo [ERRO] Falha ao criar executavel.
)
echo.

pause
