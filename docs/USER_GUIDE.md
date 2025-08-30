# 📖 Guía del Usuario - SOF-IA

## Bienvenido a SOF-IA

SOF-IA es un asistente de IA avanzado que te ayuda a investigar temas complejos y generar informes detallados de alta calidad. Con tecnología de vanguardia y protocolos de seguridad empresarial, SOF-IA te proporciona análisis profundos y estructurados sobre cualquier tema que necesites investigar.

## 🚀 Inicio Rápido

### Primeros Pasos

1. **Accede a la aplicación** en `http://localhost:8501`
2. **Inicia sesión** con tus credenciales
3. **Configura tu consulta** en el área de texto principal
4. **Haz clic en "Generar Informe Avanzado"**
5. **Espera los resultados** y explora las opciones adicionales

### Credenciales por Defecto

- **Usuario**: admin / admin123 (acceso completo)
- **Usuario**: user / user123 (acceso limitado)

⚠️ **Importante**: Cambia estas credenciales en producción por seguridad.

## 💬 Realizando Consultas

### Tipos de Consultas Soportadas

#### Investigación Académica

```
"Analiza los avances en inteligencia artificial cuántica durante 2024"
"Investiga el impacto de los modelos de lenguaje en la educación superior"
"Examina las tendencias en aprendizaje automático para el procesamiento de imágenes"
```

#### Análisis de Mercado

```
"Evalúa el mercado de criptomonedas y sus perspectivas para 2025"
"Analiza las estrategias de marketing digital en redes sociales"
"Investiga las tendencias de consumo sostenible en la industria alimentaria"
```

#### Consultas Técnicas

```
"Explica el funcionamiento de los transformers en el procesamiento de lenguaje natural"
"Compara las arquitecturas de redes neuronales convolucionales vs transformers"
"Analiza las mejores prácticas para implementar DevOps en empresas tecnológicas"
```

### Mejores Prácticas para Consultas

#### ✅ Hazlo Específico

- ❌ "Háblame sobre IA"
- ✅ "Compara GPT-4 vs Claude vs Gemini para tareas de análisis de datos"

#### ✅ Proporciona Contexto

- ❌ "Ventajas de Python"
- ✅ "Analiza las ventajas de Python para desarrollo web en comparación con Node.js"

#### ✅ Especifica el Enfoque

- ❌ "Tendencias tecnológicas"
- ✅ "Examina las tendencias emergentes en computación en la nube para startups"

## 🎯 Características Principales

### 1. Generación de Informes Inteligente

SOF-IA genera informes estructurados con:

- **Resumen Ejecutivo**: Visión general del tema
- **Análisis Profundo**: Desarrollo detallado con datos
- **Casos de Uso**: Aplicaciones prácticas
- **Limitaciones**: Consideraciones importantes
- **Conclusiones**: Hallazgos principales
- **Fuentes**: Referencias verificadas

### 2. Búsqueda Web en Tiempo Real

- Integración con Tavily para información actualizada
- Fuentes verificadas y confiables
- Análisis de múltiples perspectivas
- Validación cruzada de información

### 3. Interfaz Moderna y Intuitiva

- **Diseño Responsivo**: Funciona en desktop, tablet y móvil
- **Tema Adaptable**: Modo claro y oscuro
- **Navegación Fluida**: Interfaz intuitiva y moderna
- **Feedback Visual**: Indicadores de progreso y estado

### 4. Seguridad de Nivel Empresarial

- **Encriptación AES-256**: Protección de datos sensibles
- **Autenticación JWT**: Sesiones seguras
- **Auditoría Completa**: Registro de todas las actividades
- **Control de Acceso**: Roles y permisos granulares

### 5. Monitorización en Tiempo Real

- **Métricas de Rendimiento**: Latencia y uso de recursos
- **Dashboard Integrado**: Estadísticas en tiempo real
- **Logs Estructurados**: Seguimiento detallado de operaciones
- **Alertas Automáticas**: Notificaciones de problemas

## 🛠️ Configuración Avanzada

### Personalización del Agente

En la barra lateral, puedes configurar:

#### Modelo de IA

- **Gemini 2.0 Flash** (recomendado): Equilibrio perfecto entre velocidad y calidad
- **Gemini 1.5 Pro**: Mayor capacidad de análisis para temas complejos
- **Gemini 1.5 Flash**: Optimizado para respuestas rápidas

#### Instrucciones del Sistema

Personaliza cómo el agente responde:

- Cambia el estilo de escritura
- Ajusta la longitud de los informes
- Especifica formatos particulares
- Enfoca en industrias específicas

### Ejemplo de Personalización

```python
# Para informes técnicos detallados
"Siempre incluye código de ejemplo y diagramas técnicos cuando sea relevante"

# Para análisis ejecutivo
"Enfócate en implicaciones comerciales y recomendaciones estratégicas"

# Para investigación académica
"Incluye referencias bibliográficas y metodología de investigación"
```

## 📊 Gestión de Resultados

### Exportación de Informes

SOF-IA permite exportar tus resultados en múltiples formatos:

#### Exportación JSON

- **Incluye**: Consulta original, respuesta completa, metadatos
- **Útil para**: Procesamiento posterior, integración con otras herramientas
- **Formato**: JSON estructurado con timestamps

#### Guardado de Favoritos

- **Función**: Guarda consultas importantes para referencia futura
- **Acceso**: Disponible en la sección de estadísticas
- **Organización**: Búsqueda y filtrado por fecha/tema

