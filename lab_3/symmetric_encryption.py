import os
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import config


class SymmetricCipher:
    """
    Класс для операций симметричного шифрования с использованием SM4 (CBC режим).
    GMSSL CryptSM4.crypt_cbc сам выполняет паддинг и анпаддинг.
    """

    @staticmethod
    def generate_key() -> bytes:
        """Генерирует случайный симметричный ключ для SM4 (128 бит)."""
        print(f"[*] Генерация симметричного ключа SM4 ({config.SM4_KEY_SIZE * 8} бит)...")
        sym_key = os.urandom(config.SM4_KEY_SIZE)
        print("[+] Симметричный ключ сгенерирован.")
        return sym_key

    @staticmethod
    def encrypt(key: bytes, data: bytes) -> bytes:
        """
        Шифрует данные симметричным алгоритмом SM4 в режиме CBC.
        Возвращает IV, сцепленный с шифротекстом.
        GMSSL crypt_cbc добавляет паддинг.
        """
        print("[*] Шифрование данных SM4 (CBC)...")

        if len(key) != config.SM4_KEY_SIZE:
            raise ValueError(
                f"Некорректный размер ключа SM4. Ожидается {config.SM4_KEY_SIZE} байт, получено {len(key)}.")

        print(f"[*] Исходный размер данных для шифрования: {len(data)} байт.")

        # Генерируем случайный IV
        iv = os.urandom(config.SM4_BLOCK_SIZE)
        print(f"[+] IV сгенерирован: {iv.hex()}")

        cipher = CryptSM4()
        cipher.set_key(key, SM4_ENCRYPT)

        # Шифрование с добавлением паддинга от GMSSL
        ciphertext = cipher.crypt_cbc(iv, data)

        print(f"[+] Данные зашифрованы. Размер шифротекста: {len(ciphertext)} байт.")

        # Возвращаем IV + шифротекст
        return iv + ciphertext

    @staticmethod
    def decrypt(key: bytes, encrypted_data: bytes) -> bytes:
        """
        Дешифрует данные симметричным алгоритмом SM4 в режиме CBC.
        Входные данные содержат IV (первые SM4_BLOCK_SIZE байт), за которым следует шифротекст.
        Возвращает дешифрованные данные без паддинга.
        GMSSL crypt_cbc удаляет паддинг.
        """
        print("[*] Дешифрование данных SM4 (CBC)...")

        if len(key) != config.SM4_KEY_SIZE:
            raise ValueError(
                f"Некорректный размер ключа SM4. Ожидается {config.SM4_KEY_SIZE} байт, получено {len(key)}.")

        # Извлекаем IV и шифротекст
        if len(encrypted_data) < config.SM4_BLOCK_SIZE:
            raise ValueError(
                f"Некорректный формат зашифрованных данных: слишком короткие (меньше размера блока IV). Размер: {len(encrypted_data)}, ожидается >= {config.SM4_BLOCK_SIZE}")

        iv = encrypted_data[:config.SM4_BLOCK_SIZE]
        ciphertext = encrypted_data[config.SM4_BLOCK_SIZE:]
        print(f"[+] Извлечен IV: {iv.hex()}")
        print(f"[*] Размер шифротекста: {len(ciphertext)} байт.")

        # Проверка кратности размера шифротекста блоку для CBC
        if len(ciphertext) % config.SM4_BLOCK_SIZE != 0:
            raise ValueError(
                f"Размер шифротекста ({len(ciphertext)}) не кратен размеру блока SM4 ({config.SM4_BLOCK_SIZE}).")

        cipher = CryptSM4()
        cipher.set_key(key, SM4_DECRYPT)

        # Дешифрование с удалением паддинга от GMSSL
        plain_data = cipher.crypt_cbc(iv, ciphertext)

        print("[+] Данные дешифрованы.")
        return plain_data
