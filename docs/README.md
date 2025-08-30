# 📚 Documentación de SOF-IA

Bienvenido a la documentación completa de SOF-IA, un sistema avanzado de agentes de IA con protocolos de seguridad de nivel empresarial.

## 📖 Guías de Inicio Rápido

### Para Usuarios

- **[Guía del Usuario](USER_GUIDE.md)** - Todo lo que necesitas saber para usar SOF-IA
- **[Instalación](INSTALLATION.md)** - Guía paso a paso para instalar y configurar

### Para Desarrolladores

- **[Arquitectura del Sistema](ARCHITECTURE.md)** - Diseño técnico y componentes
- **[Métricas y KPIs](METRICS_KPIS.md)** - Medición del rendimiento y éxito

## 🏗️ Arquitectura y Diseño

### Componentes Principales

```
SOF-IA/
├── 🔐 Seguridad
│   ├── Encriptación AES-256
│   ├── Autenticación JWT
│   └── Control de acceso
├── 🤖 IA y Agentes
│   ├── Gemini 2.0 Flash
│   ├── LangGraph orchestration
│   └── Sub-agentes especializados
├── 📊 Monitorización
│   ├── Prometheus metrics
│   ├── Structured logging
│   └── Performance monitoring
└── 🎨 Interfaz de Usuario
    ├── Diseño responsivo
    ├── Tema moderno
    └── UX optimizada
```

### Flujo de Datos

1. **Usuario** → Autenticación segura
2. **Consulta** → Validación y procesamiento
3. **Agente IA** → Análisis y búsqueda web
4. **Resultado** → Formateo y entrega segura

## 🚀 Inicio Rápido

### Instalación en 5 Minutos

```bash
# 1. Clonar repositorio
git clone https://github.com/Cesde-Suroeste/Sof-ia.git
cd Sof-ia

# 2. Ejecutar instalación automática
./run_linux.sh  # Linux/Mac
# o
run_windows.bat  # Windows

# 3. Configurar seguridad
python scripts/encrypt_keys.py

# 4. Iniciar aplicación
streamlit run streamlit_app.py
```

### Primer Uso

1. Abrir `http://localhost:8501`
2. Iniciar sesión (admin/admin123)
3. Escribir consulta de investigación
4. Generar informe avanzado

## 🔧 Configuración

### Variables de Entorno

```env
# Obligatorias
SOFIA_MASTER_KEY=tu_master_key_aqui
GEMINI_API_KEY_ENCRYPTED=clave_encriptada
TAVILY_API_KEY_ENCRYPTED=clave_encriptada

# Opcionales
JWT_SECRET=secret_para_jwt
LOG_LEVEL=INFO
METRICS_PORT=8000
```

### Personalización

- **Modelo IA**: Gemini 2.0 Flash (por defecto)
- **Tema**: Claro/Oscuro automático
- **Idioma**: Español (configurable)
- **Logs**: Estructurados con contexto

## 📊 Características Principales

### 🔒 Seguridad Empresarial

- ✅ Encriptación AES-256 para datos sensibles
- ✅ Autenticación JWT con expiración
- ✅ Control de acceso basado en roles
- ✅ Auditoría completa de actividades
- ✅ Validación automática de configuración

### 🤖 Inteligencia Artificial

- ✅ Agentes especializados con LangGraph
- ✅ Búsqueda web en tiempo real con Tavily
- ✅ Análisis profundo y estructurado
- ✅ Generación de informes de 900-1200 palabras
- ✅ Múltiples modelos IA soportados

### 📈 Monitorización Avanzada

- ✅ Métricas Prometheus integradas
- ✅ Dashboard de rendimiento en tiempo real
- ✅ Logging estructurado con JSON
- ✅ Alertas automáticas configurables
- ✅ Seguimiento de uso y rendimiento

### 🎨 Experiencia de Usuario

- ✅ Interfaz moderna y responsiva
- ✅ Diseño mobile-first
- ✅ Tema adaptable (claro/oscuro)
- ✅ Componentes interactivos
- ✅ Feedback visual inmediato

## 🧪 Calidad y Testing

### Cobertura de Pruebas

- **Unit Tests**: > 85% cobertura
- **Integration Tests**: Flujos completos
- **Security Tests**: Validación de vulnerabilidades
- **Performance Tests**: Benchmarks automatizados

### Ejecución de Pruebas

