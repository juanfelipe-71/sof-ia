import os
import sys
import time
from typing import Literal

import streamlit as st
from dotenv import load_dotenv

# Load .env for local dev. On Streamlit Cloud, set secrets in app settings.
load_dotenv(override=False)

# Ensure deepagents is importable - Add src directory to Python path
repo_src = os.path.join(os.path.dirname(__file__), "src")
if repo_src not in sys.path:
    sys.path.insert(0, repo_src)

try:
    from deepagents import create_deep_agent
    from deepagents.config import get_gemini_api_key, get_tavily_api_key, validate_configuration
    from deepagents.monitoring import init_monitoring, log_user_action, log_agent_interaction, time_request, metrics
    from deepagents.ui import (
        init_responsive_layout, modern_header, status_message, enhanced_text_area,
        loading_spinner, accessibility_features
    )
except ImportError as e:
    st.error(f"❌ Error al importar módulos: {e}")
    st.error("Asegúrate de que todos los archivos estén en sus ubicaciones correctas.")
    st.stop()

from tavily import TavilyClient

# LangChain model provider
from langchain_google_genai import ChatGoogleGenerativeAI  # for Gemini


def build_model(model_name: str | None = None):
    """Return a LangChain chat model for Gemini.

    Uses secure configuration for API keys.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY/GOOGLE_API_KEY para Gemini. Configure las variables de entorno o use encriptación.")
    # Gemini 2.0 Flash (adjust to released model name as available)
    model = model_name or "gemini-2.0-flash-exp"  # Using available model name
    return ChatGoogleGenerativeAI(google_api_key=api_key, model=model, temperature=0.2)


# It's best practice to initialize Tavily client once
_tavily_client = None

def get_tavily_client() -> TavilyClient:
    global _tavily_client
    if _tavily_client is None:
        tavily_api_key = get_tavily_api_key()
        if not tavily_api_key:
            raise RuntimeError("Falta TAVILY_API_KEY para búsquedas en internet (Tavily). Configure las variables de entorno o use encriptación.")
        _tavily_client = TavilyClient(api_key=tavily_api_key)
    return _tavily_client


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search using Tavily."""
    client = get_tavily_client()
    return client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


def init_agent(model_name: str | None, system_instructions: str):
    model = build_model(model_name)
    tools = [internet_search]
    return create_deep_agent(tools=tools, instructions=system_instructions, model=model)


