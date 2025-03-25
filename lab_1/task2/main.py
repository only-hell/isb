import config


def decode_text(file_path, replacements):
    # функия расшифровки текста
    with open(file_path, encoding="utf-8") as file:
        text = file.read()

    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def main():
    decoded_text = decode_text(config.ENCODED_FILE, config.REPLACEMENTS)

    # запись результатов в файлы
    with open(config.DECODED_FILE, "w", encoding="utf-8") as file:
        file.write(decoded_text)
    with open(config.DECRYPTION_KEY_FILE, "w", encoding="utf-8") as file:
        file.writelines(f"{k} -> {v}\n" for k, v in config.REPLACEMENTS.items())

    print("Декодированный текст:\n\n", decoded_text)


if __name__ == "__main__":
    main()
