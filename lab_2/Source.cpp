#include <iostream>
#include <fstream>
#include <random>
#include <locale>

int main() {
    std::setlocale(LC_ALL, "");

    const int sequence_length = 128;  
    const std::string output_path = "C:/Users/user/Desktop/oib lab2/pythonProject/lab2/sequence_c++.txt";  

    // Открытие файла для записи
    std::ofstream output_file(output_path);
    if (!output_file) {
        std::cerr << "Не удалось открыть файл для записи: " << output_path << std::endl;
        return 1;
    }

    // Создание генератора случайных чисел и распределения
    std::random_device rd;  
    std::mt19937 rng(rd());  
    std::uniform_int_distribution<int> bit_dist(0, 1); 

    // Генерация последовательности случайных битов
    for (int i = 0; i < sequence_length; ++i) {
        output_file << bit_dist(rng);  
    }

    
    output_file.close();
    std::cout << "Бинарная последовательность длиной 128 бит успешно записана в файл." << std::endl;
    return 0;
}
