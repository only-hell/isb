def xor(text, key):
    result = []
    for i in range(len(text)):
        result.append(chr(ord(text[i]) ^ ord(key[i % len(key)])))
    return ''.join(result)  # Соединяем результат в строку


def main():
    input_text = ("КАКОЙТО НОРМАЛЬНЫЙ ТЕКСТ")
    key = "КЛЮЧ"
    print(xor(input_text, key))


if __name__ == "__main__":
    main()