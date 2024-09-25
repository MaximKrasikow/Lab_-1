import random  # Импортируем библиотеку random для работы сс случайными значениями
import tkinter as tk  # Импортируем tkinter для создания графического интерфейса
from tkinter import filedialog  # Импортируем filedialog для работы с диалоговыми окнами для выбора файлов

# Функция пузырьковой сортировки целочисленного массива случайных чисел
def test_bubble(arr):
    arr_n = len(arr)  # Получение длины массива
    swap_count = 0  # Инициализация счётчика

    # Цикл пузырьковой сортировки
    for i in range(arr_n - 1):  # Внешний цикл: проход по массиву
        swapped = False  # Переменная для отслеживания обменов в текущем проходе

        # Внутренний цикл: сравнение пар элементов
        for j in range(arr_n - i - 1):  # Проход по неотсортированной части массива
            if arr[j] > arr[j + 1]:  # Сравнение текущего элемента со следующим
                # Обмен элементов
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_count += 1  # Увеличение счётчика обменов
                swapped = True  # Установка флага обмена

        # Если в текущем проходе не было обменов, массив отсортирован
        if not swapped:
            break  # Выход из внешнего цикла, если массив отсортирован

    return swap_count  # Функция возвращает количество обменов элементов в цикле

# Функция работы с тестовыми данными из файла
def file_test():
    # Открытие проводника для выбора файла
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно Tkinter
    filename = filedialog.askopenfilename(title="Выберите файл с тестами", filetypes=[("Text files", "*.txt")])

    if not filename:  # Если файл не выбран
        print("\n*** !ОШИБКА: Файл не выбран. ***\n")
        return

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()  # Считываются все строки из файла
    except FileNotFoundError:
        print("\n*** !ОШИБКА: Файл не найден. ***\n")
        return

    test_number = 1  # Номер теста
    test_total = 0  # Общее количество тестов
    test_passed = 0  # Количество пройденных тестов
    i = 0  # Индекс текущей строки в файле

    # Цикл прохода по строкам файла
    while i < len(lines):
        line = lines[i].strip()

        # Игнорируем пустые строки и комментарии в файле
        if not line or line.startswith("#"):
            i += 1
            continue
        try:
            expected_swaps = int(line)  # Чтение предполагаемого количества обменов
            i += 1
            if i < len(lines):
                array = list(map(int, lines[i].strip().split()))  # Чтение массива
                i += 1
            else:
                print(f"\n*** !ОШИБКА: Неверный формат данных в тесте {test_number}. ***\n")
                break

            # Печатаем данные теста
            print(f"\nТест {test_number}: МАССИВ {array}, Предполагаемое количество обменов: {expected_swaps}", end=", ")

            swap_count = test_bubble(array)  # Вызов функции сортировки
            print(f"Получаемое количество обменов: {swap_count}, Результат: {'ДА' if swap_count == expected_swaps else 'НЕТ'}")

            # Увеличиваем счётчики тестов
            test_number += 1
            test_total += 1
            if swap_count == expected_swaps:
                test_passed += 1

        except (ValueError, TypeError):
            print(f"\n*** !ОШИБКА: неверный формат данных в тесте {test_number}. ***\n")
            break

    print(f"\nКоличество тестов пройдено: {test_passed}/{test_total} \n===============\n")  # Вывод общего количества пройденных тестов

# Функция для работы с вводом вручную
def manual_test():
    print("\n----- Ввод массива вручную -----")
    user_input = input("Введите массив чисел через пробел: ").strip()

    if not user_input:  # Проверка на пустой ввод
        print("\n*** !ОШИБКА: Вы не ввели массив. Пожалуйста, введите числа. ***\n")
        return
    try:
        array = list(map(int, user_input.split()))  # Преобразование строки в список чисел
        if any(n < 0 for n in array):
            print("\n*** !ОШИБКА: Массив не может содержать отрицательные числа. ****\n")
            return
        if any(n > 10**9 for n in array):  # Проверка на превышение максимального значения
            print("\n*** !ОШИБКА: Элементы массива не могут превышать 10^9. ***\n")
            return
    except ValueError:
        print("\n*** !ОШИБКА: Необходимо вводить только целые числа. ***\n")
        return

    print("\nВведённый массив:", array, "\n---------------\n")

    swap_count = test_bubble(array)  # Вызов функции сортировки
    print("Количество обменов:", swap_count, "\n===============\n")

# Унифицированная функция для генерации случайного массива
def random_test(generate_size=True):
    if generate_size:
        # Случайный размер
        size = random.randint(1, 1000)  # Генерация случайного размера от 1 до 1000
        print("\n----- Генерация случайного массива с рандомным размером -----")
    else:
        # Ввод размера пользователем
        print("\n----- Генерация случайного массива с выбором размера -----")
        try:
            size = int(input("Введите размер массива: ").strip())
        except ValueError:
            print("\n*** !ОШИБКА: размер массива должен быть целым числом. ***\n")
            return

        if size <= 0 or size > 1000:  # Проверка размера массива
            print("\n*** !ОШИБКА: размер массива должен быть в пределах от 1 до 1000. ***\n")
            return

    array = [random.randint(1, 10**9) for _ in range(size)]  # Генерация случайного массива
    print("\nСгенерированный массив:", array, "\n---------------\n")

    swap_count = test_bubble(array)  # Вызов функции сортировки
    print("Количество обменов:", swap_count, "\n===============\n")

# Главная функция
def main():
    while True:
        choice = input("Выберите способ ввода данных или введите 'ВЫХОД' для завершения программы:\n"
                       "1. Ввести массив вручную\n"
                       "2. Тестировать массив из файла\n"
                       "3. Сгенерировать случайный массив с выбором размера\n"
                       "4. Сгенерировать случайный массив с рандомным размером\n"
                       "Ваш выбор (1/2/3/4) или ВЫХОД: ").strip().upper()

        # Используем match-case для считывания выбора пользователя
        match choice:
            case '1':
                manual_test()  # Ввод вручную
            case '2':
                file_test()  # Тестирование из файла через диалоговое окно
            case '3':
                random_test(generate_size=False)  # Генерация случайного массива с выбором размера
            case '4':
                random_test(generate_size=True)  # Генерация случайного массива с рандомным размером
            case 'ВЫХОД':
                print("Программа завершена. \n===============\n")
                break  # Завершение программы при вводе "ВЫХОД"
            case _:
                print("\n*** !ОШИБКА: Неверный ввод!. ***\n")

# Запуск программы с главной функции
main()
