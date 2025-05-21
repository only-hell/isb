from asymmetric_encryption import AsymmetricCipher
from symmetric_encryption import SymmetricCipher
from file_manager import FileManager
from utils import Utils


def hybrid_encrypt(settings: dict):
    """Выполняет гибридное шифрование файла."""
    Utils.print_status("\n===== Режим: Шифрование данных =====")

    try:
        # Получение путей из настроек
        initial_file_path = settings.get('initial_file')
        private_key_path = settings.get('secret_key')
        encrypted_sym_key_path = settings.get('encrypted_symmetric_key_file')
        encrypted_file_path = settings.get('encrypted_file')

        # Проверка наличия всех путей
        if not all([initial_file_path, private_key_path, encrypted_sym_key_path, encrypted_file_path]):
            Utils.print_error("Не указаны все необходимые пути в настройках для шифрования.")
            return

        # Проверка существования входных файлов
        if not FileManager.read_file(initial_file_path): return
        if not FileManager.read_file(private_key_path): return
        if not FileManager.read_file(encrypted_sym_key_path): return

        # Расшифровка симметричного ключа с помощью приватного RSA ключа
        encrypted_sym_key_data = FileManager.read_file(encrypted_sym_key_path)
        if not encrypted_sym_key_data: return

        private_key = AsymmetricCipher.load_private_key(private_key_path)
        if not private_key: return

        sym_key = AsymmetricCipher.decrypt_sym_key(private_key, encrypted_sym_key_data)
        if not sym_key: return

        # Шифрование файла симметричным ключом SM4 (CBC)
        data = FileManager.read_file(initial_file_path)
        if not data: return

        encrypted_data_with_iv = SymmetricCipher.encrypt(sym_key, data)
        if not encrypted_data_with_iv: return  # encrypt печатает ошибку при необходимости

        # Сохранение зашифрованных данных (IV + шифротекст)
        FileManager.save_file(encrypted_file_path, encrypted_data_with_iv)

        Utils.print_success("===== Шифрование завершено успешно! =====")

    except Exception as e:
        # Перехвачены ошибки из File/Crypto методов (которые уже вывели детальное сообщение)
        Utils.print_error(f"Произошла ошибка в процессе шифрования: {e}")
