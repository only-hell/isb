import os


class FileManager:
    """Класс для управления операциями с файлами."""

    @staticmethod
    def save_file(path: str, data: bytes):
        """Сохраняет байтовые данные в файл."""
        print(f"[*] Сохранение данных в {path}...")
        try:
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)  # Создать директорию, если ее нет

            with open(path, 'wb') as f:
                f.write(data)
            print(f"[+] Данные успешно сохранены в {path}.")
        except Exception as e:
            print(f"[!] Ошибка сохранения файла {path}: {e}")
            raise

    @staticmethod
    def read_file(path: str) -> bytes:
        """Читает байтовые данные из файла."""
        print(f"[*] Чтение данных из {path}...")
        try:
            with open(path, 'rb') as f:
                data = f.read()
            print(f"[+] Данные успешно прочитаны из {path}.")
            return data
        except FileNotFoundError:
            print(f"[!] Ошибка: Файл не найден по пути {path}")
            raise
        except Exception as e:
            print(f"[!] Ошибка чтения файла {path}: {e}")
            raise

    @staticmethod
    def create_test_file(path: str = "initial.txt", size_mb: int = 1):
        """Создает тестовый файл с повторяющимся текстом."""
        print(f"[*] Создание тестового файла {path} размером ~{size_mb} MB...")
        try:
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)  # Создать директорию, если ее нет

            block_size = 1024 * 10  # Блок 10 KB
            # Повторяющаяся строка для заполнения файла
            text_block = "Это повторяющийся текст для заполнения файла. " * (
                    block_size // len("Это повторяющийся текст для заполнения файла. ")) + "\n"
            bytes_block = text_block.encode('utf-8')

            target_bytes = size_mb * 1024 * 1024  # Целевой размер в байтах
            bytes_written = 0

            with open(path, 'wb') as f:
                while bytes_written < target_bytes:
                    f.write(bytes_block)
                    bytes_written += len(bytes_block)
            print(f"[+] Тестовый файл {path} создан.")
        except Exception as e:
            print(f"[!] Ошибка при создании тестового файла: {e}")
            raise
