# 🚀 Guía de Instalación - SOF-IA

## Requisitos del Sistema

### Hardware Mínimo

- **CPU**: 2 núcleos (4+ recomendado)
- **RAM**: 4GB mínimo (8GB+ recomendado)
- **Almacenamiento**: 2GB de espacio libre
- **Red**: Conexión a internet estable

### Software Requerido

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 11, Linux Ubuntu, o macOS

## 📦 Instalación Automática

### Opción 1: Scripts Automáticos (Recomendado)

#### Windows 11

```cmd
# Clona el repositorio
git clone https://github.com/Cesde-Suroeste/Sof-ia.git
cd Sof-ia

# Ejecuta el instalador automático
run_windows.bat
```

#### Linux Ubuntu

```bash
# Clona el repositorio
git clone https://github.com/Cesde-Suroeste/Sof-ia.git
cd Sof-ia

# Ejecuta el instalador automático
./run_linux.sh
```

### Opción 2: Instalación Manual

#### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/Cesde-Suroeste/Sof-ia.git
cd Sof-ia
```

#### Paso 2: Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

#### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Paso 4: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
nano .env  # o usa tu editor preferido
```

## 🔐 Configuración de Seguridad

### Generar Master Key para Encriptación

SOF-IA utiliza encriptación AES-256 para proteger tus API keys. Para generar una master key segura:

```bash
python scripts/encrypt_keys.py
```

Esto generará:

- Una master key única
- Instrucciones para encriptar tus API keys
- Archivo de configuración seguro

### Configurar API Keys

#### Opción A: API Keys Encriptadas (Recomendado para Producción)

```bash
# Después de ejecutar encrypt_keys.py, configura:
SOFIA_MASTER_KEY=tu_master_key_generada
GEMINI_API_KEY_ENCRYPTED=tu_clave_encriptada
TAVILY_API_KEY_ENCRYPTED=tu_clave_encriptada
```

#### Opción B: API Keys Planas (Solo para Desarrollo)

```bash
# Solo para desarrollo local
GEMINI_API_KEY=tu_api_key_directa
TAVILY_API_KEY=tu_api_key_directa
```

### Obtener API Keys Requeridas

#### 1. Gemini API Key

1. Visita [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la clave generada

#### 2. Tavily API Key

1. Regístrate en [Tavily](https://tavily.com/)
2. Obtén tu API key gratuita
3. Copia la clave desde tu dashboard

## 🏃‍♂️ Ejecución de la Aplicación

### Modo Desarrollo

```bash
# Con variables de entorno
streamlit run streamlit_app.py --server.port 8501 --server.headless true

# O usando el script de Windows
run_windows.bat
```

### Modo Producción

```bash
# Configurar puerto y opciones de producción
streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection true
```

## 🔍 Verificación de Instalación

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas de seguridad específicamente
pytest tests/test_security.py -v

# Ejecutar con cobertura
pytest --cov=src/deepagents
```

### Verificar Configuración

```bash
# Verificar que las dependencias están instaladas
pip list | grep -E "(streamlit|cryptography|pytest)"

# Verificar configuración de seguridad
python -c "from src.deepagents.config import validate_configuration; print('Configuración:', 'VÁLIDA' if validate_configuration() else 'INVÁLIDA')"
```

## 🐛 Solución de Problemas

### Error: "Python no encontrado"

```bash
# Instalar Python 3.8+
# Windows: Descargar desde python.org
# Linux: sudo apt install python3.8 python3.8-venv
```

### Error: "Dependencias faltantes"

```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "API Keys no válidas"

```bash
# Verificar que las API keys son correctas
# Revisar que no hay espacios extra
# Confirmar que las claves no han expirado
```

### Error: "Puerto 8501 en uso"

```bash
# Cambiar puerto
streamlit run streamlit_app.py --server.port 8502

# O matar proceso existente
# Windows: netstat -ano | findstr :8501
# Linux: lsof -ti:8501 | xargs kill -9
```

## 📊 Monitoreo y Logs

### Ver Logs de la Aplicación

```bash
# Logs se guardan en:
tail -f sofia_secure.log

# Logs estructurados en JSON
tail -f sofia_secure.log | jq .
```

### Métricas de Rendimiento

- Las métricas Prometheus están disponibles en `http://localhost:8000`
- Dashboard de Grafana puede conectarse al endpoint de métricas

## 🔄 Actualizaciones

### Actualizar SOF-IA

```bash
# Obtener últimas actualizaciones
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Ejecutar migraciones si existen
# (por ahora manual)
```

### Backup de Configuración

```bash
# Backup de configuración segura
cp .env .env.backup
cp sofia_secure.log sofia_secure.log.backup
```

## 🆘 Soporte

Si encuentras problemas durante la instalación:

1. **Revisa los logs**: `tail -f sofia_secure.log`
2. **Ejecuta las pruebas**: `pytest tests/test_security.py -v`
3. **Verifica la configuración**: Asegúrate de que todas las variables de entorno están configuradas
4. **Abre un issue**: [GitHub Issues](https://github.com/Cesde-Suroeste/Sof-ia/issues)

## 📋 Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Master key generada
- [ ] API keys configuradas y encriptadas
- [ ] Archivo .env configurado
- [ ] Pruebas ejecutadas exitosamente
- [ ] Aplicación ejecutándose en http://localhost:8501
