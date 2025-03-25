import random
import config


def generate_random_key(length):
    # функция генерации случайного ключа
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
    return ''.join(random.choice(alphabet) for _ in range(length))


def xor_encrypt_decrypt(text, key):
    # функция шифровки XOR
    return ''.join(chr(ord(text[i]) ^ ord(key[i])) for i in range(len(text)))


key = generate_random_key(len(config.INPUT_TEXT))


def main():
    encrypted_text = xor_encrypt_decrypt(config.INPUT_TEXT, key)

    # запись результатов в файлы
    with open(config.ORIGINAL_TEXT_FILE, 'w', encoding='utf-8') as f:
        f.write(config.INPUT_TEXT)
    with open(config.ENCRYPTED_TEXT_FILE, 'w', encoding='utf-8') as f:
        f.write(encrypted_text)
    with open(config.ENCRYPTION_KEY_FILE, 'w', encoding='utf-8') as f:
        f.write(key)

    print("Зашифрованный текст: \n\n", encrypted_text)


if __name__ == "__main__":
    main()
