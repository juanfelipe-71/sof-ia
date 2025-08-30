"""
Pruebas de seguridad para SOF-IA.
Valida el funcionamiento de la encriptación, autenticación y configuración segura.
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from src.deepagents.config import SecureConfig, get_gemini_api_key, get_tavily_api_key, validate_configuration
from src.deepagents.auth import AuthManager


class TestSecureConfig:
    """Pruebas para la configuración segura."""

    def test_encrypt_decrypt_value(self):
        """Prueba de encriptación y desencriptación."""
        config = SecureConfig(master_key="test_key_12345")

        original_value = "my_secret_api_key"
        encrypted = config.encrypt_value(original_value)
        decrypted = config.decrypt_value(encrypted)

        assert decrypted == original_value
        assert encrypted != original_value

    def test_get_secure_api_key_encrypted(self):
        """Prueba de obtención de API key encriptada."""
        config = SecureConfig(master_key="test_key_12345")

        # Simular variable de entorno encriptada
        test_key = "sk-test123456789"
        encrypted_key = config.encrypt_value(test_key)

        with patch.dict(os.environ, {'GEMINI_API_KEY_ENCRYPTED': encrypted_key}):
            config = SecureConfig(master_key="test_key_12345")
            retrieved_key = config.get_secure_api_key('gemini')
            assert retrieved_key == test_key

    def test_get_secure_api_key_plain(self):
        """Prueba de obtención de API key sin encriptar (fallback)."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'sk-plain123'}):
            config = SecureConfig()
            retrieved_key = config.get_secure_api_key('gemini')
            assert retrieved_key == 'sk-plain123'

    def test_validate_configuration_success(self):
        """Prueba de validación exitosa de configuración."""
        with patch.dict(os.environ, {
            'GEMINI_API_KEY': 'sk-test123',
            'TAVILY_API_KEY': 'tv-test123'
        }):
            result = validate_configuration()
            assert result is True

    def test_validate_configuration_failure(self):
        """Prueba de validación fallida de configuración."""
        with patch.dict(os.environ, {}, clear=True):
            result = validate_configuration()
            assert result is False


class TestAuthManager:
    """Pruebas para el gestor de autenticación."""

    def test_authenticate_user_success(self):
        """Prueba de autenticación exitosa."""
        auth = AuthManager()
        result = auth.authenticate_user('admin', 'admin123')

        assert result is not None
        assert result['username'] == 'admin'
        assert result['role'] == 'admin'

    def test_authenticate_user_failure(self):
        """Prueba de autenticación fallida."""
        auth = AuthManager()
        result = auth.authenticate_user('admin', 'wrong_password')

        assert result is None

    def test_create_verify_jwt_token(self):
        """Prueba de creación y verificación de token JWT."""
        auth = AuthManager()
        user_info = {
            'username': 'test_user',
            'role': 'user',
            'login_time': '2024-01-01T00:00:00'
        }

        token = auth.create_jwt_token(user_info)
        assert token is not None

        decoded = auth.verify_jwt_token(token)
        assert decoded is not None
        assert decoded['username'] == 'test_user'
        assert decoded['role'] == 'user'

    def test_verify_invalid_jwt_token(self):
        """Prueba de verificación de token JWT inválido."""
        auth = AuthManager()
        result = auth.verify_jwt_token('invalid_token')
        assert result is None


class TestIntegration:
    """Pruebas de integración."""

    def test_full_security_workflow(self):
        """Prueba del flujo completo de seguridad."""
        # 1. Configurar master key
        master_key = "integration_test_key"
        config = SecureConfig(master_key=master_key)

        # 2. Encriptar API keys
        gemini_key = "sk-gemini-integration123"
        tavily_key = "tv-tavily-integration123"

        encrypted_gemini = config.encrypt_value(gemini_key)
        encrypted_tavily = config.encrypt_value(tavily_key)

        # 3. Simular variables de entorno
        with patch.dict(os.environ, {
            'SOFIA_MASTER_KEY': master_key,
            'GEMINI_API_KEY_ENCRYPTED': encrypted_gemini,
            'TAVILY_API_KEY_ENCRYPTED': encrypted_tavily
        }):
            # 4. Verificar que se pueden obtener las keys
            retrieved_gemini = get_gemini_api_key()
            retrieved_tavily = get_tavily_api_key()

            assert retrieved_gemini == gemini_key
            assert retrieved_tavily == tavily_key

            # 5. Verificar validación de configuración
            assert validate_configuration() is True

    @patch('streamlit.session_state')
    def test_authentication_workflow(self, mock_session_state):
        """Prueba del flujo de autenticación."""
        # Mock session state
        mock_session_state.get.return_value = None
        mock_session_state.__contains__ = MagicMock(return_value=False)

        auth = AuthManager()

        # Autenticar usuario
        user_info = auth.authenticate_user('admin', 'admin123')
        assert user_info is not None

        # Crear token
        token = auth.create_jwt_token(user_info)
        assert token is not None

        # Verificar token
        decoded = auth.verify_jwt_token(token)
        assert decoded is not None
        assert decoded['username'] == 'admin'