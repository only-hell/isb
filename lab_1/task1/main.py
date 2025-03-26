import random
import config
import sys


def generate_random_key(length):
    # Функция генерации случайного ключа
    try:
        alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
        if length <= 0:
            raise ValueError("Длина ключа должна быть положительным числом")
        return ''.join(random.choice(alphabet) for _ in range(length))
    except Exception as e:
        print(f"Ошибка при генерации ключа: {e}")
        sys.exit(1)


def xor_encrypt_decrypt(text, key):
    # Функция шифровки XOR
    try:
        if len(text) != len(key):
            raise ValueError("Длина текста и ключа должны совпадать")
        return ''.join(chr(ord(text[i]) ^ ord(key[i])) for i in range(len(text)))
    except Exception as e:
        print(f"Ошибка при шифровании/дешифровании: {e}")
        sys.exit(1)


def write_to_file(filename, content):
    # Функция записи в файл
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        print(f"Ошибка записи в файл {filename}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка при работе с файлом {filename}: {e}")
        sys.exit(1)


def main():
    try:
        # Проверка наличия входного текста
        if not hasattr(config, 'INPUT_TEXT') or not config.INPUT_TEXT:
            raise ValueError("Входной текст не найден в config.py")

        # Генерация и сохранение ключа в config
        config.ENCRYPTION_KEY = generate_random_key(len(config.INPUT_TEXT))
        encrypted_text = xor_encrypt_decrypt(config.INPUT_TEXT, config.ENCRYPTION_KEY)

        # Запись результатов в файлы
        write_to_file(config.ORIGINAL_TEXT_FILE, config.INPUT_TEXT)
        write_to_file(config.ENCRYPTED_TEXT_FILE, encrypted_text)
        write_to_file(config.ENCRYPTION_KEY_FILE, config.ENCRYPTION_KEY)

        print("Зашифрованный текст: \n\n", encrypted_text)

    except Exception as e:
        print(f"Критическая ошибка в работе программы: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()