with open("cod7.txt", encoding="utf-8") as file:
    text = file.read()

# Словарь замен символов
# Полностью переделал принцип замены букв для удобства
replacements = {"-": " "}

# вносим изменения в исходный зашифрованный текст
decoded_text = text
for old, new in replacements.items():
    decoded_text = decoded_text.replace(old, new)

print(decoded_text)