```bash
# Todas las pruebas
pytest

# Pruebas de seguridad
pytest tests/test_security.py -v

# Con cobertura
pytest --cov=src/deepagents --cov-report=html
```

### Calidad de Código

- **Black**: Formateo automático
- **Flake8**: Linting y estilo
- **MyPy**: Verificación de tipos
- **Pre-commit**: Validación automática

## 📈 Métricas y KPIs

### Rendimiento

- **Latencia**: < 2.0s promedio
- **Throughput**: > 100 consultas/hora
- **Disponibilidad**: > 99.9%
- **Tasa de Error**: < 0.1%

### Usuario

- **Satisfacción**: > 4.2/5.0
- **Adopción**: > 85%
- **Retención**: > 75% (7 días)

### Seguridad

- **Vulnerabilidades**: 0 críticas
- **Cumplimiento**: 100% RGPD
- **Intentos de Intrusión**: < 10/día

## 🔄 Ciclo de Desarrollo

### Versionado Semántico

- **MAJOR.MINOR.PATCH**
- **v1.0.0**: Primera versión estable
- **v1.1.0**: Nuevas funcionalidades
- **v1.0.1**: Parches y correcciones

### Ramas de Desarrollo

```
main          # Rama de producción
develop       # Rama de desarrollo
feature/*     # Nuevas funcionalidades
hotfix/*      # Correcciones urgentes
release/*     # Preparación de releases
```

### Proceso de Release

1. **Desarrollo** → feature branches
2. **Testing** → integration en develop
3. **Staging** → release candidate
4. **Producción** → merge a main

## 🌐 Despliegue y Escalabilidad

### Opciones de Despliegue

- **Local**: Desarrollo y testing
- **Docker**: Contenedorización
- **Kubernetes**: Orquestación escalable
- **Cloud**: AWS/GCP/Azure

### Escalabilidad

- **Horizontal**: Auto-scaling con K8s
- **Vertical**: Optimización de recursos
- **Caching**: Redis para sesiones
- **CDN**: Distribución global

## 🤝 Contribución

### Cómo Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Guías de Contribución

- Seguir estándares de código
- Escribir pruebas para nuevas funcionalidades
- Actualizar documentación
- Mantener compatibilidad hacia atrás

## 📞 Soporte

### Canales de Soporte

- **GitHub Issues**: Bugs y features
- **Discussions**: Preguntas generales
- **Documentation**: Búsqueda en docs
- **Community**: Foro de usuarios

### Niveles de Soporte

- **Community**: Auto-ayuda y comunidad
- **Standard**: Issues y preguntas
- **Priority**: Problemas críticos
- **Enterprise**: Soporte dedicado

## 📋 Roadmap

### Próximas Versiones

- **v1.1.0**: API REST completa
- **v1.2.0**: Multi-tenancy
- **v2.0.0**: Microservicios completos
- **v2.1.0**: IA personalizada

### Funcionalidades Planificadas

- [ ] Aplicación móvil nativa
- [ ] Integraciones con Slack/Teams
- [ ] Machine learning para insights
- [ ] Soporte multi-idioma
- [ ] Analytics predictivos

## 📄 Licencias y Legal

### Licencia

Este proyecto está bajo la **Licencia MIT**. Ver `LICENSE` para más detalles.

### Cumplimiento

- **RGPD**: Protección de datos personales
- **LGPD**: Cumplimiento Brasil
- **ISO 27001**: Seguridad de la información
- **OWASP**: Mejores prácticas de seguridad

## 🙏 Agradecimientos

### Tecnologías

- **Google Gemini**: Modelo de IA avanzado
- **Tavily**: Búsqueda web inteligente
- **LangChain**: Framework de IA
- **Streamlit**: Framework web
- **Prometheus**: Monitorización

### Comunidad

- Contribuidores activos
- Usuarios beta testers
- Comunidad open source
- Instituciones educativas

---

## 📚 Enlaces Útiles

- [Repositorio GitHub](https://github.com/Cesde-Suroeste/Sof-ia)
- [Documentación API](api/)
- [Guías de Troubleshooting](troubleshooting/)
- [Ejemplos de Uso](examples/)
- [Blog y Tutoriales](blog/)

---

**¿Necesitas ayuda?** Comienza con la [Guía de Instalación](INSTALLATION.md) o abre un [issue en GitHub](https://github.com/Cesde-Suroeste/Sof-ia/issues).
