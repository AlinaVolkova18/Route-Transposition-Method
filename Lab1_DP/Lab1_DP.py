import numpy as np

# Файл с текстом для шифрования
TEXT_FILE = "text.txt"
# Зашифрованный текст и так же источник данных для декодирования
ENCODED_FILE = "encoded.txt"
# Файл результата декодировнаия
DECODE_FILE = "decode.txt"
# Файл с ключём
KEY_FILE = "key.txt"
# Вспомогательный файл
SUPPORT_FILE = "support.txt"


def encode(m, n):
    global TEXT_FILE, ENCODED_FILE, DECODE_FILE, KEY_FILE, SUPPORT_FILE
    # Считываем текст и ключ
    with open(TEXT_FILE, "r", encoding="utf-8") as file:
        text = file.read()
    with open(KEY_FILE, "r", encoding="utf-8") as file:
        key = file.read()
    # Создаём ключ из ключевого слова
    #из ключа создаем побуквенный массив (буквы в алфавитном порядке)
    sorted_key = sorted(key)
    indexes = []
    key_number = [0 for i in range(len(sorted_key))]
    counter = 1

    for i in range(len(sorted_key)):
        if sorted_key[i] == sorted_key[i - 1]:
            ### Ищем по срезу от прошлого символа
            indexes += [key.find(sorted_key[i], indexes[-1] + 1)]
        else:
            indexes += [key.find(sorted_key[i])]
    for i in indexes:
        key_number[i] = counter
        counter += 1
    # Сохраняем вспомогательную информацию
    space_indexes = []
    line_break_indexes = []
    lenght_of_text = len(text)
    for i in range(len(text)):
        if text[i] == " ":
            space_indexes += [i]
        elif text[i] == "\n":
            line_break_indexes += [i]
    # Создаём матрицу маршрутной транспозиции
    text = text.replace(" ", "")
    text = text.replace("\n", "")

    ## Создаём русский алфавит
    a = ord('а')
    russian_alphabet = "".join([chr(i) for i in range(a, a + 32)]).upper()
    ## Добавляем нехватающих букв
    if m * n > len(text):
        delta = m * n - len(text)
        counter = 0
        for i in range(delta):
            text += russian_alphabet[counter]
            #проверка на то, что если закончился алфавит начинаем заново
            if counter >= len(russian_alphabet) - 1:
                counter = 0
            else:
                counter += 1

    matrix = np.zeros((n, m), dtype=str)
    characters_passed = 0
    for i in range(matrix.shape[0]):
        if i % 2 == 0:
            matrix[i] = list(text[characters_passed:characters_passed + m])
            characters_passed += m
        else:
            matrix[i] = list(text[characters_passed:characters_passed + m][::-1])
            characters_passed += m
    # Получаем зашифрованное сообщение
    encoded = []
    for i in indexes:
        encoded += ["".join(list(matrix[:, i]))]
    # Запись результатов в файл
    with open(SUPPORT_FILE, "w+", encoding="utf-8") as file:
        file.write(str([space_indexes, line_break_indexes, lenght_of_text]))
    with open(ENCODED_FILE, "w+", encoding="utf-8") as file:
        file.write(" ".join(encoded))

    return encoded


def decode(m, n):
    # Считываем информацию из файлов
    global TEXT_FILE, ENCODED_FILE, DECODE_FILE, KEY_FILE, SUPPORT_FILE
    with open(ENCODED_FILE, "r", encoding="utf-8") as file:
        encoded = file.read().split(" ")
    with open(KEY_FILE, "r", encoding="utf-8") as file:
        key = file.read()
    with open(SUPPORT_FILE, "r", encoding="utf-8") as file:
        space_indexes, line_break_indexes, lenght_of_text = eval(file.read())
    # Создаём ключ из ключевого слова
    sorted_key = sorted(key)
    indexes = []
    key_number = [0 for i in range(len(sorted_key))]
    counter = 1

    for i in range(len(sorted_key)):
        if sorted_key[i] == sorted_key[i - 1]:
            ### Ищем по срезу от прошлого символа
            indexes += [key.find(sorted_key[i], indexes[-1] + 1)]
        else:
            indexes += [key.find(sorted_key[i])]
    for i in indexes:
        key_number[i] = counter
        counter += 1
    # Создание матрицы маршрутной транспозиции
    matrix = np.zeros((m, n), dtype=str)
    for i in range(len(encoded)):
        matrix[indexes[i]] = list(encoded[i])
    #переворачиваем матрицу
    matrix = matrix.T
    # Декодируем зашифрованный текст
    decoded = []
    for i in range(matrix.shape[0]):
        if i % 2 == 0:
            decoded += matrix[i, ::].tolist()
        else:
            decoded += matrix[i, ::-1].tolist()
    decoded = "".join(decoded)
    for i in range(lenght_of_text):
        if i in space_indexes:
            decoded = decoded[:i] + " " + decoded[i:]
        if i in line_break_indexes:
            decoded = decoded[:i] + "\n" + decoded[i:]
    decoded = decoded[:lenght_of_text]
    # Записываем результат в файл
    with open(DECODE_FILE, "w+", encoding="utf-8") as file:
        file.write(decoded)

    return decoded


def main():
    mode = input("Выберите кодировать (e) или декодировать (d): ")
    m, n = 9, 10
    if mode == 'e':
        return encode(m, n)
    elif mode == 'd':
        return decode(m, n)
    else:
        print("Введён неправильный режим работы")

print(main())