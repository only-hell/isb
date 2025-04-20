import math
import os
from config import BLOCK_SIZE, P_VALUE_THRESHOLD, THEORETICAL_PROBS
from scipy.special import gammaincc


def read_sequence(filename="sequence.txt"):
    # Чтение последовательности из файла
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден. Убедитесь, что он лежит рядом с main.py.")
    with open(filename, "r") as file:
        return file.read().strip()


def frequency_test(bits):
    # Частотный побитовый тест (Frequency test)
    n = len(bits)
    s = sum(1 if bit == '1' else -1 for bit in bits)
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value


def runs_test(bits):
    # Тест на одинаковые подряд идущие биты (Runs test)
    n = len(bits)
    pi = bits.count('1') / n
    if abs(pi - 0.5) > (2 / math.sqrt(n)):
        return 0.0
    vn_obs = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            vn_obs += 1
    p_value = math.erfc(abs(vn_obs - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))
    return p_value


def longest_run_ones_test(bits, block_size=BLOCK_SIZE):
    # Тест на самую длинную последовательность единиц в блоке (Longest run of ones)
    n = len(bits)
    if n < block_size:
        raise ValueError("Последовательность слишком короткая для данного размера блока.")

    num_blocks = n // block_size
    blocks = [bits[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]
    max_runs = [max(map(len, block.split('0'))) for block in blocks]

    freq = [0, 0, 0, 0]  # категории: <=1, ==2, ==3, >=4
    for run in max_runs:
        if run <= 1:
            freq[0] += 1
        elif run == 2:
            freq[1] += 1
        elif run == 3:
            freq[2] += 1
        else:
            freq[3] += 1

    # Расчёт хи-квадрат и P-value
    chi_squared = 0.0
    for i in range(4):
        expected = num_blocks * THEORETICAL_PROBS[i]
        chi_squared += (freq[i] - expected) ** 2 / expected

    degrees_of_freedom = 3
    p_value = gammaincc(degrees_of_freedom / 2.0, chi_squared / 2.0)

    return freq, p_value


def write_results_to_file(filename, results):
    # Запись результатов тестирования в файл
    with open(filename, "w", encoding="utf-8") as file:
        for result in results:
            file.write(result + "\n")


def compare_sequences(sequences, sequence_names):
    # Сравнение последовательностей и запись результатов в файл
    results = ["Результаты NIST тестов для 128-битных последовательностей:\n"]

    for sequence_name, sequence in zip(sequence_names, sequences):
        results.append(f"\nРезультаты для {sequence_name}:")

        results.append("1. Частотный побитовый тест:")
        freq_p = frequency_test(sequence)
        results.append(f"P-value: {freq_p:.6f} => {'Прошел' if freq_p >= P_VALUE_THRESHOLD else 'Не прошел'}\n")

        results.append("2. Тест на одинаковые подряд идущие биты:")
        runs_p = runs_test(sequence)
        results.append(f"P-value: {runs_p:.6f} => {'Прошел' if runs_p >= P_VALUE_THRESHOLD else 'Не прошел'}\n")

        results.append("3. Тест на самую длинную последовательность единиц в блоке:")
        longest_run_hist, run_p = longest_run_ones_test(sequence)
        results.append("Категории (<=1, 2, 3, >=4): " + str(longest_run_hist))
        results.append(f"P-value: {run_p:.6f} => {'Прошел' if run_p >= P_VALUE_THRESHOLD else 'Не прошел'}")

    # Запись результатов в файл
    write_results_to_file("test_results_comparison.txt", results)
    print("Результаты тестирования сохранены в файл test_results_comparison.txt")


def main():
    # Основная функция для выполнения всех тестов
    sequence_py = read_sequence("sequence_py.txt")
    sequence_java = read_sequence("sequence_java.txt")
    sequence_cplusplus = read_sequence("sequence_c++.txt")

    # Сравнение всех последовательностей
    compare_sequences([sequence_py, sequence_java, sequence_cplusplus], ["Python", "Java", "C++"])


if __name__ == "__main__":
    main()
