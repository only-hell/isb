import random
from config_random import SEQUENCE_LENGTH, OUTPUT_PATH


def generate_random_bit_sequence(length=SEQUENCE_LENGTH, output_path=OUTPUT_PATH):
    # Генерация случайной бинарной последовательности и запись в файл
    try:
        with open(output_path, "w") as file:
            for _ in range(length):
                file.write(str(random.randint(0, 1)))
        print(f"Бинарная последовательность длиной {length} бит успешно записана в файл.")
    except IOError as e:
        print(f"Не удалось открыть файл для записи: {output_path}")
        print("Ошибка:", e)


if __name__ == "__main__":
    generate_random_bit_sequence()
