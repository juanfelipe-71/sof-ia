import os
import sys
from typing import Literal

import streamlit as st
from dotenv import load_dotenv

# Load .env for local dev. On Streamlit Cloud, set secrets in app settings.
load_dotenv(override=False)

# Ensure deepagents is importable when running locally without installation
try:
    from deepagents import create_deep_agent
except ModuleNotFoundError:
    repo_src = os.path.join(os.path.dirname(__file__), "src")
    if repo_src not in sys.path:
        sys.path.insert(0, repo_src)
    from deepagents import create_deep_agent  # type: ignore

from tavily import TavilyClient

# LangChain model provider
from langchain_google_genai import ChatGoogleGenerativeAI  # for Gemini


def build_model(model_name: str | None = None):
    """Return a LangChain chat model for Gemini.

    Uses Google Generative AI via GOOGLE_API_KEY or GEMINI_API_KEY
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY/GOOGLE_API_KEY para Gemini.")
    # Gemini 2.0 Flash (adjust to released model name as available)
    model = model_name or "gemini-2.0-flash-exp"  # Using available model name
    return ChatGoogleGenerativeAI(google_api_key=api_key, model=model, temperature=0.2)


# It's best practice to initialize Tavily client once
_tavily_client = None

def get_tavily_client() -> TavilyClient:
    global _tavily_client
    if _tavily_client is None:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            raise RuntimeError("Falta TAVILY_API_KEY para búsquedas en internet (Tavily).")
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
    st.set_page_config(page_title="DeepAgents MVP: Internet Agent", page_icon="🤖", layout="wide")
    st.title("🧠🤖 Deep Agent con Internet (Tavily)")
    st.caption("MVP que usa deepagents + Tavily con Gemini 2.0 Flash para generar informes detallados.")

    with st.sidebar:
        st.header("⚙️ Configuración")
        st.info("🤖 **Modelo:** Gemini 2.0 Flash - Optimizado para informes detallados")

        model_name = st.text_input(
            "Nombre del modelo Gemini",
            value="gemini-2.0-flash-exp",
            help="Usa nombres válidos del SDK de Google Gemini.",
        )

        st.markdown("---")
        st.subheader("📝 Instrucciones del agente")
        default_instructions = (
            "Eres un investigador experto y asistente de IA. Entrega SIEMPRE un INFORME largo y bien estructurado en español (mínimo 900-1200 palabras). Tu trabajo es:\n\n"
            "1. Usar la herramienta internet_search para buscar información actualizada en internet\n"
            "2. Analizar y sintetizar la información encontrada\n"
            "3. Redactar un INFORME COMPLETO con esta estructura:\n"
            "   - Resumen ejecutivo (4-6 frases)\n"
            "   - Introducción y contexto\n"
            "   - Desarrollo del tema (secciones temáticas relevantes)\n"
            "   - Casos de uso y aplicaciones prácticas\n"
            "   - Limitaciones y consideraciones\n"
            "   - Conclusiones\n"
            "   - Fuentes y enlaces\n\n"
            "4. Integrar los hallazgos en prosa fluida (NO usar solo listas de viñetas)\n"
            "5. Incluir ejemplos concretos y datos específicos cuando sea posible\n"
            "6. Si necesitas hacer múltiples búsquedas para una tarea compleja, hazlo paso a paso\n\n"
            "IMPORTANTE: Evita responder con listas simples. Siempre redacta un informe narrativo, estructurado y extenso que demuestre análisis profundo del tema."
        )
        system_instructions = st.text_area("Prompt del sistema", value=default_instructions, height=300)

    # Initialize or update agent when configuration changes
    if ("agent" not in st.session_state or
        st.session_state.get("agent_model") != model_name or
        st.session_state.get("agent_instructions") != system_instructions):

        try:
            with st.spinner("Inicializando agente..."):
                st.session_state.agent = init_agent(model_name, system_instructions)
                st.session_state.agent_model = model_name
                st.session_state.agent_instructions = system_instructions
            st.success("✅ Agente inicializado correctamente")
        except Exception as e:
            st.error(f"❌ Error inicializando el agente: {e}")
            st.stop()

    st.markdown("## 💬 Consulta")
    user_query = st.text_area(
        "¿Sobre qué tema quieres un informe detallado?",
        placeholder="Ej: Investiga los últimos avances en modelos LLM open-source en 2025\n\nOtros ejemplos:\n- Analiza el estado actual de la IA generativa y sus aplicaciones empresariales\n- Investiga las mejores prácticas para implementar RAG en producción\n- Examina las tendencias emergentes en automatización con IA\n- Estudia el impacto de los agentes de IA en diferentes industrias",
        height=120
    )

    col_run, col_clear = st.columns([1, 1])
    run = col_run.button("📊 Generar informe", type="primary")
    if col_clear.button("🗑️ Limpiar historial", type="secondary"):
        st.session_state.pop("last_result", None)
        st.rerun()

    if run and user_query.strip():
        with st.spinner("🔍 Ejecutando agente..."):
            try:
                result = st.session_state.agent.invoke({
                    "messages": [{"role": "user", "content": user_query}]
                })
                st.session_state.last_result = result
            except Exception as e:
                st.error(f"❌ Falló la ejecución: {e}")

    if st.session_state.get("last_result"):
        st.markdown("## 📋 Resultado")
        messages = st.session_state.last_result.get("messages", [])

        # Render last assistant message
        assistant_message = None
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "ai":
                assistant_message = msg.content
                break
            elif hasattr(msg, "role") and msg.role in {"assistant", "ai"}:
                assistant_message = msg.content
                break

        if assistant_message:
            st.markdown(assistant_message)
        else:
            st.warning("No se encontró respuesta del asistente.")

        # Show tool calls history if present
        tool_messages = [m for m in messages if hasattr(m, "type") and m.type == "tool"]
        if tool_messages:
            with st.expander("🔧 Ver historial de herramientas"):
                for i, m in enumerate(tool_messages, 1):
                    st.subheader(f"Llamada {i}")
                    st.code(str(m), language="json")


if __name__ == "__main__":
    main()

