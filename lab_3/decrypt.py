# decrypt.py

from crypto_utils import load_private_key, decrypt_symmetric_key, unpad_data, save_file, read_file, SM4_BLOCK_SIZE
from gmssl.sm4 import CryptSM4, SM4_DECRYPT
import os  # Импорт os не нужен, убран


def hybrid_decrypt(settings):
    """Выполняет гибридное дешифрование файла."""
    print("\n===== Режим: Дешифрование данных =====")

    # Пути для чтения/записи из настроек
    encrypted_file_path = settings.get('encrypted_file')
    private_key_path = settings.get('secret_key')
    # Используем новое имя ключа для зашифрованного симметричного ключа
    encrypted_sym_key_path = settings.get('encrypted_symmetric_key_file')
    if not encrypted_sym_key_path:
        # Или старое имя ключа, если не переименовывали в JSON
        encrypted_sym_key_path = settings.get('symmetric_key')
    decrypted_file_path = settings.get('decrypted_file')

    # Проверка наличия необходимых файлов
    if not all([encrypted_file_path, private_key_path, encrypted_sym_key_path, decrypted_file_path]):
        print("[!] Ошибка: Не указаны все необходимые пути в настройках для дешифрования.")
        exit(1)
    if not os.path.exists(encrypted_file_path):
        print(f"[!] Ошибка: Зашифрованный файл не найден по пути {encrypted_file_path}")
        exit(1)
    if not os.path.exists(private_key_path):
        print(f"[!] Ошибка: Файл приватного ключа не найден по пути {private_key_path}")
        exit(1)
    if not os.path.exists(encrypted_sym_key_path):
        print(f"[!] Ошибка: Файл зашифрованного симметричного ключа не найден по пути {encrypted_sym_key_path}")
        exit(1)

    # 3.1. Расшифровать симметричный ключ.
    private_key = load_private_key(private_key_path)
    encrypted_sym_key_data = read_file(encrypted_sym_key_path)
    sym_key = decrypt_symmetric_key(private_key, encrypted_sym_key_data)

    # 3.2. Расшифровать текст симметричным алгоритмом и сохранить по указанному пути.
    print(f"[*] Чтение зашифрованного файла {encrypted_file_path}...")
    encrypted_data = read_file(encrypted_file_path)

    # Извлекаем IV (первые 16 байт) и шифротекст
    if len(encrypted_data) < SM4_BLOCK_SIZE:
        print("[!] Ошибка: Зашифрованный файл слишком короткий (меньше размера блока IV).")
        exit(1)
    iv = encrypted_data[:SM4_BLOCK_SIZE]
    ciphertext = encrypted_data[SM4_BLOCK_SIZE:]
    print(f"[+] Извлечен IV: {iv.hex()}")
    print(f"[*] Размер шифротекста: {len(ciphertext)} байт.")

    # Шифротекст должен быть кратен размеру блока для CBC режима перед анпаддингом
    if len(ciphertext) % SM4_BLOCK_SIZE != 0:
        print(
            f"[!] Ошибка: Размер шифротекста ({len(ciphertext)}) не кратен размеру блока SM4 ({SM4_BLOCK_SIZE}). Возможно, файл поврежден.")
        exit(1)

    print("[*] Инициализация дешифратора SM4 в режиме CBC...")
    cipher = CryptSM4()
    cipher.set_key(sym_key, SM4_DECRYPT)

    print("[*] Дешифрование данных симметричным алгоритмом SM4...")
    # Примечание: gmssl.sm4.CryptSM4.crypt_cbc дешифрует данные целиком
    padded_plain = cipher.crypt_cbc(iv, ciphertext)
    print("[+] Данные дешифрованы.")

    print("[*] Удаление паддинга из дешифрованных данных...")
    try:
        plain = unpad_data(padded_plain)
        print("[+] Паддинг успешно удален.")
    except ValueError as e:
        print(f"[!] Ошибка при удалении паддинга. Данные, возможно, повреждены или ключ неверен: {e}")
        exit(1)

    print(f"[*] Сохранение расшифрованных данных в {decrypted_file_path}...")
    save_file(decrypted_file_path, plain)

    print("===== Дешифрование завершено успешно! =====")
