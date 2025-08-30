"""
Sistema de autenticación básico para SOF-IA.
Proporciona autenticación de usuarios con JWT y gestión de sesiones.
"""
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import streamlit as st
from .config import secure_config
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    """Gestor de autenticación con JWT y hash seguro de contraseñas."""

    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET', 'sofia-jwt-secret-key-change-in-production')
        self.users_db = self._load_users_db()

    def _load_users_db(self) -> Dict[str, Dict[str, Any]]:
        """Cargar base de datos de usuarios (en memoria por ahora)."""
        # En producción, esto debería venir de una base de datos
        default_users = {
            "admin": {
                "password_hash": self._hash_password("admin123"),  # Cambiar en producción
                "role": "admin",
                "enabled": True
            },
            "user": {
                "password_hash": self._hash_password("user123"),  # Cambiar en producción
                "role": "user",
                "enabled": True
            }
        }

        # Incluir usuarios registrados desde session_state
        if 'registered_users' in st.session_state:
            default_users.update(st.session_state.registered_users)

        return default_users

    def _hash_password(self, password: str) -> str:
        """Hash seguro de contraseña usando SHA-256 con salt."""
        salt = os.getenv('PASSWORD_SALT', 'sofia-salt-2024')
        salted_password = password + salt
        return hashlib.sha256(salted_password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verificar contraseña contra hash."""
        return self._hash_password(password) == password_hash

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autenticar usuario y devolver información si es válido."""
        user = self.users_db.get(username)
        if not user or not user.get('enabled', False):
            logger.warning(f"Intento de login fallido para usuario: {username}")
            return None

        if self._verify_password(password, user['password_hash']):
            logger.info(f"Login exitoso para usuario: {username}")
            return {
                'username': username,
                'role': user['role'],
                'login_time': datetime.utcnow().isoformat()
            }
        else:
            logger.warning(f"Contraseña incorrecta para usuario: {username}")
            return None

    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        """Registrar un nuevo usuario."""
        if not username or not password:
            logger.warning("Intento de registro con campos vacíos")
            return False

        if username in self.users_db:
            logger.warning(f"Intento de registro con usuario existente: {username}")
            return False

        # Crear usuario registrado
        new_user = {
            "password_hash": self._hash_password(password),
            "role": role,
            "enabled": True,
            "registered_at": datetime.utcnow().isoformat()
        }

        # Guardar en session_state para persistencia temporal
        if 'registered_users' not in st.session_state:
            st.session_state.registered_users = {}
        st.session_state.registered_users[username] = new_user

        # Actualizar users_db
        self.users_db[username] = new_user

        logger.info(f"Usuario registrado exitosamente: {username}")
        return True

    def create_jwt_token(self, user_info: Dict[str, Any]) -> str:
        """Crear token JWT para el usuario."""
        payload = {
            'user': user_info['username'],
            'role': user_info['role'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24)  # 24 horas
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        return token

    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verificar token JWT y devolver información del usuario."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return {
                'username': payload['user'],
                'role': payload['role']
            }
        except jwt.ExpiredSignatureError:
            logger.warning("Token JWT expirado")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Token JWT inválido")
            return None

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Obtener usuario actual desde session state."""
        if 'auth_token' in st.session_state:
            return self.verify_jwt_token(st.session_state.auth_token)
        return None

    def require_auth(self, required_role: Optional[str] = None) -> bool:
        """Verificar que el usuario esté autenticado y tenga el rol requerido."""
        user = self.get_current_user()
        if not user:
            return False

        if required_role and user.get('role') != required_role:
            logger.warning(f"Usuario {user['username']} no tiene rol requerido: {required_role}")
            return False

        return True

    def logout(self):
        """Cerrar sesión del usuario con limpieza completa."""
        keys_to_remove = [
            'auth_token', 'user_info', 'remember_me', 'login_timestamp',
            'session_start', 'agent', 'agent_model', 'agent_instructions',
            'last_result', 'query_history', 'favorites'
        ]

        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

        logger.info("Usuario cerró sesión - limpieza completa realizada")

    def remember_session(self, user_info: Dict[str, Any]):
        """Recordar sesión del usuario para próximos accesos."""
        if st.session_state.get('remember_me', False):
            # Guardar información de sesión persistente
            st.session_state.persistent_user = user_info['username']
            st.session_state.persistent_role = user_info['role']
            st.session_state.session_remembered = True
            logger.info(f"Sesión recordada para usuario: {user_info['username']}")

    def restore_session(self) -> Optional[Dict[str, Any]]:
        """Restaurar sesión recordada si existe."""
        if (st.session_state.get('session_remembered', False) and
            'persistent_user' in st.session_state):

            username = st.session_state.persistent_user
            role = st.session_state.persistent_role

            # Verificar que el usuario aún existe
            if username in self.users_db:
                user_info = {
                    'username': username,
                    'role': role,
                    'login_time': datetime.utcnow().isoformat(),
                    'restored': True
                }

                # Crear nuevo token
                token = self.create_jwt_token(user_info)
                st.session_state.auth_token = token
                st.session_state.user_info = user_info
                st.session_state.session_start = time.time()

                logger.info(f"Sesión restaurada para usuario: {username}")
                return user_info

        return None

# Instancia global del gestor de autenticación
auth_manager = AuthManager()

def login_form() -> bool:
    """Mostrar formulario de login/registro moderno y manejar autenticación."""
    st.sidebar.markdown("---")

    # Intentar restaurar sesión recordada
    restored_user = auth_manager.restore_session()
    if restored_user:
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; animation: fadeIn 0.5s ease-out;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">🔄</span>
                <div>
                    <strong>Sesión Restaurada</strong><br>
                    <small>Bienvenido de vuelta, {}!</small>
                </div>
            </div>
        </div>
        """.format(restored_user['username']), unsafe_allow_html=True)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
                with st.spinner("Cerrando sesión..."):
                    time.sleep(0.5)
                auth_manager.logout()
                st.success("✅ Sesión cerrada exitosamente")
                time.sleep(1)
                st.rerun()

        with col2:
            if st.sidebar.button("🔒 Nueva Sesión", use_container_width=True):
                # Mantener usuario pero limpiar sesión temporal
                if 'session_remembered' in st.session_state:
                    del st.session_state.session_remembered
                st.info("🔄 Nueva sesión iniciada")
                time.sleep(1)
                st.rerun()

        return True

    # Estado de autenticación normal
    if auth_manager.get_current_user():
        user = auth_manager.get_current_user()
        is_restored = user.get('restored', False)

        status_icon = "🔄" if is_restored else "✅"
        status_text = "Sesión Restaurada" if is_restored else "Conectado"

        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; animation: fadeIn 0.5s ease-out;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">{}</span>
                <div>
                    <strong>{}</strong><br>
                    <small>{{}} ({{}})</small>
                </div>
            </div>
        </div>
        """.format(status_icon, status_text, user['username'], user['role']), unsafe_allow_html=True)

        # Botón de logout mejorado
        if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
            with st.spinner("Cerrando sesión..."):
                time.sleep(0.5)
            auth_manager.logout()
            st.success("✅ Sesión cerrada exitosamente")
            time.sleep(1)
            st.rerun()
        return True

    # Contenedor principal de autenticación
    st.sidebar.markdown("""
    <div class="auth-container">
        <h3 style="margin: 0 0 1.5rem 0; color: #333; text-align: center;">
            🔐 <span class="text-gradient">Autenticación</span>
        </h3>
    """, unsafe_allow_html=True)

    # Sistema de pestañas moderno
    tab_selection = st.sidebar.radio(
        "Selecciona una opción",
        ["🔑 Iniciar Sesión", "📝 Registrarse"],
        key="auth_tab",
        label_visibility="collapsed",
        horizontal=True
    )

    if tab_selection == "🔑 Iniciar Sesión":
        with st.sidebar.form("login_form"):
            st.markdown("### 🔑 Iniciar Sesión")

            # Campo de usuario con icono
            st.markdown("""
            <div class="form-group">
                <input type="text" id="login_username" name="username" placeholder="Usuario" required>
                <label class="form-icon" for="login_username">👤</label>
            </div>
            """, unsafe_allow_html=True)

            # Campo de contraseña con icono
            st.markdown("""
            <div class="form-group">
                <input type="password" id="login_password" name="password" placeholder="Contraseña" required>
                <label class="form-icon" for="login_password">🔒</label>
            </div>
            """, unsafe_allow_html=True)

            # Checkbox recordar sesión
            remember_me = st.checkbox("Recordar sesión", key="remember_login")

            submitted = st.form_submit_button(
                "🚀 Iniciar Sesión",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                username = st.session_state.get('login_username', '')
                password = st.session_state.get('login_password', '')

                if not username or not password:
                    st.error("❌ Por favor complete todos los campos")
                    return False

                with st.spinner("🔐 Verificando credenciales..."):
                    user_info = auth_manager.authenticate_user(username, password)

                if user_info:
                    token = auth_manager.create_jwt_token(user_info)
                    st.session_state.auth_token = token
                    st.session_state.user_info = user_info
                    st.session_state.session_start = time.time()

                    # Recordar sesión si está marcado
                    if remember_me:
                        auth_manager.remember_session(user_info)

                    st.success("✅ ¡Bienvenido de vuelta!")
                    time.sleep(1)
                    st.rerun()
                    return True
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
                    return False

    else:  # Registro
        with st.sidebar.form("register_form"):
            st.markdown("### 📝 Crear Cuenta")

            # Campo de usuario con validación
            st.markdown("""
            <div class="form-group">
                <input type="text" id="reg_username" name="new_username" placeholder="Nombre de usuario" pattern="[a-zA-Z0-9_]{3,20}" title="3-20 caracteres, solo letras, números y guiones bajos" required>
                <label class="form-icon" for="reg_username">👤</label>
            </div>
            """, unsafe_allow_html=True)

            # Campo de contraseña con validación
            st.markdown("""
            <div class="form-group">
                <input type="password" id="reg_password" name="new_password" placeholder="Contraseña (mín. 6 caracteres)" pattern=".{6,}" title="Mínimo 6 caracteres" required>
                <label class="form-icon" for="reg_password">🔒</label>
            </div>
            """, unsafe_allow_html=True)

            # Campo de confirmación
            st.markdown("""
            <div class="form-group">
                <input type="password" id="reg_confirm" name="confirm_password" placeholder="Confirmar contraseña" required>
                <label class="form-icon" for="reg_confirm">🔄</label>
            </div>
            """, unsafe_allow_html=True)

            submitted_reg = st.form_submit_button(
                "✨ Crear Cuenta",
                use_container_width=True,
                type="secondary"
            )

            if submitted_reg:
                new_username = st.session_state.get('reg_username', '')
                new_password = st.session_state.get('reg_password', '')
                confirm_password = st.session_state.get('reg_confirm', '')

                # Validaciones
                if not new_username or not new_password:
                    st.error("❌ Por favor complete todos los campos")
                    return False

                if len(new_username) < 3:
                    st.error("❌ El nombre de usuario debe tener al menos 3 caracteres")
                    return False

                if new_password != confirm_password:
                    st.error("❌ Las contraseñas no coinciden")
                    return False

                if len(new_password) < 6:
                    st.error("❌ La contraseña debe tener al menos 6 caracteres")
                    return False

                with st.spinner("📝 Creando cuenta..."):
                    if auth_manager.register_user(new_username, new_password):
                        st.success("✅ ¡Cuenta creada exitosamente!")
                        st.info("🔑 Ahora puede iniciar sesión con sus credenciales")
                        time.sleep(2)
                        return False  # No devolver True aún, debe hacer login
                    else:
                        st.error("❌ Error al crear la cuenta. El usuario ya existe.")
                        return False

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # Información de ayuda
    with st.sidebar.expander("ℹ️ Credenciales por defecto"):
        st.markdown("""
        **Para desarrollo (cambiar en producción):**
        - **Admin**: admin / admin123
        - **Usuario**: user / user123

        Para configurar usuarios personalizados, modifique `src/deepagents/auth.py`
        """)

    return False

def require_login(required_role: Optional[str] = None):
    """Decorador para requerir autenticación."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not auth_manager.require_auth(required_role):
                st.error("❌ Debe iniciar sesión para acceder a esta funcionalidad")
                login_form()
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator