# create_initial_file.py
import os


def create_test_file(path="initial.txt", size_mb=1):
    """Создает тестовый файл с текстом или случайными данными."""
    print(f"[*] Создание тестового файла {path} размером ~{size_mb} MB...")
    try:
        # Создаем директорию, если ее нет
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Создаем повторяющуюся строку, чтобы получить нужный размер
        block_size = 1024 * 10  # 10 KB на блок
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


if __name__ == "__main__":
    # Создать файл initial.txt размером 5 MB для тестирования
    create_test_file("initial.txt", size_mb=5)
    # Можно также сохранить настройки по умолчанию после создания файла
    # import json
    # import config
    # settings = {
    #     "initial_file": config.initial_file,
    #     "encrypted_file": config.encrypted_file,
    #     "decrypted_file": config.decrypted_file,
    #     "encrypted_symmetric_key_file": getattr(config, 'encrypted_symmetric_key_file', config.symmetric_key),
    #     "public_key": config.public_key,
    #     "secret_key": config.secret_key
    # }
    # with open('settings.json', 'w', encoding='utf-8') as f:
    #     json.dump(settings, f, indent=4)
    # print("Настройки по умолчанию сохранены в settings.json")
