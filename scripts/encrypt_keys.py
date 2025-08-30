#!/usr/bin/env python3
"""
Script para encriptar API keys de forma segura para SOF-IA.
Uso: python encrypt_keys.py
"""
import os
import sys
import base64
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_master_key():
    """Generar una nueva master key."""
    return base64.urlsafe_b64encode(os.urandom(32)).decode()

def create_cipher(master_key: str):
    """Crear cipher para encriptación."""
    salt = b'sofia_salt_2024'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    return Fernet(key)

def encrypt_value(cipher: Fernet, value: str) -> str:
    """Encriptar un valor."""
    if not value:
        return ""
    encrypted = cipher.encrypt(value.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def main():
    print("🔐 SOF-IA - Encriptador de API Keys")
    print("=" * 50)

    # Generar o usar master key existente
    master_key = os.getenv('SOFIA_MASTER_KEY')
    if not master_key:
        print("No se encontró SOFIA_MASTER_KEY en variables de entorno.")
        generate_new = input("¿Generar una nueva master key? (y/n): ").lower().strip()
        if generate_new == 'y':
            master_key = generate_master_key()
            print(f"\n✅ Nueva master key generada:")
            print(f"SOFIA_MASTER_KEY={master_key}")
            print("\n⚠️  GUARDE ESTA CLAVE DE FORMA SEGURA!")
            print("⚠️  Sin ella NO podrá desencriptar las claves!")
            input("\nPresione Enter cuando haya guardado la clave...")
        else:
            master_key = getpass("Ingrese su master key existente: ")

    # Crear cipher
    try:
        cipher = create_cipher(master_key)
        print("\n✅ Master key validada correctamente")
    except Exception as e:
        print(f"❌ Error con la master key: {e}")
        sys.exit(1)

    # Encriptar API keys
    print("\n🔑 Encriptando API Keys...")
    print("Deje en blanco para omitir")

    # Gemini API Key
    gemini_key = getpass("Gemini API Key: ").strip()
    if gemini_key:
        encrypted_gemini = encrypt_value(cipher, gemini_key)
        print(f"\nGEMINI_API_KEY_ENCRYPTED={encrypted_gemini}")

    # Tavily API Key
    tavily_key = getpass("Tavily API Key: ").strip()
    if tavily_key:
        encrypted_tavily = encrypt_value(cipher, tavily_key)
        print(f"\nTAVILY_API_KEY_ENCRYPTED={encrypted_tavily}")

    # JWT Secret
    jwt_secret = getpass("JWT Secret (opcional): ").strip()
    if jwt_secret:
        encrypted_jwt = encrypt_value(cipher, jwt_secret)
        print(f"\nJWT_SECRET_ENCRYPTED={encrypted_jwt}")

    print("\n✅ Encriptación completada!")
    print("\n📝 Agregue estas variables a su archivo .env:")
    print("SOFIA_MASTER_KEY=your_master_key_here")
    print("# Y las variables encriptadas generadas arriba")

    print("\n🔒 Recuerde:")
    print("- Nunca comparta la master key")
    print("- Mantenga el .env fuera del control de versiones")
    print("- Use las variables encriptadas en producción")

if __name__ == "__main__":
    main()