### Historial de Consultas

- **Seguimiento**: Todas las consultas quedan registradas
- **Búsqueda**: Encuentra consultas anteriores rápidamente
- **Estadísticas**: Métricas de uso personalizadas

## 🔍 Solución de Problemas

### Problemas Comunes

#### "Error de Configuración"

**Síntomas**: La aplicación no inicia o muestra errores de configuración
**Solución**:

1. Verifica que el archivo `.env` existe
2. Confirma que las API keys están configuradas
3. Ejecuta `python scripts/encrypt_keys.py` para encriptar claves
4. Reinicia la aplicación

#### "Error de Autenticación"

**Síntomas**: No puedes iniciar sesión
**Solución**:

1. Verifica credenciales (admin/admin123 por defecto)
2. Confirma que el archivo `.env` tiene `JWT_SECRET`
3. Borra cookies del navegador si es necesario

#### "Informe No Generado"

**Síntomas**: La consulta no produce resultados
**Solución**:

1. Verifica conexión a internet
2. Confirma que las API keys de Gemini y Tavily son válidas
3. Revisa los logs en `sofia_secure.log`
4. Intenta con una consulta más simple

#### "Aplicación Lenta"

**Síntomas**: Respuestas lentas o timeouts
**Solución**:

1. Verifica conexión a internet
2. Reduce la complejidad de la consulta
3. Espera a que se complete la búsqueda web
4. Consulta las métricas de rendimiento en el dashboard

### Logs y Diagnóstico

#### Verificar Logs

```bash
# Ver logs en tiempo real
tail -f sofia_secure.log

# Buscar errores específicos
grep "ERROR" sofia_secure.log

# Ver logs de los últimos 100 líneas
tail -100 sofia_secure.log
```

#### Métricas de Rendimiento

- **Uptime**: Tiempo que la aplicación ha estado ejecutándose
- **Requests**: Número total de consultas procesadas
- **Latencia**: Tiempo promedio de respuesta
- **Errores**: Tasa de error de las operaciones

## 🎨 Personalización de la Interfaz

### Tema Visual

- **Modo Claro**: Ideal para ambientes de oficina
- **Modo Oscuro**: Recomendado para uso nocturno
- **Auto-detección**: Se adapta a las preferencias del sistema

### Layout Responsivo

- **Desktop**: Layout completo con sidebar expandida
- **Tablet**: Sidebar colapsable, componentes adaptados
- **Móvil**: Interfaz simplificada, navegación por pestañas

## 📈 Métricas y Estadísticas

### Dashboard de Usuario

- **Consultas Realizadas**: Número total de búsquedas
- **Tiempo Promedio**: Latencia de respuestas
- **Temas Más Consultados**: Análisis de patrones
- **Éxito de Operaciones**: Tasa de consultas exitosas

### Métricas de Rendimiento

- **Disponibilidad**: Porcentaje de uptime
- **Velocidad**: Tiempo de respuesta promedio
- **Fiabilidad**: Tasa de error del sistema
- **Uso**: Recursos consumidos por sesión

## 🔒 Seguridad y Privacidad

### Protección de Datos

- **Encriptación**: Todas las comunicaciones encriptadas
- **Almacenamiento Seguro**: Datos sensibles protegidos
- **Auditoría**: Registro completo de actividades
- **Control de Acceso**: Solo usuarios autorizados

### Cumplimiento Normativo

- **RGPD**: Protección de datos personales
- **LGPD**: Cumplimiento con legislación brasileña
- **ISO 27001**: Estándares de seguridad de la información

## 🚀 Consejos Avanzados

### Optimización de Consultas

1. **Sé Específico**: Cuanto más detallada la consulta, mejor el resultado
2. **Proporciona Contexto**: Ayuda al agente a entender el alcance
3. **Usa Palabras Clave**: Mejora la precisión de la búsqueda
4. **Itera**: Refina tu consulta basado en los resultados

### Uso Eficiente

1. **Configura el Modelo**: Elige el modelo adecuado para tu necesidad
2. **Personaliza Instrucciones**: Adapta el comportamiento del agente
3. **Guarda Favoritos**: Mantén un registro de consultas importantes
4. **Monitorea Rendimiento**: Usa el dashboard para optimizar uso

## 📞 Soporte y Comunidad

### Recursos de Ayuda

- **Documentación**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Arquitectura**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **GitHub Issues**: Reporta bugs y solicita features

### Comunidad

- **Discusiones**: Únete a conversaciones en GitHub
- **Contribuciones**: Ayuda a mejorar SOF-IA
- **Feedback**: Comparte tu experiencia

## 🎯 Próximas Funcionalidades

### En Desarrollo

- **API REST**: Integración con otros sistemas
- **Dashboards Avanzados**: Visualizaciones interactivas
- **Colaboración**: Trabajo en equipo en tiempo real
- **IA Personalizada**: Modelos adaptados a tu uso

### Planificadas

- **Aplicación Móvil**: Versión nativa para iOS/Android
- **Integraciones**: Conexión con Slack, Teams, Notion
- **Analytics Avanzado**: IA para insights predictivos
- **Multi-tenancy**: Soporte para múltiples organizaciones

---

**¿Necesitas ayuda?** No dudes en abrir un [issue en GitHub](https://github.com/Cesde-Suroeste/Sof-ia/issues) o consultar la documentación técnica.
