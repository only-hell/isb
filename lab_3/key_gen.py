# key_gen.py

import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import serialization, hashes
from crypto_utils import save_file  # Используем общую функцию сохранения


# Генерация симметричного ключа SM4 (128 бит)
def generate_symmetric_key():
    """Генерирует случайный симметричный ключ для SM4 (128 бит)."""
    print("[*] Генерация симметричного ключа SM4 (128 бит)...")
    # SM4 использует 128-битный ключ (16 байт)
    sym_key = os.urandom(16)
    print("[+] Симметричный ключ сгенерирован.")
    # Не сохраняем незашифрованный ключ на диск!
    return sym_key


# Генерация пары RSA-ключей
def generate_rsa_keys(settings):
    """Генерирует пару RSA ключей и сохраняет их в PEM файлы."""
    print("[*] Генерация пары RSA ключей (размер 2048 бит)...")
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,  # Рекомендованное публичное экспонента
            key_size=2048  # Размер ключа в битах
        )
        public_key = private_key.public_key()

        # Сохранение приватного ключа
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # Не шифруем приватный ключ паролем для простоты лабы
        )
        save_file(settings['secret_key'], private_pem)
        print(f"[+] Приватный ключ сохранен в {settings['secret_key']}.")

        # Сохранение публичного ключа
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        save_file(settings['public_key'], public_pem)
        print(f"[+] Публичный ключ сохранен в {settings['public_key']}.")

        print("[+] Пара RSA ключей сгенерирована и сохранена.")
        return private_key, public_key
    except Exception as e:
        print(f"[!] Ошибка при генерации или сохранении RSA ключей: {e}")
        exit(1)


# Шифрование симметричного ключа с использованием публичного RSA-ключа
def encrypt_symmetric_key(public_key, symmetric_key, output_path):
    """Шифрует симметричный ключ с использованием публичного RSA ключа и сохраняет его."""
    print(f"[*] Шифрование симметричного ключа с использованием публичного RSA ключа и сохранение в {output_path}...")
    try:
        # Используем OAEP padding для шифрования ключа RSA
        encrypted_key = public_key.encrypt(
            symmetric_key,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None  # Опциональная метка
            )
        )
        save_file(output_path, encrypted_key)
        print(f"[+] Зашифрованный симметричный ключ сохранен в {output_path}.")
    except Exception as e:
        print(f"[!] Ошибка при шифровании или сохранении симметричного ключа: {e}")
        exit(1)


# Основная функция для вызова всех шагов генерации
def generate_keys(settings):
    """Выполняет все шаги генерации ключей гибридной системы."""
    print("\n===== Режим: Генерация ключей =====")

    # 1.1. Сгенерировать ключ для симметричного алгоритма.
    sym_key = generate_symmetric_key()

    # 1.2. Сгенерировать ключи для ассиметричного алгоритма.
    # 1.3. Сериализовать ассиметричные ключи.
    # Пути для сохранения берутся из settings
    private_key, public_key = generate_rsa_keys(settings)

    # 1.4. Зашифровать ключ симметричного шифрования открытым ключом
    # и сохранить по указанному пути (путь из settings['encrypted_symmetric_key_file'])
    # Проверяем, что путь для зашифрованного симметричного ключа указан в settings
    encrypted_sym_key_path = settings.get('encrypted_symmetric_key_file')  # Используем новое имя ключа
    if not encrypted_sym_key_path:
        # Или используем старое имя ключа, если решили не переименовывать в JSON
        encrypted_sym_key_path = settings.get('symmetric_key')
        if not encrypted_sym_key_path:
            print("[!] Ошибка: Не указан путь для сохранения зашифрованного симметричного ключа в настройках.")
            exit(1)

    encrypt_symmetric_key(public_key, sym_key, encrypted_sym_key_path)

    print("===== Генерация ключей завершена успешно! =====")
