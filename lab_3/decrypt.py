from asymmetric_encryption import AsymmetricCipher
from symmetric_encryption import SymmetricCipher
from file_manager import FileManager
from utils import Utils


def hybrid_decrypt(settings: dict):
    """Выполняет гибридное дешифрование файла."""
    Utils.print_status("\n===== Режим: Дешифрование данных =====")

    try:
        # Получение путей из настроек
        encrypted_file_path = settings.get('encrypted_file')
        private_key_path = settings.get('secret_key')
        encrypted_sym_key_path = settings.get('encrypted_symmetric_key_file')
        decrypted_file_path = settings.get('decrypted_file')

        # Проверка наличия всех путей
        if not all([encrypted_file_path, private_key_path, encrypted_sym_key_path, decrypted_file_path]):
            Utils.print_error("Не указаны все необходимые пути в настройках для дешифрования.")
            return

        # Проверка существования входных файлов
        if not FileManager.read_file(encrypted_file_path): return
        if not FileManager.read_file(private_key_path): return
        if not FileManager.read_file(encrypted_sym_key_path): return

        # Расшифровка симметричного ключа с помощью приватного RSA ключа
        encrypted_sym_key_data = FileManager.read_file(encrypted_sym_key_path)
        if not encrypted_sym_key_data: return

        private_key = AsymmetricCipher.load_private_key(private_key_path)
        if not private_key: return

        sym_key = AsymmetricCipher.decrypt_sym_key(private_key, encrypted_sym_key_data)
        if not sym_key: return

        # Дешифровка файла симметричным ключом SM4 (CBC)
        encrypted_data_with_iv = FileManager.read_file(encrypted_file_path)
        if not encrypted_data_with_iv: return

        plain_data = SymmetricCipher.decrypt(sym_key, encrypted_data_with_iv)
        if plain_data is None: return

        # Сохранение расшифрованных данных
        FileManager.save_file(decrypted_file_path, plain_data)

        Utils.print_success("===== Дешифрование завершено успешно! =====")

    except Exception as e:
        # Перехвачены ошибки из File/Crypto методов (которые уже вывели детальное сообщение)
        Utils.print_error(f"Произошла ошибка в процессе дешифрования: {e}")
