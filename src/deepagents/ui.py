"""
Componentes de interfaz de usuario moderna para SOF-IA.
Incluye estilos CSS personalizados, componentes responsivos y UX mejorada.
"""
import streamlit as st
from typing import Optional, Dict, Any
import time

def load_custom_css():
    """Cargar estilos CSS personalizados para una UI moderna y avanzada."""
    custom_css = """
    <style>
    /* Variables CSS para consistencia */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        --error-gradient: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        --warning-gradient: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        --info-gradient: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        --shadow-light: 0 4px 20px rgba(0,0,0,0.08);
        --shadow-medium: 0 8px 32px rgba(102, 126, 234, 0.3);
        --shadow-heavy: 0 12px 40px rgba(102, 126, 234, 0.4);
        --border-radius: 12px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Reset y base */
    * {
        box-sizing: border-box;
    }

    /* Tema moderno y profesional */
    .main-header {
        background: var(--primary-gradient);
        color: white;
        padding: 2.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-medium);
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s ease-out;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }

    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }

    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin: 0;
        position: relative;
        z-index: 2;
    }

    /* Animaciones */
    @keyframes slideInDown {
        from {
            transform: translateY(-100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.1; }
        50% { opacity: 0.3; }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }

    /* Cards modernos con mejoras */
    .metric-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow-light);
        border: 1px solid rgba(255,255,255,0.8);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.6s ease-out;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }

    .metric-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: var(--shadow-heavy);
    }

    .metric-card .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .metric-card .metric-label {
        font-size: 1rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }

    /* Formularios de autenticación mejorados */
    .auth-container {
        background: white;
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow-medium);
        border: 1px solid rgba(102, 126, 234, 0.1);
        animation: bounceIn 0.6s ease-out;
    }

    .auth-tabs {
        display: flex;
        margin-bottom: 2rem;
        background: #f8f9fa;
        border-radius: 8px;
        padding: 4px;
    }

    .auth-tab {
        flex: 1;
        padding: 0.75rem 1rem;
        border: none;
        background: transparent;
        border-radius: 6px;
        cursor: pointer;
        transition: var(--transition);
        font-weight: 500;
        color: #666;
    }

    .auth-tab.active {
        background: white;
        color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }

    .form-group {
        margin-bottom: 1.5rem;
        position: relative;
    }

    .form-group input {
        width: 100%;
        padding: 1rem 1rem 1rem 3rem;
        border: 2px solid #e1e5e9;
        border-radius: 8px;
        font-size: 1rem;
        transition: var(--transition);
        background: #fafbfc;
    }

    .form-group input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
        background: white;
    }

    .form-group input:valid {
        border-color: #4CAF50;
    }

    .form-group input:invalid:not(:placeholder-shown) {
        border-color: #f44336;
    }

    .form-icon {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #999;
        font-size: 1.2rem;
    }

    .form-group input:focus + .form-icon {
        color: #667eea;
    }

    /* Botones mejorados */
    .custom-button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: var(--transition);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        font-size: 1rem;
    }

    .custom-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .custom-button:hover::before {
        left: 100%;
    }

    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-heavy);
    }

    .custom-button:active {
        transform: translateY(0);
    }

    .custom-button.secondary {
        background: var(--secondary-gradient);
    }

    .custom-button.success {
        background: var(--success-gradient);
    }

    .custom-button.error {
        background: var(--error-gradient);
    }

    /* Estados de carga mejorados */
    .loading-container {
        text-align: center;
        padding: 3rem;
        animation: fadeIn 0.5s ease-out;
    }

    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }

    .loading-dots {
        display: inline-block;
    }

    .loading-dots::after {
        content: '...';
        animation: dots 1.5s steps(4, end) infinite;
    }

    @keyframes dots {
        0%, 20% { color: rgba(102, 126, 234, 0); text-shadow: .25em 0 0 rgba(102, 126, 234, 0), .5em 0 0 rgba(102, 126, 234, 0); }
        40% { color: #667eea; text-shadow: .25em 0 0 rgba(102, 126, 234, 0), .5em 0 0 rgba(102, 126, 234, 0); }
        60% { text-shadow: .25em 0 0 #667eea, .5em 0 0 rgba(102, 126, 234, 0); }
        80%, 100% { text-shadow: .25em 0 0 #667eea, .5em 0 0 #667eea; }
    }

    /* Mensajes de notificación mejorados */
    .notification {
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        border-left: 4px solid;
        position: relative;
        animation: slideInRight 0.5s ease-out;
        box-shadow: var(--shadow-light);
    }

    .notification.success {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(69, 160, 73, 0.1) 100%);
        border-left-color: #4CAF50;
        color: #2e7d32;
    }

    .notification.error {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(211, 47, 47, 0.1) 100%);
        border-left-color: #f44336;
        color: #c62828;
    }

    .notification.warning {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.1) 0%, rgba(245, 124, 0, 0.1) 100%);
        border-left-color: #ff9800;
        color: #ef6c00;
    }

    .notification.info {
        background: var(--info-gradient);
        color: white;
        border-left-color: #1976D2;
    }

    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    /* Sidebar mejorada */
    .sidebar-content {
        padding: 1.5rem;
        animation: fadeIn 0.8s ease-out;
    }

    .sidebar-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
        box-shadow: var(--shadow-light);
        transition: var(--transition);
    }

    .sidebar-section:hover {
        transform: translateX(4px);
        box-shadow: var(--shadow-medium);
    }

    .sidebar-section h3 {
        color: #333;
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Responsive design mejorado */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
        }

        .main-header h1 {
            font-size: 2.2rem;
        }

        .main-header p {
            font-size: 1rem;
        }

        .auth-container {
            padding: 1.5rem;
            margin: 1rem;
        }

        .metric-card {
            margin-bottom: 1rem;
            padding: 1.5rem;
        }

        .custom-button {
            width: 100%;
            margin-bottom: 0.5rem;
        }

        .auth-tabs {
            flex-direction: column;
        }
    }

    /* Tema oscuro mejorado */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background: #2d3748;
            border-color: #4a5568;
            color: white;
        }

        .auth-container {
            background: #2d3748;
            border-color: #4a5568;
        }

        .sidebar-section {
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
            color: white;
        }

        .form-group input {
            background: #2d3748;
            border-color: #4a5568;
            color: white;
        }

        .form-group input:focus {
            background: #1a202c;
        }
    }

    /* Accesibilidad */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* Focus visible para navegación por teclado */
    .custom-button:focus-visible,
    .form-group input:focus-visible {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }

    /* Utilidades */
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }

    .bounce-in {
        animation: bounceIn 0.6s ease-out;
    }

    .text-gradient {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def modern_header(title: str, subtitle: str):
    """Crear un header moderno y atractivo."""
    st.markdown(f"""
    <div class="main-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def metric_card(value: str, label: str, icon: Optional[str] = None):
    """Crear una tarjeta de métrica moderna."""
    icon_html = f'<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>' if icon else ''
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{icon_html}{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def custom_button(label: str, key: Optional[str] = None, type: str = "primary", **kwargs):
    """Crear un botón personalizado con estilo moderno."""
    button_type = "secondary" if type == "secondary" else ""
    if st.button(label, key=key, **kwargs):
        st.markdown(f"""
        <style>
        .stButton>button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 2rem !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4) !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        return True
    return False

def enhanced_text_area(label: str, value: str = "", height: int = 120, **kwargs):
    """Crear un área de texto mejorada."""
    st.markdown('<style>.stTextArea textarea {border-radius: 8px; border: 2px solid #e1e5e9; padding: 1rem;}</style>',
                unsafe_allow_html=True)
    return st.text_area(label, value=value, height=height, **kwargs)

def loading_spinner(message: str = "Procesando..."):
    """Mostrar un spinner de carga moderno."""
    with st.container():
        st.markdown(f"""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p style="color: #667eea; font-weight: 500;">{message}</p>
        </div>
        """, unsafe_allow_html=True)

def status_message(message: str, type: str = "info"):
    """Mostrar mensaje de estado con estilo."""
    if type == "success":
        st.markdown(f"""
        <div class="success-message">
            ✅ {message}
        </div>
        """, unsafe_allow_html=True)
    elif type == "error":
        st.markdown(f"""
        <div class="error-message">
            ❌ {message}
        </div>
        """, unsafe_allow_html=True)
    elif type == "warning":
        st.markdown(f"""
        <div class="warning-message">
            ⚠️ {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(message)

def create_sidebar_section(title: str, content_func):
    """Crear una sección organizada en la sidebar."""
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-section">
            <h3>{title}</h3>
        </div>
        """, unsafe_allow_html=True)
        content_func()

def responsive_columns(*args, **kwargs):
    """Crear columnas responsivas."""
    # En móviles, convertir a filas
    if st.session_state.get('is_mobile', False):
        for arg in args:
            if callable(arg):
                arg()
            else:
                st.write(arg)
    else:
        cols = st.columns(*args, **kwargs)
        return cols

def progress_bar_with_steps(steps: list, current_step: int):
    """Mostrar barra de progreso con pasos."""
    progress = (current_step + 1) / len(steps)

    st.progress(progress)

    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            if i < current_step:
                st.success(f"✅ {step}")
            elif i == current_step:
                st.info(f"🔄 {step}")
            else:
                st.write(f"⏳ {step}")

def theme_toggle():
    """Alternar entre tema claro y oscuro."""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("☀️ Claro" if st.session_state.theme == 'dark' else "🌙 Oscuro"):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()

def export_results(data: Dict[str, Any], filename: str = "sofia_results.json"):
    """Exportar resultados con opciones de formato."""
    import json
    from datetime import datetime

    # Agregar metadata
    export_data = {
        'metadata': {
            'exported_at': datetime.utcnow().isoformat(),
            'sofia_version': '1.0.0',
            'user': st.session_state.get('user_info', {}).get('username', 'unknown')
        },
        'data': data
    }

    json_data = json.dumps(export_data, indent=2, ensure_ascii=False)

    st.download_button(
        label="📥 Descargar Resultados (JSON)",
        data=json_data,
        file_name=filename,
        mime="application/json"
    )

def init_responsive_layout():
    """Inicializar layout responsivo con detección automática de dispositivo."""
    # Detectar si es móvil basado en el ancho de pantalla
    try:
        # Intentar detectar el ancho de pantalla (simplificado)
        st.session_state.is_mobile = False
    except:
        st.session_state.is_mobile = False

    # Configurar página con mejor metadata
    st.set_page_config(
        page_title="SOF-IA - Deep Agents Seguros",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/SOF-IA',
            'Report a bug': 'https://github.com/your-repo/SOF-IA/issues',
            'About': '''
                ## SOF-IA 🤖
                Sistema avanzado de agentes IA con seguridad de nivel empresarial.

                **Características:**
                - 🤖 Agentes IA inteligentes
                - 🔒 Seguridad de nivel empresarial
                - 📊 Monitoreo en tiempo real
                - 🎨 Interfaz moderna y responsiva
            '''
        }
    )

    # Cargar estilos personalizados
    load_custom_css()

    # Inicializar estado de sesión si no existe
    if 'session_start' not in st.session_state:
        st.session_state.session_start = time.time()

    # Verificar tiempo de sesión para auto-logout
    if 'user_info' in st.session_state:
        session_duration = time.time() - st.session_state.session_start
        max_session_time = 8 * 3600  # 8 horas

        if session_duration > max_session_time:
            from .auth import auth_manager
            auth_manager.logout()
            st.warning("⚠️ Sesión expirada por tiempo. Por favor, inicie sesión nuevamente.")
            time.sleep(2)
            st.rerun()

def enhanced_status_message(message: str, type: str = "info", duration: int = None):
    """Mensaje de estado mejorado con auto-desaparición opcional."""
    if type == "success":
        st.markdown(f"""
        <div class="notification success fade-in">
            ✅ <strong>¡Éxito!</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    elif type == "error":
        st.markdown(f"""
        <div class="notification error fade-in">
            ❌ <strong>Error:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    elif type == "warning":
        st.markdown(f"""
        <div class="notification warning fade-in">
            ⚠️ <strong>Advertencia:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:  # info
        st.markdown(f"""
        <div class="notification info fade-in">
            ℹ️ <strong>Información:</strong> {message}
        </div>
        """, unsafe_allow_html=True)

    # Auto-desaparición opcional
    if duration:
        time.sleep(duration)
        st.empty()

def session_manager():
    """Gestor de sesiones mejorado con indicadores visuales."""
    if 'user_info' in st.session_state:
        user = st.session_state.user_info

        # Información de sesión
        session_time = time.time() - st.session_state.session_start
        hours = int(session_time // 3600)
        minutes = int((session_time % 3600) // 60)

        with st.sidebar.expander("📊 Estado de Sesión"):
            st.markdown(f"""
            **👤 Usuario:** {user['username']}
            **🔒 Rol:** {user['role']}
            **⏱️ Tiempo activo:** {hours}h {minutes}m
            **🕒 Login:** {user.get('login_time', 'N/A')}
            """)

            # Barra de progreso de sesión
            max_session = 8 * 3600  # 8 horas
            progress = min(session_time / max_session, 1.0)

            if progress > 0.8:
                st.progress(progress)
                st.warning("⚠️ La sesión expirará pronto")
            else:
                st.progress(progress)
                st.info(f"✅ Sesión activa ({int(progress * 100)}%)")

def accessibility_features():
    """Características de accesibilidad mejoradas."""
    # Inicializar valores de accesibilidad si no existen
    if 'font_scale' not in st.session_state:
        st.session_state.font_scale = 1.0
    if 'accessibility_high_contrast' not in st.session_state:
        st.session_state.accessibility_high_contrast = False
    if 'accessibility_focus_mode' not in st.session_state:
        st.session_state.accessibility_focus_mode = False

    # Botones de accesibilidad en sidebar
    with st.sidebar.expander("♿ Accesibilidad"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Aumentar texto", key="accessibility_increase_font"):
                st.session_state.font_scale = min(st.session_state.font_scale + 0.1, 1.5)
                st.rerun()

            if st.button("📱 Alto contraste", key="accessibility_high_contrast_btn"):
                st.session_state.accessibility_high_contrast = not st.session_state.accessibility_high_contrast
                st.rerun()

        with col2:
            if st.button("🔽 Disminuir texto", key="accessibility_decrease_font"):
                st.session_state.font_scale = max(st.session_state.font_scale - 0.1, 0.8)
                st.rerun()

            if st.button("🎯 Modo foco", key="accessibility_focus_mode_btn"):
                st.session_state.accessibility_focus_mode = not st.session_state.accessibility_focus_mode
                st.rerun()

    # Aplicar configuraciones de accesibilidad
    if st.session_state.get('accessibility_high_contrast', False):
        st.markdown("""
        <style>
        body { filter: contrast(1.5) brightness(1.1); }
        .stTextInput input, .stTextArea textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.session_state.get('accessibility_focus_mode', False):
        st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        .main .block-container { max-width: none !important; padding: 2rem !important; }
        </style>
        """, unsafe_allow_html=True)

    # Escala de fuente
    font_scale = st.session_state.get('font_scale', 1.0)
    if font_scale != 1.0:
        st.markdown(f"""
        <style>
        body {{ font-size: {font_scale}em !important; }}
        .stTextInput input, .stTextArea textarea, .stButton button {{
            font-size: {font_scale}em !important;
        }}
        </style>
        """, unsafe_allow_html=True)