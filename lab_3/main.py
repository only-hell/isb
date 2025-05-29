import argparse
import config

from key_gen import generate_keys
from hybrid_cipher import HybridCipher
from utils import Utils
from file_manager import FileManager
from symmetric_encryption import SymmetricCipher
from asymmetric_encryption import AsymmetricCipher


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема: генерация ключей, шифрование, дешифрование.")

    # Режимы работы: gen (все ключи), enc, dec(по отдельности), gen-sym, gen-rsa, encrypt-sym-key-rsa
    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument('-gen', '--generation', nargs='?', const='settings.json', help='Режим генерации ВСЕХ ключей.')
    group.add_argument('-enc', '--encryption', nargs='?', const='settings.json', help='Режим шифрования данных .')
    group.add_argument('-dec', '--decryption', nargs='?', const='settings.json', help='Режим дешифрования данных .')
    group.add_argument('-gen-sym', '--generate-symmetric-key', type=str, metavar='SYMMETRIC_KEY_PATH',
                       help='Генерирует только симметричный ключ SM4 и сохраняет его в указанный файл.')
    group.add_rsa_keys_arg = group.add_argument('-gen-rsa', '--generate-rsa-keys', type=str, nargs=2,
                                                metavar=('PUBLIC_KEY_PATH', 'PRIVATE_KEY_PATH'),
                                                help='Генерирует пару RSA ключей и сохраняет их в указанные файлы.')
    group.add_argument('--encrypt-sym-key-rsa', type=str, nargs=3,
                       metavar=('UNENCRYPTED_SM4_PATH', 'RSA_PUBLIC_KEY_PATH', 'OUTPUT_ENCRYPTED_SM4_PATH'),
                       help='Шифрует НЕЗАШИФРОВАННЫЙ симметричный ключ SM4 ПУБЛИЧНЫМ RSA ключом и сохраняет ЗАШИФРОВАННЫЙ симметричный ключ .')

    parser.add_argument('-ctf', '--create-test-file', type=str, nargs='+', help='Создает тестовый файл.')
    args = parser.parse_args()

    # Обработка создания тестового файла
    if args.create_test_file:
        file_path = args.create_test_file[0]
        size_mb = 1

        if len(args.create_test_file) > 1:
            try:
                size_mb = int(args.create_test_file[1])
                if size_mb <= 0:
                    raise ValueError("Размер должен быть положительным числом.")
            except ValueError:
                Utils.print_error(
                    f"Неверный формат или значение размера файла: {args.create_test_file[1]}. Размер должен быть положительным целым числом (в MB).")
                return

        try:
            FileManager.create_test_file(file_path, size_mb)
        except Exception:
            pass
        return

    selected_mode = None
    json_path = None
    if args.generation is not None:
        selected_mode = 'gen'
        json_path = args.generation
    elif args.encryption is not None:
        selected_mode = 'enc'
        json_path = args.encryption
    elif args.decryption is not None:
        selected_mode = 'dec'
        json_path = args.decryption
    elif args.generate_symmetric_key is not None:
        selected_mode = 'gen-sym'
    elif args.generate_rsa_keys is not None:
        selected_mode = 'gen-rsa'
    elif args.encrypt_sym_key_rsa is not None:
        selected_mode = 'encrypt-sym-key-rsa'

    if selected_mode is None:
        parser.error(
            "Выберите один из режимов: -gen, -enc, -dec, -gen-sym, -gen-rsa, --encrypt-sym-key-rsa.")
    settings = {}
    if selected_mode in ['gen', 'enc', 'dec']:
        try:
            settings = Utils.load_settings(json_path)
        except Exception as e:
            Utils.print_error(f"Не удалось загрузить настройки: {e}")
            return

    # Запускаем соответствующий сценарий
    try:
        if selected_mode == 'gen':
            # Комплексная генерация для гибрида (использует настройки)
            generate_keys(settings)
        elif selected_mode == 'enc':
            # Гибридное шифрование (использует настройки)
            HybridCipher.encrypt_file(settings)
        elif selected_mode == 'dec':
            # Гибридное дешифрование (использует настройки)
            HybridCipher.decrypt_file(settings)
        elif selected_mode == 'gen-sym':
            # Отдельная генерация симметричного ключа
            Utils.print_status("\n===== Режим: Генерация симметричного ключа =====")
            sym_key = SymmetricCipher.generate_key()
            output_path = args.generate_symmetric_key
            FileManager.save_file(output_path, sym_key)
            Utils.print_success("===== Генерация симметричного ключа завершена успешно! =====")
        elif selected_mode == 'gen-rsa':
            # Отдельная генерация пары RSA ключей
            Utils.print_status("\n===== Режим: Генерация пары RSA ключей =====")
            public_path = args.generate_rsa_keys[0]
            private_path = args.generate_rsa_keys[1]
            # Вызываем функцию для генерации и сохранения RSA ключей
            AsymmetricCipher.generate_and_save_rsa_keys(public_path, private_path)
            Utils.print_success("===== Генерация пары RSA ключей завершена успешно! =====")
        elif selected_mode == 'encrypt-sym-key-rsa':
            # Шифрование симметричного ключа публичным RSA ключом
            Utils.print_status("\n===== Режим: Шифрование симметричного ключа публичным RSA ключом =====")
            unencrypted_sym_path = args.encrypt_sym_key_rsa[0]
            rsa_public_path = args.encrypt_sym_key_rsa[1]
            output_encrypted_sym_path = args.encrypt_sym_key_rsa[2]
            unencrypted_sym_key_data = FileManager.read_file(unencrypted_sym_path)
            if unencrypted_sym_key_data is None:
                return
            if len(unencrypted_sym_key_data) != config.SM4_KEY_SIZE:
                Utils.print_error(
                    f"Ошибка: Размер файла симметричного ключа ({len(unencrypted_sym_key_data)} байт) не равен ожидаемому размеру ключа SM4 ({config.SM4_KEY_SIZE} байт).")
                return

            # Загружаем публичный RSA ключ
            public_key = AsymmetricCipher.load_public_key(rsa_public_path)
            if public_key is None:
                return
                # Шифруем симметричный ключ публичным RSA ключом
            encrypted_sym_key_data = AsymmetricCipher.encrypt_sym_key(public_key, unencrypted_sym_key_data)

            # Сохраняем зашифрованный симметричный ключ
            if encrypted_sym_key_data:
                FileManager.save_file(output_encrypted_sym_path, encrypted_sym_key_data)
                Utils.print_success("===== Шифрование симметричного ключа завершено успешно! =====")

    except Exception as e:
        pass


if __name__ == "__main__":
    main()
