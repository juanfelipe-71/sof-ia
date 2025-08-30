# 🚀 SOF-IA - Despliegue en Streamlit Cloud

## 📋 Descripción

SOF-IA es una aplicación de IA avanzada con interfaz moderna que combina modelos de lenguaje de Google Gemini con búsqueda web integrada de Tavily. Esta versión está optimizada para despliegue en Streamlit Cloud.

## ✨ Características Principales

- 🤖 **IA Avanzada**: Integración con Google Gemini 2.0 Flash
- 🔍 **Búsqueda Web**: Búsqueda en tiempo real con Tavily
- 🎨 **Interfaz Moderna**: Diseño responsivo con animaciones
- 🌍 **Multiidioma**: Soporte para Español, English, Português, Français
- 📱 **Accesibilidad**: Características de accesibilidad integradas
- ⚡ **Sin Autenticación**: Acceso directo y sencillo

## 🚀 Despliegue en Streamlit Cloud

### Paso 1: Preparar el Repositorio

1. Asegúrate de que todos los archivos estén en tu repositorio de GitHub
2. Verifica que el archivo principal sea `streamlit_app.py`

### Paso 2: Configurar Secrets en Streamlit Cloud

Ve a [Streamlit Cloud](https://share.streamlit.io) y:

1. **Conecta tu repositorio** de GitHub
2. **Configura las variables de entorno** (secrets):

```toml
# En Streamlit Cloud > Settings > Secrets
GEMINI_API_KEY = "tu_api_key_de_google_gemini"
TAVILY_API_KEY = "tu_api_key_de_tavily"
JWT_SECRET = "tu_jwt_secret_seguro"
SOFIA_MASTER_KEY = "tu_master_key_segura"
PASSWORD_SALT = "tu_password_salt"
```

### Paso 3: Variables de Entorno Requeridas

| Variable           | Descripción                         | Requerida   |
| ------------------ | ----------------------------------- | ----------- |
| `GEMINI_API_KEY`   | API Key de Google Gemini            | ✅ Sí       |
| `TAVILY_API_KEY`   | API Key de Tavily para búsqueda web | ✅ Sí       |
| `JWT_SECRET`       | Secret para tokens JWT              | ❌ Opcional |
| `SOFIA_MASTER_KEY` | Master key para encriptación        | ❌ Opcional |
| `PASSWORD_SALT`    | Salt para hash de contraseñas       | ❌ Opcional |

### Paso 4: Desplegar

1. **Haz clic en "Deploy"** en Streamlit Cloud
2. **Selecciona la rama** `master` o `main`
3. **Configura el archivo principal** como `streamlit_app.py`
4. **Espera a que se complete** el despliegue

## 🔧 Configuración Avanzada

### Archivo de Configuración

El archivo `.streamlit/config.toml` ya está configurado para Streamlit Cloud:

```toml
[server]
listenOnAllIPs = true
port = 8501
headless = true

[browser]
gatherUsageStats = false
```

### Dependencias

Las dependencias están optimizadas para Streamlit Cloud en `requirements.txt`:

- `streamlit>=1.35.0` - Framework principal
- `langchain-google-genai>=1.0.0` - Para Google Gemini
- `tavily-python>=0.3.0` - Para búsqueda web
- `python-dotenv>=1.0.0` - Para variables de entorno

## 🎯 Uso de la Aplicación

### Tipos de Respuesta Disponibles

1. **Respuesta Completa**: Análisis detallado y comprehensivo
2. **Respuesta Concisa**: Información directa y breve
3. **Solo Hechos**: Datos verificables y objetivos
4. **Análisis Detallado**: Investigación profunda con múltiples perspectivas

### Idiomas Soportados

- 🇪🇸 **Español** (predeterminado)
- 🇺🇸 **English**
- 🇧🇷 **Português**
- 🇫🇷 **Français**

### Características de Accesibilidad

- 🔍 **Aumentar/Disminuir texto**
- 📱 **Alto contraste**
- 🎯 **Modo foco** (oculta sidebar)

## 📊 Monitoreo y Métricas

La aplicación incluye métricas de Prometheus para:

- ⏱️ **Tiempo de respuesta**
- 🔍 **Consultas realizadas**
- ⚡ **RPS (Requests per Second)**
- 📈 **Estadísticas de uso**

## 🛠️ Solución de Problemas

### Error de API Keys

```
❌ Error de configuración. Verifique las API keys en el archivo .env
```

**Solución**: Verifica que las secrets estén configuradas correctamente en Streamlit Cloud.

### Error de Dependencias

```
ModuleNotFoundError: No module named 'langchain_google_genai'
```

**Solución**: Las dependencias se instalan automáticamente. Si hay problemas, verifica `requirements.txt`.

### Error de Memoria

```
StreamlitCloudError: App exceeded memory limit
```

**Solución**: Optimiza el uso de memoria o considera actualizar el plan de Streamlit Cloud.

## 🔒 Seguridad

- ✅ **Sin autenticación** (acceso público)
- ✅ **Variables de entorno** para API keys
- ✅ **Encriptación** opcional para datos sensibles
- ✅ **Validación** de entradas de usuario

## 📈 Rendimiento

- ⚡ **Inicialización rápida** del agente IA
- 🔄 **Cache inteligente** de respuestas
- 📊 **Monitoreo en tiempo real**
- 🎯 **Optimización automática**

## 🌐 URLs de Ejemplo

Una vez desplegada, tu aplicación estará disponible en:

- `https://[tu-app].streamlit.app`

## 📞 Soporte

Para soporte técnico:

- 📧 **Email**: [tu-email]
- 📖 **Documentación**: Ver carpeta `docs/`
- 🐛 **Issues**: [GitHub Issues](https://github.com/juanfelipe-71/sof-ia/issues)

## 🔄 Actualizaciones

Para actualizar la aplicación:

1. **Haz push** de los cambios a GitHub
2. **Streamlit Cloud** detectará automáticamente los cambios
3. **La aplicación se redeployará** automáticamente

---

**¡Disfruta usando SOF-IA en Streamlit Cloud!** 🚀🤖
