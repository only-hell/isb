with open("cod7.txt", encoding="utf-8") as file:
    text = file.read()

# Словарь замен символов на буквы русского алфавита
# Для удобства работы я заменил символы "/" и "\" на "{" и "}" соответственно
replacements = {
    "": "Я", "1": "Й", "d": "Ш", "9": "Г", "p": "Ф", "c": "Щ", "o": "У",
    "x": "Э", "t": "Х", "}": "Л", "{": "К", "0": "Е", "s": "Ь",
    "f": "Ц", "7": "Б", "n": "С", "q": "М", "4": "Ж", "z": "Ю",
    "5": "Д", "r": "П", "w": "Н", "8": "В", "3": "З", ";": "Ы",
    "/": "К", "6": "А", "m": "Р", "2": "И", "i": "Т", "k": "Ч",
    "e": "О", "-": " "
}

# Дешифруем текст
decoded_text = text
for old, new in replacements.items():
    decoded_text = decoded_text.replace(old, new)

# Сохраняем дешифрованный текст
with open("decoded_text.txt", "w", encoding="utf-8") as file:
    file.write(decoded_text)

# Сохраняем найденный ключ шифрования
with open("decryption_key.txt", "w", encoding="utf-8") as file:
    for key, value in replacements.items():
        file.write(f"{key} -> {value}\n")

print("Декодированный текст: \n\n", decoded_text)
