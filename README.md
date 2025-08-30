# 🧠🤖🔒 SOF-IA - Deep Agents Seguros con Gemini

**SOF-IA** es un agente de IA inteligente y seguro que utiliza Gemini 2.0 Flash para generar informes detallados y estructurados basados en búsquedas de internet en tiempo real. El sistema incorpora las más avanzadas medidas de seguridad, incluyendo encriptación AES-256, autenticación JWT, y monitorización en tiempo real. Está optimizado para producir análisis profundos y documentos extensos sobre cualquier tema solicitado, con total confidencialidad y trazabilidad.

## ✨ Características

- 🤖 **Agente IA Avanzado**: Powered by Gemini 2.0 Flash
- 🌐 **Búsqueda en Internet**: Integración con Tavily para información actualizada
- 📊 **Informes Estructurados**: Genera documentos de 900-1200 palabras mínimo
- 🎯 **Análisis Profundo**: Estructura narrativa con secciones temáticas
- 🔒 **Seguridad Avanzada**: Encriptación AES-256, autenticación JWT, logging seguro
- 📈 **Monitorización en Tiempo Real**: Métricas Prometheus, dashboards de rendimiento
- 🔐 **Autenticación Integrada**: Sistema de login con roles y permisos
- 🛡️ **Validación de Configuración**: Verificación automática de seguridad
- 📝 **Logging Estructurado**: Auditoría completa con structlog
- ⚡ **Arquitectura Modular**: Diseño escalable y mantenible

## 🚀 Inicio Rápido

### Requisitos Previos

- **Python 3.8+** instalado en tu sistema
- **API Keys** necesarias:
  - `GEMINI_API_KEY` o `GOOGLE_API_KEY` (Google AI Studio)
  - `TAVILY_API_KEY` (Tavily Search)

### 📥 Instalación Automática

#### Windows 11

```cmd
# Clona el repositorio
git clone https://github.com/Cesde-Suroeste/Sof-ia.git
cd Sof-ia

# Ejecuta el script automático
run_windows.bat
```

#### Linux Ubuntu

```bash
# Clona el repositorio
git clone https://github.com/Cesde-Suroeste/Sof-ia.git
cd Sof-ia

# Ejecuta el script automático
./run_linux.sh
```

### 🔐 Configuración Segura

#### Paso 1: Generar Master Key

```bash
# Ejecutar el script de encriptación
python scripts/encrypt_keys.py
```

Esto generará una master key segura y encriptará sus API keys.

#### Paso 2: Configurar Variables de Entorno

Cree un archivo `.env` en la raíz del proyecto:

```env
# Master key para encriptación (OBLIGATORIA)
SOFIA_MASTER_KEY=your_generated_master_key_here

# API Keys encriptadas (RECOMENDADO)
GEMINI_API_KEY_ENCRYPTED=your_encrypted_gemini_key
TAVILY_API_KEY_ENCRYPTED=your_encrypted_tavily_key

# O use variables sin encriptar (solo para desarrollo)
GEMINI_API_KEY=your_plain_gemini_key
TAVILY_API_KEY=your_plain_tavily_key

# JWT para autenticación
JWT_SECRET=your_jwt_secret_here
```

#### Paso 3: Autenticación

SOF-IA incluye autenticación integrada:

- **Admin**: admin/admin123
- **Usuario**: user/user123

⚠️ **Cambie estas credenciales en producción**

### Características de Seguridad

- 🔒 **Encriptación AES-256** para API keys sensibles
- 🔐 **Autenticación JWT** con tokens seguros
- 📊 **Logging estructurado** para auditoría
- 📈 **Monitorización en tiempo real** con métricas Prometheus
- 🛡️ **Validación de configuración** al inicio

### 🔗 Obtener API Keys

