# crypto_utils.py

import os
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import hashes

# Размер блока для SM4 (128 бит = 16 байт)
SM4_BLOCK_SIZE = 16


def load_private_key(path):
    """Загружает приватный ключ RSA из файла PEM."""
    print(f"[*] Загрузка приватного ключа из {path}...")
    try:
        with open(path, 'rb') as f:
            private_key = load_pem_private_key(f.read(), password=None)
        print("[+] Приватный ключ загружен.")
        return private_key
    except FileNotFoundError:
        print(f"[!] Ошибка: Файл приватного ключа не найден по пути {path}")
        exit(1)
    except Exception as e:
        print(f"[!] Ошибка загрузки приватного ключа: {e}")
        exit(1)


def load_public_key(path):
    """Загружает публичный ключ RSA из файла PEM."""
    print(f"[*] Загрузка публичного ключа из {path}...")
    try:
        with open(path, 'rb') as f:
            public_key = load_pem_public_key(f.read())
        print("[+] Публичный ключ загружен.")
        return public_key
    except FileNotFoundError:
        print(f"[!] Ошибка: Файл публичного ключа не найден по пути {path}")
        exit(1)
    except Exception as e:
        print(f"[!] Ошибка загрузки публичного ключа: {e}")
        exit(1)


def decrypt_symmetric_key(private_key, encrypted_ciphertext):
    """Расшифровывает симметричный ключ с использованием приватного RSA ключа."""
    print("[*] Расшифровка симметричного ключа...")
    try:
        # Используем OAEP padding, как при шифровании
        symmetric_key = private_key.decrypt(
            encrypted_ciphertext,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("[+] Симметричный ключ успешно расшифрован.")
        return symmetric_key
    except Exception as e:
        print(f"[!] Ошибка расшифровки симметричного ключа RSA: {e}")
        exit(1)


def pad_data(data):
    """Добавляет паддинг ANSI X9.23 к данным до кратности размеру блока SM4."""
    # Паддинг ANSI X9.23, размер блока SM4 = 16 байт
    padder = sym_padding.ANSIX923(SM4_BLOCK_SIZE).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(padded_data):
    """Удаляет паддинг ANSI X9.23 из данных."""
    unpadder = sym_padding.ANSIX923(SM4_BLOCK_SIZE).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


def save_file(path, data):
    """Сохраняет байтовые данные в файл."""
    print(f"[*] Сохранение данных в {path}...")
    try:
        with open(path, 'wb') as f:
            f.write(data)
        print(f"[+] Данные успешно сохранены в {path}.")
    except Exception as e:
        print(f"[!] Ошибка сохранения файла {path}: {e}")
        exit(1)


def read_file(path):
    """Читает байтовые данные из файла."""
    print(f"[*] Чтение данных из {path}...")
    try:
        with open(path, 'rb') as f:
            data = f.read()
        print(f"[+] Данные успешно прочитаны из {path}.")
        return data
    except FileNotFoundError:
        print(f"[!] Ошибка: Файл не найден по пути {path}")
        exit(1)
    except Exception as e:
        print(f"[!] Ошибка чтения файла {path}: {e}")
        exit(1)
