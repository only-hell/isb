import json
import os
import config


class Utils:
    """Вспомогательные функции для загрузки настроек и вывода статуса."""

    @staticmethod
    def load_settings(json_path: str = None) -> dict:
        """Загружает настройки из JSON файла, объединяя с дефолтными из config.py."""
        print("[*] Загрузка настроек...")
        settings = {
            "initial_file": config.initial_file,
            "encrypted_file": config.encrypted_file,
            "decrypted_file": config.decrypted_file,
            "encrypted_symmetric_key_file": config.encrypted_symmetric_key_file,
            "public_key": config.public_key,
            "secret_key": config.secret_key
        }

        if json_path and isinstance(json_path, str):
            print(f"[*] Попытка загрузить настройки из JSON файла: {json_path}")
            if not os.path.exists(json_path):
                print(f"[!] Предупреждение: JSON файл настроек не найден по пути {json_path}.")
            else:
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        json_settings = json.load(f)
                    settings.update(json_settings)
                    print("[+] Настройки успешно обновлены из JSON файла.")
                except json.JSONDecodeError:
                    print(f"[!] Предупреждение: Неверный формат JSON файла {json_path}.")
                except Exception as e:
                    print(f"[!] Предупреждение: Неизвестная ошибка при загрузке JSON настроек ({e}).")

        print("[+] Настройки загружены.")
        return settings

    @staticmethod
    def print_status(message: str):
        """Выводит сообщение о текущем статусе."""
        print(f"[*] {message}")

    @staticmethod
    def print_success(message: str):
        """Выводит сообщение об успешном выполнении."""
        print(f"[+] {message}")

    @staticmethod
    def print_error(message: str):
        """Выводит сообщение об ошибке."""
        print(f"[!] {message}")
