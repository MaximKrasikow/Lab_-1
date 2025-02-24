def main():
    # Объявляем константы: 
    # TOTAL_SIZE – общий объём виртуального диска в байтах
    # MIN_SIZE, MAX_SIZE – минимальный и максимальный допустимые размеры файла
    TOTAL_SIZE = 368640
    MIN_SIZE = 18
    MAX_SIZE = 32768

    # Инициализируем структуру диска:
    # "used" – список занятых блоков в виде [имя файла, начало, конец]
    # "free" – список свободных блоков; изначально весь диск свободен
    disk = {"used": [], "free": [[0, TOTAL_SIZE - 1]]}

    # Основной цикл работы программы – реализует интерфейс командной строки
    while True:
        print("1. Добавить 2. Удалить 3. Просмотр 4. Выход")
        try:
            cmd = input("> ").strip()
            if cmd == "4":  # Завершение работы программы
                break

            if cmd == "1":  # Добавление нового файла
                name = input("Имя: ").strip()
                # Проверка на уникальность имени файла
                for f in disk["used"]:
                    if f[0] == name:
                        print("Имя занято")
                        break
                else:
                    # Ввод и проверка корректности размера файла
                    while True:
                        try:
                            size_input = input("Размер: ").strip()
                            if not size_input:
                                raise ValueError("Введите число")
                            size = int(size_input)
                            # Проверка, что размер находится в допустимых пределах
                            if MIN_SIZE <= size <= MAX_SIZE:
                                break
                            else:
                                print(f"Допустимо {MIN_SIZE} - {MAX_SIZE}")
                        except ValueError:
                            print(f"Допустимо {MIN_SIZE} - {MAX_SIZE}")

                    # Поиск наименьшего подходящего блока (best-fit алгоритм)
                    found = None
                    min_size = TOTAL_SIZE + 1  # Инициализируем значение, превышающее максимальный возможный размер
                    for i, block in enumerate(disk["free"]):
                        block_size = block[1] - block[0] + 1
                        if block_size >= size and block_size < min_size:
                            min_size = block_size
                            found = i

                    if found is not None:
                        # Если найден подходящий свободный блок, выделяем из него требуемый отрезок
                        block = disk["free"].pop(found)
                        start = block[0]
                        end = start + size - 1
                        disk["used"].append([name, start, end])
                        # Если осталась неиспользованная часть блока, добавляем её обратно в список свободных
                        if end < block[1]:
                            disk["free"].append([end + 1, block[1]])
                    else:
                        # Если подходящий свободный блок не найден, определяем начало нового блока после последнего занятого
                        last = -1
                        for f in disk["used"]:
                            if f[2] > last:
                                last = f[2]
                        start = last + 1
                        end = start + size - 1
                        # Проверка, что выделенный блок не выходит за пределы общего объёма диска
                        if end >= TOTAL_SIZE:
                            print("Нет места")
                            continue
                        disk["used"].append([name, start, end])
                    # Сортировка списка свободных блоков по начальному адресу
                    disk["free"].sort()
                    # Объединение соседних свободных блоков в один, если они смежны
                    i = 0
                    while i < len(disk["free"]) - 1:
                        if disk["free"][i][1] + 1 >= disk["free"][i + 1][0]:
                            disk["free"][i][1] = max(
                                disk["free"][i][1], disk["free"][i + 1][1]
                            )
                            del disk["free"][i + 1]
                        else:
                            i += 1

            elif cmd == "2":  # Удаление файла
                if not disk["used"]:
                    print("Нет файлов")
                    continue
                name = input("Имя: ").strip()
                # Поиск файла в списке занятых блоков по имени
                found = -1
                for i, f in enumerate(disk["used"]):
                    if f[0] == name:
                        found = i
                        break
                if found == -1:
                    print("Нет файла")
                    continue
                # Извлекаем блок файла и возвращаем его в список свободных
                file = disk["used"].pop(found)
                disk["free"].append([file[1], file[2]])
                disk["free"].sort()
                # Объединяем соседние свободные блоки для оптимизации распределения памяти
                i = 0
                while i < len(disk["free"]) - 1:
                    if disk["free"][i][1] + 1 >= disk["free"][i + 1][0]:
                        disk["free"][i][1] = max(
                            disk["free"][i][1], disk["free"][i + 1][1]
                        )
                        del disk["free"][i + 1]
                    else:
                        i += 1

            elif cmd == "3":  # Просмотр текущего состояния диска
                print("Файлы:")
                # Сортировка списка занятых блоков по начальному адресу для наглядного отображения
                used_files = sorted(
                    disk["used"], key=lambda x: x[1]
                )  # Использование lambda для сортировки по полю начала блока
                # Вывод информации о каждом файле: имя, диапазон адресов и размер в байтах
                for f in used_files:
                    print(f"{f[0]}: {f[1]} - {f[2]} ({f[2] - f[1] + 1} байт)")
                print("Свободно:")
                # Вывод информации о каждом свободном блоке
                for b in disk["free"]:
                    print(f"{b[0]} - {b[1]} ({b[1] - b[0] + 1} байт)")
                # Подсчёт суммарного размера занятых блоков
                used = sum(f[2] - f[1] + 1 for f in disk["used"])
                print(f"Использовано: {used}_{TOTAL_SIZE} ({used/TOTAL_SIZE:.1%})")
            else:
                # Обработка некорректного ввода команды
                print("Неверная команда")
        except Exception as e:
            # Общий обработчик исключений для предотвращения аварийного завершения программы
            print("Ошибка:", e)


if __name__ == "__main__":
    # Точка входа в программу
    main()
