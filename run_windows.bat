@echo off
echo ========================================
echo    SOF-IA - Deep Agents con Gemini
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo [1/5] Verificando Python... OK

REM Crear directorio del entorno virtual si no existe
if not exist "venv" (
    echo [2/5] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
) else (
    echo [2/5] Entorno virtual ya existe... OK
)

REM Activar entorno virtual
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Instalar dependencias
echo [4/5] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Verifica que requirements.txt existe y es válido
    pause
    exit /b 1
)

REM Verificar variables de entorno
echo [5/5] Verificando configuración...
if not defined GEMINI_API_KEY (
    if not defined GOOGLE_API_KEY (
        echo.
        echo WARNING: No se encontró GEMINI_API_KEY ni GOOGLE_API_KEY
        echo Por favor configura tu API key de Gemini:
        echo   set GEMINI_API_KEY=tu_api_key_aqui
        echo.
        echo O crea un archivo .env con:
        echo   GEMINI_API_KEY=tu_api_key_aqui
        echo   TAVILY_API_KEY=tu_api_key_aqui
        echo.
    )
)

if not defined TAVILY_API_KEY (
    echo WARNING: No se encontró TAVILY_API_KEY
    echo La búsqueda en internet no funcionará sin esta clave
    echo.
)

echo.
echo ========================================
echo Iniciando SOF-IA...
echo Abriendo en: http://localhost:8501
echo Presiona Ctrl+C para detener
echo ========================================
echo.

REM Ejecutar la aplicación
streamlit run streamlit_app.py --server.port 8501 --server.headless true

REM Si llegamos aquí, la aplicación se cerró
echo.
echo La aplicación se ha cerrado.
pause
