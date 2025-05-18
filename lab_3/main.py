# main.py

import argparse
import json
import os  # Импорт os для проверки существования файла
from key_gen import generate_keys
from encrypt import hybrid_encrypt
from decrypt import hybrid_decrypt
import config  # Импорт config для дефолтных путей


def load_settings(json_path=None):
    """Загружает настройки из JSON файла, объединяя с дефолтными."""
    print("[*] Загрузка настроек...")
    # Начинаем с дефолтных настроек из config.py
    settings = {
        "initial_file": config.initial_file,
        "encrypted_file": config.encrypted_file,
        "decrypted_file": config.decrypted_file,
        # Используем новое имя ключа для ясности, даже если в config старое
        # Если в вашем settings.json осталось старое имя 'symmetric_key',
        # нужно будет поправить это место или использовать .get() с запасным именем.
        "encrypted_symmetric_key_file": getattr(config, 'encrypted_symmetric_key_file', config.symmetric_key),
        "public_key": config.public_key,
        "secret_key": config.secret_key
    }

    # Если указан путь к JSON файлу, пытаемся загрузить и обновить настройки
    if json_path:
        print(f"[*] Попытка загрузить настройки из JSON файла: {json_path}")
        if not os.path.exists(json_path):
            print(f"[!] Ошибка: JSON файл настроек не найден по пути {json_path}")
            # Продолжаем с дефолтными настройками, но предупреждаем
        else:
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_settings = json.load(f)
                settings.update(json_settings)
                print("[+] Настройки успешно обновлены из JSON файла.")
            except json.JSONDecodeError:
                print(f"[!] Ошибка: Неверный формат JSON файла {json_path}")
                # Продолжаем с дефолтными настройками, но предупреждаем
            except Exception as e:
                print(f"[!] Неизвестная ошибка при загрузке JSON настроек: {e}")
                # Продолжаем с дефолтными настройками, но предупреждаем

    print("[+] Настройки загружены.")
    # print("Используемые настройки:")
    # for key, value in settings.items():
    #     print(f"  {key}: {value}")
    return settings


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема: генерация, шифрование, дешифрование")
    group = parser.add_mutually_exclusive_group(required=True)  # required=True гарантирует выбор одного флага
    group.add_argument('-gen', '--generation', nargs='?', const='settings.json',
                       help='Запускает режим генерации ключей. Опционально принимает путь к JSON файлу настроек (по умолчанию settings.json).')
    group.add_argument('-enc', '--encryption', nargs='?', const='settings.json',
                       help='Запускает режим шифрования данных. Опционально принимает путь к JSON файлу настроек (по умолчанию settings.json).')
    group.add_argument('-dec', '--decryption', nargs='?', const='settings.json',
                       help='Запускает режим дешифрования данных. Опционально принимает путь к JSON файлу настроек (по умолчанию settings.json).')

    args = parser.parse_args()

    # Определяем путь к JSON файлу из аргументов
    json_path = None
    if args.generation is not None:
        json_path = args.generation
    elif args.encryption is not None:
        json_path = args.encryption
    elif args.decryption is not None:
        json_path = args.decryption

    # Если флаг был указан без значения, nargs='?' установит его в const='settings.json'
    # Если флаг был указан со значением, nargs='?' установит его в это значение
    # Если флаг не был указан, соответствующее поле в args будет None

    settings = load_settings(json_path if isinstance(json_path, str) else None)

    if args.generation is not None:
        generate_keys(settings)
    elif args.encryption is not None:
        hybrid_encrypt(settings)
    elif args.decryption is not None:
        hybrid_decrypt(settings)


if __name__ == "__main__":
    main()
