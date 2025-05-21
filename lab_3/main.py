import argparse
import os

from key_gen import generate_keys
from encrypt import hybrid_encrypt
from decrypt import hybrid_decrypt
from utils import Utils
from file_manager import FileManager


def main():
    """Главная точка входа в приложение."""
    parser = argparse.ArgumentParser(description="Гибридная криптосистема: генерация ключей, шифрование, дешифрование.")

    # Режимы работы: gen, enc, dec (взаимоисключающие, необязательны если используется ctf)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-gen', '--generation', nargs='?', const='settings.json', help='Режим генерации ключей.')
    group.add_argument('-enc', '--encryption', nargs='?', const='settings.json', help='Режим шифрования данных.')
    group.add_argument('-dec', '--decryption', nargs='?', const='settings.json', help='Режим дешифрования данных.')

    # Опция создания тестового файла
    parser.add_argument('-ctf', '--create-test-file', type=str, nargs='+',
                        help='Создает тестовый файл. Принимает путь и опционально размер в MB (по умолчанию 1).')

    args = parser.parse_args()

    # Обработка создания тестового файла (-ctf)
    if args.create_test_file:
        file_path = args.create_test_file[0]
        size_mb = 1  # Размер по умолчанию в MB

        # Парсим опциональный размер, если предоставлен
        if len(args.create_test_file) > 1:
            try:
                size_mb = int(args.create_test_file[1])
                if size_mb <= 0:
                    raise ValueError("Размер должен быть положительным числом.")
            except ValueError:
                Utils.print_error(
                    f"Неверный формат или значение размера файла: {args.create_test_file[1]}. Размер должен быть положительным целым числом (в MB).")
                return  # Выход при ошибке парсинга размера

        # Пытаемся создать файл. FileManager сам выводит ошибки и выбрасывает исключения.
        try:
            FileManager.create_test_file(file_path, size_mb)
        except Exception:
            # Если FileManager выбросил исключение (после вывода своей ошибки), просто выходим.
            pass

        return  # Всегда выходим из main после попытки создания файла (-ctf)

    # Если не был запрошен только create-test-file, то один из gen/enc/dec должен быть обязательным.
    if not (args.generation or args.encryption or args.decryption):
        parser.error("Выберите один из режимов: -gen, -enc, -dec или используйте -ctf.")

    # Определяем путь к JSON файлу настроек
    json_path = None
    if args.generation is not None:
        json_path = args.generation
    elif args.encryption is not None:
        json_path = args.encryption
    elif args.decryption is not None:
        json_path = args.decryption

    # Загружаем настройки и запускаем выбранный сценарий
    try:
        settings = Utils.load_settings(json_path)

        if args.generation is not None:
            generate_keys(settings)
        elif args.encryption is not None:
            hybrid_encrypt(settings)
        elif args.decryption is not None:
            hybrid_decrypt(settings)

    except Exception:
        pass


if __name__ == "__main__":
    main()
