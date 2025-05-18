# encrypt.py

from crypto_utils import load_private_key, decrypt_symmetric_key, pad_data, save_file, read_file, SM4_BLOCK_SIZE
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT
import os


def hybrid_encrypt(settings):
    """Выполняет гибридное шифрование файла."""
    print("\n===== Режим: Шифрование данных =====")

    # Пути для чтения/записи из настроек
    initial_file_path = settings.get('initial_file')
    private_key_path = settings.get('secret_key')
    # Используем новое имя ключа для зашифрованного симметричного ключа
    encrypted_sym_key_path = settings.get('encrypted_symmetric_key_file')
    if not encrypted_sym_key_path:
        # Или старое имя ключа, если не переименовывали в JSON
        encrypted_sym_key_path = settings.get('symmetric_key')

    encrypted_file_path = settings.get('encrypted_file')

    # Проверка наличия необходимых файлов
    if not all([initial_file_path, private_key_path, encrypted_sym_key_path, encrypted_file_path]):
        print("[!] Ошибка: Не указаны все необходимые пути в настройках для шифрования.")
        exit(1)
    if not os.path.exists(initial_file_path):
        print(f"[!] Ошибка: Исходный файл не найден по пути {initial_file_path}")
        exit(1)
    if not os.path.exists(private_key_path):
        print(f"[!] Ошибка: Файл приватного ключа не найден по пути {private_key_path}")
        exit(1)
    if not os.path.exists(encrypted_sym_key_path):
        print(f"[!] Ошибка: Файл зашифрованного симметричного ключа не найден по пути {encrypted_sym_key_path}")
        exit(1)

    # 2.1. Расшифровать симметричный ключ.
    private_key = load_private_key(private_key_path)
    encrypted_sym_key_data = read_file(encrypted_sym_key_path)
    sym_key = decrypt_symmetric_key(private_key, encrypted_sym_key_data)

    # 2.2. Зашифровать текст симметричным алгоритмом и сохранить по указанному пути.
    print(f"[*] Чтение исходного файла {initial_file_path}...")
    data = read_file(initial_file_path)

    print("[*] Добавление паддинга к данным...")
    padded_data = pad_data(data)
    print(f"[+] Данные дополнены паддингом. Исходный размер: {len(data)}, после паддинга: {len(padded_data)}.")

    print("[*] Генерация IV (Initial Vector) для CBC режима...")
    iv = os.urandom(SM4_BLOCK_SIZE)  # IV должен быть случайным и иметь размер блока
    print(f"[+] IV сгенерирован: {iv.hex()}")

    print("[*] Инициализация шифра SM4 в режиме CBC...")
    cipher = CryptSM4()
    cipher.set_key(sym_key, SM4_ENCRYPT)

    print("[*] Шифрование данных симметричным алгоритмом SM4...")
    # Примечание: gmssl.sm4.CryptSM4.crypt_cbc шифрует данные целиком
    # Для очень больших файлов этот подход может быть неоптимальным по памяти.
    # Потоковое шифрование с gmssl требует более сложного управления IV.
    ciphertext = cipher.crypt_cbc(iv, padded_data)
    print("[+] Данные зашифрованы.")

    # Сохраняем IV вместе с шифротекстом, IV всегда идет первыми 16 байтами
    print(f"[*] Сохранение IV и зашифрованных данных в {encrypted_file_path}...")
    save_file(encrypted_file_path, iv + ciphertext)

    print("===== Шифрование завершено успешно! =====")
