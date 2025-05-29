import argparse

from key_gen import generate_keys
from hybrid_cipher import HybridCipher
from utils import Utils
from file_manager import FileManager


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема: генерация ключей, шифрование, дешифрование.")

    # Режимы работы: gen, enc, dec
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-gen', '--generation', nargs='?', const='settings.json', help='Режим генерации ключей.')
    group.add_argument('-enc', '--encryption', nargs='?', const='settings.json', help='Режим шифрования данных.')
    group.add_argument('-dec', '--decryption', nargs='?', const='settings.json', help='Режим дешифрования данных.')
    parser.add_argument('-ctf', '--create-test-file', type=str, nargs='+', help='Создает тестовый файл.')

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
                    f"Неверный формат или значение размера файла: {args.create_test_file[1]}.")
                return

        try:
            FileManager.create_test_file(file_path, size_mb)
        except Exception:
            pass

        return

    if not (args.generation or args.encryption or args.decryption):
        parser.error("Выберите один из режимов: -gen, -enc, -dec или используйте -ctf.")

    json_path = None
    if args.generation is not None:
        json_path = args.generation
    elif args.encryption is not None:
        json_path = args.encryption
    elif args.decryption is not None:
        json_path = args.decryption

    settings = Utils.load_settings(json_path)

    if args.generation is not None:
        generate_keys(settings)
    elif args.encryption is not None:
        HybridCipher.encrypt_file(settings)
    elif args.decryption is not None:
        HybridCipher.decrypt_file(settings)


if __name__ == "__main__":
    main()
