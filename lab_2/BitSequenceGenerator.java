import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

public class BitSequenceGenerator {
    // Константы
    private static final int SEQUENCE_LENGTH = 128;
    private static final String OUTPUT_PATH = "C:/Users/user/Desktop/oib lab2/pythonProject/lab2/sequence_java.txt";
    
    // Логгер
    private static final Logger logger = Logger.getLogger(BitSequenceGenerator.class.getName());

    public static void main(String[] args) {
        // Проверка существования папки, если нет - создать
        File outputFile = new File(OUTPUT_PATH);
        File parentDir = outputFile.getParentFile();
        if (!parentDir.exists()) {
            if (parentDir.mkdirs()) {
                System.out.println("Папка успешно создана: " + parentDir.getAbsolutePath());
            } else {
                System.err.println("Не удалось создать папку: " + parentDir.getAbsolutePath());
                return;
            }
        }

        try (FileWriter writer = new FileWriter(outputFile)) {
            Random random = new Random();

            for (int i = 0; i < SEQUENCE_LENGTH; i++) {
                writer.write(random.nextBoolean() ? '1' : '0');
            }

            System.out.println("Бинарная последовательность длиной " + SEQUENCE_LENGTH + " бит успешно записана в файл: sequence_java.txt");
        } catch (IOException e) {
            // Логируем ошибку
            logger.log(Level.SEVERE, "Не удалось записать в файл: " + OUTPUT_PATH, e);
            System.err.println("Произошла ошибка при записи в файл. См. лог для подробностей.");
        }
    }
}
