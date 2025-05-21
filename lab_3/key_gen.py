from symmetric_encryption import SymmetricCipher
from asymmetric_encryption import AsymmetricCipher
from file_manager import FileManager
from utils import Utils


def generate_keys(settings: dict):
    """
    Выполняет генерацию ключей гибридной системы:
    1. Генерирует симметричный ключ (SM4).
    2. Генерирует RSA ключи и сохраняет их.
    3. Зашифровывает симметричный ключ публичным RSA ключом и сохраняет.
    """
    Utils.print_status("\n===== Режим: Генерация ключей =====")

    try:
        # Генерируем ключ SM4
        sym_key = SymmetricCipher.generate_key()

        # Генерируем и сохраняем RSA ключи
        private_key, public_key = AsymmetricCipher.generate_keys(settings)

        # Шифруем симметричный ключ публичным RSA ключом и сохраняем
        encrypted_sym_key_path = settings.get('encrypted_symmetric_key_file')
        if not encrypted_sym_key_path:
            Utils.print_error(
                "Не указан путь для сохранения зашифрованного симметричного ключа в настройках.")
            return

        encrypted_sym_key_data = AsymmetricCipher.encrypt_sym_key(public_key, sym_key)
        FileManager.save_file(encrypted_sym_key_path, encrypted_sym_key_data)

        Utils.print_success("===== Генерация ключей завершена успешно! =====")

    except Exception as e:
        # Перехвачены ошибки из File/Crypto методов (которые уже вывели детальное сообщение)
        Utils.print_error(f"Произошла ошибка в процессе генерации ключей: {e}")
