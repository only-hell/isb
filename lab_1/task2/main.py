import config
import sys


def decode_text(file_path, replacements):
    # Функция расшифровки текста
    try:
        with open(file_path, encoding="utf-8") as file:
            text = file.read()

        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        sys.exit(1)
    except PermissionError:
        print(f"Ошибка: нет прав для чтения файла {file_path}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Ошибка: неверная кодировка файла {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла: {e}")
        sys.exit(1)


def write_to_file(file_path, content):
    # Функция записи в файл
    try:
        with open(file_path, 'w', encoding="utf-8") as file:
            if isinstance(content, str):
                file.write(content)
            else:  # Для записи списка строк
                file.writelines(content)
    except PermissionError:
        print(f"Ошибка: нет прав для записи в файл {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка при записи в файл: {e}")
        sys.exit(1)


def main():
    try:
        # Проверка наличия необходимых параметров
        if not hasattr(config, 'REPLACEMENTS') or not config.REPLACEMENTS:
            raise ValueError("Словарь замен (REPLACEMENTS) не найден в config.py")

        decoded_text = decode_text(config.ENCODED_FILE, config.REPLACEMENTS)

        # Подготовка ключа для записи
        decryption_key_content = []
        for k, v in config.REPLACEMENTS.items():
            decryption_key_content.append(f"{k} -> {v}\n")

        # Запись результатов
        write_to_file(config.DECODED_FILE, decoded_text)
        write_to_file(config.DECRYPTION_KEY_FILE, decryption_key_content)

        print("Декодированный текст:\n\n", decoded_text)

    except Exception as e:
        print(f"Критическая ошибка в работе программы: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
