"""
Configuración segura para SOF-IA con encriptación de claves sensibles.
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional
import logging

# Configurar logging seguro
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sofia_secure.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecureConfig:
    """Gestor de configuración segura con encriptación."""

    def __init__(self, master_key: Optional[str] = None):
        self.master_key = master_key or os.getenv('SOFIA_MASTER_KEY')
        if not self.master_key:
            logger.warning("No se encontro SOFIA_MASTER_KEY. Generando una nueva...")
            self.master_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            logger.info("Nueva master key generada. Guardela de forma segura.")

        self._cipher = self._create_cipher()

    def _create_cipher(self) -> Fernet:
        """Crear cipher para encriptación."""
        # Derivar clave usando PBKDF2
        salt = b'sofia_salt_2024'  # En producción, usar salt aleatorio
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
        return Fernet(key)

    def encrypt_value(self, value: str) -> str:
        """Encriptar un valor sensible."""
        if not value:
            return ""
        encrypted = self._cipher.encrypt(value.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt_value(self, encrypted_value: str) -> str:
        """Desencriptar un valor."""
        if not encrypted_value:
            return ""
        try:
            encrypted = base64.urlsafe_b64decode(encrypted_value.encode())
            decrypted = self._cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Error desencriptando valor: {e}")
            return ""

    def get_encrypted_env_var(self, key: str, default: str = "") -> str:
        """Obtener variable de entorno encriptada."""
        encrypted_value = os.getenv(key)
        if encrypted_value:
            return self.decrypt_value(encrypted_value)
        return default

    def get_secure_api_key(self, service: str) -> str:
        """Obtener API key de forma segura."""
        env_key = f"{service.upper()}_API_KEY"
        encrypted_key = f"{service.upper()}_API_KEY_ENCRYPTED"

        # Primero intentar variable encriptada
        api_key = self.get_encrypted_env_var(encrypted_key)
        if api_key:
            logger.info(f"API key para {service} cargada desde variable encriptada")
            return api_key

        # Fallback a variable no encriptada (para migración)
        api_key = os.getenv(env_key)
        if api_key:
            logger.warning(f"API key para {service} cargada sin encriptación. Considere encriptarla.")
            return api_key

        logger.error(f"No se encontró API key para {service}")
        return ""

# Instancia global de configuración segura
secure_config = SecureConfig()

# Funciones de conveniencia
def get_gemini_api_key() -> str:
    """Obtener API key de Gemini de forma segura."""
    return secure_config.get_secure_api_key('gemini') or secure_config.get_secure_api_key('google')

def get_tavily_api_key() -> str:
    """Obtener API key de Tavily de forma segura."""
    return secure_config.get_secure_api_key('tavily')

def get_master_key() -> str:
    """Obtener la master key (solo para debugging)."""
    return secure_config.master_key

# Validación de configuración
def validate_configuration() -> bool:
    """Validar que la configuración sea segura."""
    issues = []

    if not secure_config.master_key:
        issues.append("SOFIA_MASTER_KEY no configurada")

    gemini_key = get_gemini_api_key()
    if not gemini_key:
        issues.append("GEMINI_API_KEY no encontrada")

    tavily_key = get_tavily_api_key()
    if not tavily_key:
        issues.append("TAVILY_API_KEY no encontrada")

    if issues:
        for issue in issues:
            logger.error(f"Problema de configuración: {issue}")
        return False

    logger.info("Configuración validada correctamente")
    return True