def main():
    # Inicializar layout responsivo y estilos
    init_responsive_layout()

    # Header moderno con animación mejorada
    modern_header(
        "🧠🤖 SOF-IA",
        "Asistente IA inteligente con búsqueda web integrada"
    )

    # Características de accesibilidad
    accessibility_features()

    # Verificar configuración
    if not validate_configuration():
        st.error("❌ Error de configuración. Verifique las API keys en el archivo .env")
        with st.expander("🔧 Solución"):
            st.markdown("""
            **Configure estas variables en su archivo `.env`:**
            - `GEMINI_API_KEY`: Su API key de Google Gemini
            - `TAVILY_API_KEY`: Su API key de Tavily para búsqueda web
            """)
        st.stop()

    # Inicializar monitorización
    init_monitoring()
    log_user_action('usuario', 'app_access')

    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: white;">⚙️ Configuración</h3>
        </div>
        """, unsafe_allow_html=True)

        st.success("🤖 **Modelo:** Gemini 2.0 Flash")
        st.success("🔍 **Búsqueda:** Tavily integrada")

        # Selector de tipo de respuesta
        response_type = st.selectbox(
            "🎯 Tipo de respuesta",
            ["Respuesta completa", "Respuesta concisa", "Solo hechos", "Análisis detallado"],
            help="Elige cómo quieres que responda el asistente"
        )

        # Selector de idioma
        language = st.selectbox(
            "🌍 Idioma",
            ["Español", "English", "Português", "Français"],
            index=0,
            help="Idioma de la respuesta"
        )

        st.markdown("---")

        # Información del sistema
        with st.expander("ℹ️ Sobre SOF-IA"):
            st.markdown("""
            **Características:**
            - 🤖 IA avanzada con Gemini
            - 🔍 Búsqueda web en tiempo real
            - 📊 Respuestas estructuradas
            - 🎨 Interfaz moderna y accesible

            **Capacidades:**
            - Investigación profunda
            - Análisis de datos
            - Generación de informes
            - Respuestas personalizadas
            """)

    # Configurar instrucciones según el tipo de respuesta
    if response_type == "Respuesta completa":
        system_instructions = (
            "Eres un asistente IA inteligente y útil. Proporciona respuestas completas, bien estructuradas y útiles. "
            "Usa la herramienta de búsqueda web cuando necesites información actualizada. "
            f"Responde en {language.lower()} de manera clara y comprensiva."
        )
    elif response_type == "Respuesta concisa":
        system_instructions = (
            "Eres un asistente conciso pero informativo. Proporciona respuestas directas y útiles sin texto innecesario. "
            "Usa la búsqueda web solo cuando sea estrictamente necesario. "
            f"Responde en {language.lower()} de forma breve pero completa."
        )
    elif response_type == "Solo hechos":
        system_instructions = (
            "Eres un asistente que se enfoca en hechos verificables. Proporciona información objetiva y basada en evidencia. "
            "Siempre verifica la información con fuentes confiables usando la búsqueda web. "
            f"Responde en {language.lower()} con datos concretos y fuentes."
        )
    else:  # Análisis detallado
        system_instructions = (
            "Eres un analista experto. Proporciona análisis profundos y detallados con múltiples perspectivas. "
            "Utiliza la búsqueda web para obtener información comprehensiva y actualizada. "
            f"Responde en {language.lower()} con análisis completo y bien fundamentado."
        )

    # Initialize or update agent when configuration changes
    model_name = "gemini-2.0-flash-exp"  # Modelo por defecto

    if ("agent" not in st.session_state or
        st.session_state.get("agent_model") != model_name or
        st.session_state.get("agent_instructions") != system_instructions):

        try:
            with st.spinner("🤖 Inicializando agente de IA..."):
                st.session_state.agent = init_agent(model_name, system_instructions)
                st.session_state.agent_model = model_name
                st.session_state.agent_instructions = system_instructions

            st.success("✅ Agente de IA inicializado correctamente")

            # Mostrar información del agente
            with st.expander("ℹ️ Información del Agente"):
                st.markdown(f"""
                **Modelo:** {model_name}
                **Estado:** ✅ Activo
                **Búsqueda web:** Habilitada
                **Monitorización:** Activa
                """)

        except Exception as e:
            st.error(f"❌ Error inicializando el agente: {e}")
            st.stop()

    # Área principal de consulta
    st.markdown("## 💬 ¿Qué necesitas saber?")

    # Crear un contenedor más atractivo para la entrada
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #667eea;">
            <h4 style="margin-top: 0; color: #333;">🤔 Haz tu pregunta o describe lo que necesitas</h4>
        </div>
        """, unsafe_allow_html=True)

        # Área de texto mejorada
        user_query = st.text_area(
            "",
            placeholder="Escribe aquí tu pregunta o consulta...\n\nEjemplos:\n• ¿Cuáles son las últimas noticias sobre IA?\n• Explícame cómo funciona el machine learning\n• ¿Qué opinas sobre el futuro de los trabajos?\n• Investiga sobre energías renovables\n• ¿Cómo puedo aprender programación?",
            height=120,
            label_visibility="collapsed"
        )

        # Botones principales
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            run = st.button("🚀 Preguntar", type="primary", use_container_width=True)

        with col2:
            if st.button("🗑️ Limpiar", use_container_width=True):
                st.session_state.pop("last_result", None)
                st.session_state.pop("user_query", None)
                st.success("✅ Historial limpiado")
                st.rerun()

        with col3:
            if st.button("💡 Ejemplos", use_container_width=True):
                st.session_state.show_examples = not st.session_state.get('show_examples', False)
                st.rerun()

        with col4:
            if st.button("📊 Stats", use_container_width=True):
                st.session_state.show_stats = not st.session_state.get('show_stats', False)
                st.rerun()

    # Mostrar ejemplos si se solicita
    if st.session_state.get('show_examples', False):
        with st.expander("💡 Ejemplos de consultas", expanded=True):
            examples = [
                "¿Cuáles son las tendencias actuales en inteligencia artificial?",
                "Explícame cómo funciona el aprendizaje automático de manera simple",
                "¿Qué opinas sobre el impacto de la IA en el mercado laboral?",
                "Investiga sobre las energías renovables en América Latina",
                "¿Cómo puedo empezar a aprender desarrollo web?",
                "¿Cuáles son las mejores prácticas para ciberseguridad?",
                "Analiza el estado actual de la exploración espacial",
                "¿Qué tecnologías emergentes cambiarán el mundo en los próximos años?"
            ]

            cols = st.columns(2)
            for i, example in enumerate(examples):
                with cols[i % 2]:
                    if st.button(f"📝 {example}", key=f"example_{i}", use_container_width=True):
                        st.session_state.user_query = example
                        st.session_state.show_examples = False
                        st.rerun()

    # Mostrar estadísticas si se solicita
    if st.session_state.get('show_stats', False):
        with st.expander("📊 Estadísticas de uso", expanded=True):
            stats = metrics.get_stats()
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("⏱️ Tiempo activo", f"{stats['uptime_seconds']:.0f}s")
            with col2:
                st.metric("🔍 Consultas", stats['total_requests'])
            with col3:
                st.metric("⚡ RPS", f"{stats['requests_per_second']:.2f}")

    # Usar la consulta del ejemplo si existe
    if 'user_query' in st.session_state and not user_query:
        user_query = st.session_state.user_query

    if run and user_query.strip():
        # Mostrar progreso
        progress_bar = st.progress(0)
        status_text = st.empty()

        with st.spinner("🤖 Procesando tu consulta..."):
            start_time = time.time()

            try:
                # Actualizar progreso
                progress_bar.progress(25)
                status_text.text("🔍 Buscando información...")

                progress_bar.progress(50)
                status_text.text("🧠 Analizando datos...")

                # Ejecutar el agente
                result = st.session_state.agent.invoke({
                    "messages": [{"role": "user", "content": user_query}]
                })

                progress_bar.progress(75)
                status_text.text("📝 Generando respuesta...")

                duration = time.time() - start_time
                st.session_state.last_result = result

                # Log de interacción
                response_length = len(str(result))
                log_agent_interaction('deep_agent', user_query, response_length, duration)

                progress_bar.progress(100)
                status_text.text("✅ ¡Respuesta lista!")

                # Limpiar después de un momento
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()

                st.success(f"🎉 Respuesta generada en {duration:.1f} segundos")

            except Exception as e:
                duration = time.time() - start_time
                progress_bar.empty()
                status_text.empty()

                st.error(f"❌ Error al procesar la consulta: {str(e)}")
                log_user_action('usuario', 'agent_error', {'error': str(e), 'duration': duration, 'query': user_query})

                # Sugerencias de solución
                with st.expander("💡 Sugerencias"):
                    st.markdown("""
                    **Posibles soluciones:**
                    - Verifica tu conexión a internet
                    - Revisa que las API keys sean válidas
                    - Intenta reformular tu pregunta
                    - Si el problema persiste, contacta al soporte
                    """)

    # Mostrar resultados si existen
    if st.session_state.get("last_result"):
        st.markdown("## 🎯 Respuesta de SOF-IA")

        # Agregar al historial
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []

        messages = st.session_state.last_result.get("messages", [])

        # Obtener la respuesta del asistente
        assistant_message = None
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "ai":
                assistant_message = msg.content
                break
            elif hasattr(msg, "role") and msg.role in {"assistant", "ai"}:
                assistant_message = msg.content
                break

        if assistant_message:
            # Contenedor principal de respuesta
            with st.container():
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border: 1px solid #e9ecef; border-radius: 12px; padding: 2rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    <div style="display: flex; align-items: flex-start; gap: 1rem;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0;">
                            🤖
                        </div>
                        <div style="flex: 1;">
                """, unsafe_allow_html=True)

                # Mostrar la respuesta
                st.markdown(assistant_message)

                st.markdown("""
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Acciones rápidas
            st.markdown("### ⚡ Acciones")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("📋 Copiar respuesta", use_container_width=True):
                    st.code(assistant_message, language=None)
                    st.success("✅ Respuesta copiada al portapapeles")

            with col2:
                if st.button("🔄 Nueva pregunta", use_container_width=True):
                    st.session_state.pop("last_result", None)
                    st.session_state.pop("user_query", None)
                    st.rerun()

            with col3:
                if st.button("💾 Guardar", use_container_width=True):
                    if 'saved_responses' not in st.session_state:
                        st.session_state.saved_responses = []

                    st.session_state.saved_responses.append({
                        'query': user_query,
                        'response': assistant_message,
                        'timestamp': time.time(),
                        'type': response_type,
                        'language': language
                    })
                    st.success("✅ Respuesta guardada")

            with col4:
                if st.button("📤 Compartir", use_container_width=True):
                    share_url = f"Consulta: {user_query[:100]}..."
                    st.code(share_url, language=None)
                    st.info("🔗 Copia este enlace para compartir")

        else:
            st.warning("⚠️ No se pudo obtener una respuesta del asistente")

        # Mostrar búsquedas realizadas (si las hay)
        tool_messages = [m for m in messages if hasattr(m, "type") and m.type == "tool"]
        if tool_messages:
            with st.expander("🔍 Fuentes consultadas"):
                st.info(f"Se realizaron {len(tool_messages)} búsquedas web para responder tu consulta:")

                for i, msg in enumerate(tool_messages, 1):
                    with st.container():
                        st.markdown(f"**🔎 Búsqueda {i}**")

                        # Mostrar contenido de manera resumida
                        content = str(msg)
                        if len(content) > 300:
                            st.text_area(
                                f"Resultado {i}",
                                content[:300] + "...",
                                height=80,
                                disabled=True,
                                label_visibility="collapsed"
                            )
                        else:
                            st.code(content, language="json")
                        st.markdown("---")


if __name__ == "__main__":
    main()