1. **Gemini API Key**:

   - Visita [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Crea una nueva API key
   - Copia la clave generada

2. **Tavily API Key**:
   - Regístrate en [Tavily](https://tavily.com/)
   - Obtén tu API key gratuita
   - Copia la clave desde tu dashboard

## 📖 Uso

1. **Ejecuta la aplicación** usando los scripts automáticos
2. **Abre tu navegador** en `http://localhost:8501`
3. **Configura el modelo** (opcional) en la barra lateral
4. **Escribe tu consulta** sobre el tema que quieres investigar
5. **Haz clic en "📊 Generar informe"**
6. **Espera el análisis** completo y detallado

### 💡 Ejemplos de Consultas

- "Investiga los últimos avances en modelos LLM open-source en 2025"
- "Analiza el estado actual de la IA generativa y sus aplicaciones empresariales"
- "Examina las tendencias emergentes en automatización con IA"
- "Estudia el impacto de los agentes de IA en diferentes industrias"

## 🛠️ Instalación Manual

Si prefieres instalar manualmente:

```bash
# 1. Clona el repositorio
git clone https://github.com/Cesde-Suroeste/Sof-ia.git
cd Sof-ia

# 2. Crea entorno virtual
python -m venv venv

# 3. Activa el entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instala dependencias
pip install -r requirements.txt

# 5. Configura variables de entorno (ver sección anterior)

# 6. Ejecuta la aplicación
streamlit run streamlit_app.py --server.port 8501
```

## 📁 Estructura del Proyecto

```
Sof-ia/
├── src/
│   └── deepagents/          # Librería principal del agente
│       ├── __init__.py
│       ├── config.py        # 🔒 Configuración segura y encriptación
│       ├── auth.py          # 🔐 Sistema de autenticación JWT
│       ├── monitoring.py    # 📊 Monitorización y métricas
│       ├── graph.py         # Grafo de agentes
│       ├── model.py         # Modelos de IA
│       ├── state.py         # Estados del agente
│       ├── tools.py         # Herramientas del agente
│       ├── prompts.py       # Prompts del sistema
│       ├── sub_agent.py     # Sub-agentes
│       └── interrupt.py     # Interrupciones
├── scripts/
│   └── encrypt_keys.py      # 🛡️ Script de encriptación
├── streamlit_app.py         # Aplicación web principal
├── requirements.txt         # Dependencias Python
├── .env.example            # 📋 Ejemplo de configuración segura
├── run_windows.bat         # Script automático Windows
├── run_linux.sh           # Script automático Linux
└── README.md             # Este archivo
```

## 🔧 Configuración Avanzada

### Personalizar el Prompt del Sistema

Puedes modificar las instrucciones del agente en la barra lateral para:

- Cambiar el estilo de escritura
- Ajustar la longitud de los informes
- Especificar formatos particulares
- Enfocar en industrias específicas

### Cambiar el Modelo de Gemini

En la configuración lateral, puedes especificar diferentes modelos:

- `gemini-2.0-flash-exp` (por defecto)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

## 🐛 Solución de Problemas

### Error: "Python no está instalado"

- Instala Python 3.8+ desde [python.org](https://python.org)
- Asegúrate de que esté en el PATH del sistema

### Error: "No se encontró API key"

- Verifica que las variables de entorno estén configuradas
- Revisa que el archivo `.env` esté en la raíz del proyecto
- Confirma que las API keys sean válidas

### Error: "Puerto 8501 en uso"

- Cierra otras instancias de Streamlit
- O cambia el puerto: `streamlit run streamlit_app.py --server.port 8502`

### La aplicación no encuentra dependencias

- Asegúrate de que el entorno virtual esté activado
- Reinstala dependencias: `pip install -r requirements.txt`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **CESDE Suroeste** - _Desarrollo inicial_ - [Cesde-Suroeste](https://github.com/Cesde-Suroeste)

## 🙏 Agradecimientos

- [Google Gemini](https://ai.google.dev/) por el modelo de IA
- [Tavily](https://tavily.com/) por la API de búsqueda
- [Streamlit](https://streamlit.io/) por el framework web
- [LangChain](https://langchain.com/) por las herramientas de IA

---

**¿Necesitas ayuda?** Abre un [issue](https://github.com/Cesde-Suroeste/Sof-ia/issues) en GitHub.
