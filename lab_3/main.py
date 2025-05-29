import argparse

from key_gen import generate_keys
from hybrid_cipher import HybridCipher
from utils import Utils
from file_manager import FileManager
from symmetric_encryption import SymmetricCipher
from asymmetric_encryption import AsymmetricCipher


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема: генерация ключей, шифрование, дешифрование.")

    # Режимы работы: gen (все ключи),gen-sym и gen-rsa (по отдельности), enc, dec
    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument('-gen', '--generation', nargs='?', const='settings.json', help='Режим генерации ВСЕХ ключей.')
    group.add_argument('-enc', '--encryption', nargs='?', const='settings.json', help='Режим шифрования данных.')
    group.add_argument('-dec', '--decryption', nargs='?', const='settings.json', help='Режим дешифрования данных.')
    parser.add_argument('-ctf', '--create-test-file', type=str, nargs='+', help='Создает тестовый файл.')
    group.add_argument('-gen-sym', '--generate-symmetric-key', type=str, metavar='SYMMETRIC_KEY_PATH',
                       help='Генерирует только симметричный ключ SM4 и сохраняет его в указанный файл.')
    group.add_argument('-gen-rsa', '--generate-rsa-keys', type=str, nargs=2,
                       metavar=('PUBLIC_KEY_PATH', 'PRIVATE_KEY_PATH'),
                       help='Генерирует пару RSA ключей (публичный и приватный) и сохраняет их в указанные файлы.')
    args = parser.parse_args()

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
        json_path = None
    elif args.generate_rsa_keys is not None:
        selected_mode = 'gen-rsa'

        json_path = None
    if selected_mode is None:
        parser.error("Выберите один из режимов: -gen, -enc, -dec, -gen-sym, -gen-rsa или используйте -ctf.")

    settings = {}
    if selected_mode in ['gen', 'enc', 'dec']:
        try:
            settings = Utils.load_settings(json_path)
        except Exception as e:
            Utils.print_error(f"Не удалось загрузить настройки: {e}")
            return

    try:
        if selected_mode == 'gen':
            generate_keys(settings)
        elif selected_mode == 'enc':
            HybridCipher.encrypt_file(settings)
        elif selected_mode == 'dec':
            HybridCipher.decrypt_file(settings)
        elif selected_mode == 'gen-sym':
            Utils.print_status("\n===== Режим: Генерация симметричного ключа =====")
            sym_key = SymmetricCipher.generate_key()
            output_path = args.generate_symmetric_key
            FileManager.save_file(output_path, sym_key)
            Utils.print_success("===== Генерация симметричного ключа завершена успешно! =====")
        elif selected_mode == 'gen-rsa':
            Utils.print_status("\n===== Режим: Генерация пары RSA ключей =====")
            public_path = args.generate_rsa_keys[0]
            private_path = args.generate_rsa_keys[1]
            AsymmetricCipher.generate_and_save_rsa_keys(public_path, private_path)
            Utils.print_success("===== Генерация пары RSA ключей завершена успешно! =====")
    except Exception as e:
        pass


if __name__ == "__main__":
    main()
