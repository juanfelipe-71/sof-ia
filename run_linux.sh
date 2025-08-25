#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e "   SOF-IA - Deep Agents con Gemini"
echo -e "========================================"
echo -e "${NC}"

# Función para mostrar errores
show_error() {
    echo -e "${RED}ERROR: $1${NC}"
    exit 1
}

# Función para mostrar warnings
show_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

# Función para mostrar éxito
show_success() {
    echo -e "${GREEN}$1${NC}"
}

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        show_error "Python no está instalado. Por favor instala Python 3.8+ usando: sudo apt install python3 python3-pip python3-venv"
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo -e "[1/5] Verificando Python... ${GREEN}OK${NC}"

# Verificar versión de Python
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Versión de Python: $PYTHON_VERSION"

# Crear directorio del entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "[2/5] Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        show_error "No se pudo crear el entorno virtual. Instala python3-venv: sudo apt install python3-venv"
    fi
else
    echo -e "[2/5] Entorno virtual ya existe... ${GREEN}OK${NC}"
fi

# Activar entorno virtual
echo "[3/5] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    show_error "No se pudo activar el entorno virtual"
fi

# Instalar dependencias
echo "[4/5] Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    show_error "No se pudieron instalar las dependencias. Verifica que requirements.txt existe y es válido"
fi

# Verificar variables de entorno
echo "[5/5] Verificando configuración..."

# Cargar .env si existe
if [ -f ".env" ]; then
    echo "Cargando variables de entorno desde .env..."
    export $(cat .env | grep -v '^#' | xargs)
fi

if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo ""
    show_warning "No se encontró GEMINI_API_KEY ni GOOGLE_API_KEY"
    echo "Por favor configura tu API key de Gemini:"
    echo "  export GEMINI_API_KEY=tu_api_key_aqui"
    echo ""
    echo "O crea un archivo .env con:"
    echo "  GEMINI_API_KEY=tu_api_key_aqui"
    echo "  TAVILY_API_KEY=tu_api_key_aqui"
    echo ""
fi

if [ -z "$TAVILY_API_KEY" ]; then
    show_warning "No se encontró TAVILY_API_KEY"
    echo "La búsqueda en internet no funcionará sin esta clave"
    echo ""
fi

echo ""
echo -e "${BLUE}========================================"
echo "Iniciando SOF-IA..."
echo "Abriendo en: http://localhost:8501"
echo "Presiona Ctrl+C para detener"
echo -e "========================================${NC}"
echo ""

# Ejecutar la aplicación
streamlit run streamlit_app.py --server.port 8501 --server.headless true

# Si llegamos aquí, la aplicación se cerró
echo ""
echo "La aplicación se ha cerrado."
