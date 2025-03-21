from collections import Counter


def frequency_analysis(text):
    # Исключаем символы перехода на новую строку
    text = text.replace("\n", "")

    # Подсчет количества вхождений каждого символа
    total_chars = len(text)
    freq_dict = Counter(text)

    freq_analysis = {char: count / total_chars for char, count in freq_dict.items()}
    sorted_freq = sorted(freq_analysis.items(), key=lambda x: x[1], reverse=True)

    return sorted_freq


with open("cod7.txt", "r", encoding="utf-8") as file:
    encrypted_text = file.read()

frequencies = frequency_analysis(encrypted_text)
for char, freq in frequencies:
    print(f"'{char}': {freq:.6f}")
 