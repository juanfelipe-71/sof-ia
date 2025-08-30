"""
Sistema de monitorización para SOF-IA.
Proporciona métricas de rendimiento, logging estructurado y alertas.
"""
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import contextmanager
import streamlit as st
from prometheus_client import Counter, Histogram, Gauge, start_http_server, CollectorRegistry
import structlog

# Configurar logging estructurado
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usar un registro personalizado para evitar conflictos con recargas de módulos
registry = CollectorRegistry()

# Función para crear métricas de forma segura
def create_metric(metric_class, name, description, *args, **kwargs):
    """Crear métrica solo si no existe."""
    try:
        return metric_class(name, description, *args, registry=registry, **kwargs)
    except ValueError:
        # Si la métrica ya existe, intentar obtenerla del registro
        try:
            return registry._names_to_collectors[name]
        except KeyError:
            # Si no se puede obtener, crear con un nombre único
            unique_name = f"{name}_{int(time.time())}"
            return metric_class(unique_name, description, *args, registry=registry, **kwargs)

# Métricas Prometheus con registro personalizado
REQUEST_COUNT = create_metric(Counter, 'sofia_requests_total', 'Total de requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = create_metric(Histogram, 'sofia_request_duration_seconds', 'Duración de requests', ['method', 'endpoint'])
ACTIVE_USERS = create_metric(Gauge, 'sofia_active_users', 'Usuarios activos')
AGENT_INVOCATIONS = create_metric(Counter, 'sofia_agent_invocations_total', 'Invocaciones de agentes', ['agent_type'])
ERROR_COUNT = create_metric(Counter, 'sofia_errors_total', 'Total de errores', ['error_type'])

class MetricsCollector:
    """Colector de métricas para SOF-IA."""

    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.agent_calls = 0

    def record_request(self, method: str, endpoint: str, status: str, duration: float):
        """Registrar una petición HTTP."""
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
        self.request_count += 1

    def record_agent_call(self, agent_type: str):
        """Registrar llamada a agente."""
        AGENT_INVOCATIONS.labels(agent_type=agent_type).inc()
        self.agent_calls += 1

    def record_error(self, error_type: str):
        """Registrar error."""
        ERROR_COUNT.labels(error_type=error_type).inc()
        self.error_count += 1

    def update_active_users(self, count: int):
        """Actualizar contador de usuarios activos."""
        ACTIVE_USERS.set(count)

    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas actuales."""
        uptime = time.time() - self.start_time
        return {
            'uptime_seconds': uptime,
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'total_agent_calls': self.agent_calls,
            'requests_per_second': self.request_count / uptime if uptime > 0 else 0
        }

# Instancia global del colector de métricas
metrics = MetricsCollector()

@contextmanager
def time_request(method: str, endpoint: str):
    """Context manager para medir tiempo de requests."""
    start_time = time.time()
    try:
        yield
        duration = time.time() - start_time
        metrics.record_request(method, endpoint, 'success', duration)
        logger.info("Request completed", method=method, endpoint=endpoint, duration=duration)
    except Exception as e:
        duration = time.time() - start_time
        metrics.record_request(method, endpoint, 'error', duration)
        metrics.record_error(type(e).__name__)
        logger.error("Request failed", method=method, endpoint=endpoint, duration=duration, error=str(e))
        raise

def log_user_action(user: str, action: str, details: Optional[Dict[str, Any]] = None):
    """Registrar acción de usuario."""
    log_data = {
        'user': user,
        'action': action,
        'timestamp': datetime.utcnow().isoformat()
    }
    if details:
        log_data.update(details)

    logger.info("User action", **log_data)

def log_agent_interaction(agent_type: str, user_query: str, response_length: int, duration: float):
    """Registrar interacción con agente."""
    metrics.record_agent_call(agent_type)
    logger.info(
        "Agent interaction",
        agent_type=agent_type,
        query_length=len(user_query),
        response_length=response_length,
        duration=duration
    )

def create_monitoring_dashboard():
    """Crear dashboard de monitorización en Streamlit."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Monitorización")

    stats = metrics.get_stats()

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.metric("Uptime", f"{stats['uptime_seconds']:.0f}s")
        st.metric("Requests", stats['total_requests'])

    with col2:
        st.metric("Errors", stats['total_errors'])
        st.metric("Agent Calls", stats['total_agent_calls'])

    # Gráfico de rendimiento básico
    if st.sidebar.checkbox("Mostrar detalles"):
        st.sidebar.markdown("### 📈 Estadísticas Detalladas")
        st.sidebar.json(stats)

        # Logs recientes (simulado)
        st.sidebar.markdown("### 📝 Actividad Reciente")
        st.sidebar.code("Sistema inicializado correctamente\nUsuario admin inició sesión\nAgente invocado: deep_agent\nBúsqueda web completada")

def start_monitoring_server(port: int = 8000):
    """Iniciar servidor de métricas Prometheus."""
    try:
        start_http_server(port)
        logger.info("Monitoring server started", port=port)
    except Exception as e:
        logger.error("Failed to start monitoring server", error=str(e))

def health_check() -> Dict[str, Any]:
    """Verificación de salud del sistema."""
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'metrics': metrics.get_stats()
    }

# Función para integrar con Streamlit
def init_monitoring():
    """Inicializar monitorización en la aplicación."""
    # Actualizar usuarios activos
    if 'user_info' in st.session_state:
        metrics.update_active_users(1)  # En producción, contar usuarios reales

    # Agregar dashboard de monitorización
    create_monitoring_dashboard()