# asymmetric_encryption.py

from cryptography.hazmat.primitives.asymmetric import rsa, \
    padding as rsa_padding  # Импортируем padding под псевдонимом rsa_padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from file_manager import FileManager
import config


class AsymmetricCipher:
    """Класс для операций асимметричного шифрования RSA (OAEP)."""

    @staticmethod
    def generate_keys(settings: dict) -> tuple[RSAPrivateKey, RSAPublicKey]:
        """Генерирует пару RSA ключей (размер из config) и сохраняет их в PEM файлы."""
        print(f"[*] Генерация пары RSA ключей (размер {config.RSA_KEY_SIZE} бит)...")
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,  # Рекомендованное публичное экспонента
                key_size=config.RSA_KEY_SIZE
            )
            public_key = private_key.public_key()
            print("[+] Пара RSA ключей сгенерирована.")

            # Сериализация и сохранение приватного ключа в формате PEM
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()  # Не шифруем приватный ключ паролем
            )
            FileManager.save_file(settings['secret_key'], private_pem)

            # Сериализация и сохранение публичного ключа в формате PEM
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            FileManager.save_file(settings['public_key'], public_pem)

            print("[+] Пара RSA ключей сериализована и сохранена.")
            return private_key, public_key
        except Exception as e:
            print(f"[!] Ошибка при генерации или сохранении RSA ключей: {e}")
            raise

    @staticmethod
    def load_private_key(path: str) -> RSAPrivateKey:
        """Загружает приватный ключ RSA из файла PEM."""
        print(f"[*] Загрузка приватного ключа из {path}...")
        try:
            private_bytes = FileManager.read_file(path)
            private_key = serialization.load_pem_private_key(private_bytes, password=None)
            print("[+] Приватный ключ загружен.")
            return private_key
        except Exception as e:
            print(f"[!] Ошибка загрузки приватного ключа: {e}")
            raise

    @staticmethod
    def load_public_key(path: str) -> RSAPublicKey:
        """Загружает публичный ключ RSA из файла PEM."""
        print(f"[*] Загрузка публичного ключа из {path}...")
        try:
            public_bytes = FileManager.read_file(path)
            public_key = serialization.load_pem_public_key(public_bytes)
            print("[+] Публичный ключ загружен.")
            return public_key
        except Exception as e:
            print(f"[!] Ошибка загрузки публичного ключа: {e}")
            raise

    @staticmethod
    def encrypt_sym_key(public_key: RSAPublicKey, symmetric_key: bytes) -> bytes:
        """Шифрует симметричный ключ публичным RSA ключом (OAEP padding)."""
        print("[*] Шифрование симметричного ключа публичным RSA ключом (OAEP)...")
        try:
            # Использование OAEP padding (рекомендовано для RSA шифрования данных)
            encrypted_key = public_key.encrypt(
                symmetric_key,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),  # <-- ИСПРАВЛЕНО: padding.MGF1 -> rsa_padding.MGF1
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print("[+] Симметричный ключ зашифрован.")
            return encrypted_key
        except Exception as e:
            print(f"[!] Ошибка при шифровании симметричного ключа RSA: {e}")
            raise

    @staticmethod
    def decrypt_sym_key(private_key: RSAPrivateKey, encrypted_ciphertext: bytes) -> bytes:
        """Расшифровывает симметричный ключ приватным RSA ключом (OAEP padding)."""
        print("[*] Расшифровка зашифрованного симметричного ключа приватным RSA ключом (OAEP)...")
        try:
            # Использование OAEP padding (должен соответствовать используемому при шифровании)
            symmetric_key = private_key.decrypt(
                encrypted_ciphertext,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),  # <-- ИСПРАВЛЕНО: padding.MGF1 -> rsa_padding.MGF1
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print("[+] Симметричный ключ расшифрован.")
            return symmetric_key
        except Exception as e:
            print(f"[!] Ошибка расшифровки симметричного ключа RSA: {e}")
            raise
