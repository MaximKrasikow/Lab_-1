# ======== КОНФИГУРАЦИЯ ========
TOTAL_SIZE = 360 * 1024  # Общий размер диска в байтах (360 Кбайт)
MIN_SIZE = 18  # Минимальный размер файла в байтах
MAX_SIZE = 32 * 1024  # Максимальный размер файла в байтах (32 Кбайт)
# ==============================

# Состояние диска
disk = {
    "files": [],  # Список занятых блоков: [[имя, начало, конец], ...]
    "free": [[0, TOTAL_SIZE - 1]]  # Список свободных блоков: [[начало, конец], ...]
}

def merge_blocks():
    """
    Объединяет смежные свободные блоки памяти.
    """
    disk["free"].sort()  # Сортируем свободные блоки по началу
    i = 0
    while i < len(disk["free"]) - 1:
        a, b = disk["free"][i], disk["free"][i + 1]
        if a[1] + 1 >= b[0]:  # Если блоки смежны
            disk["free"][i][1] = max(a[1], b[1])  # Объединяем блоки
            del disk["free"][i + 1]  # Удаляем второй блок
        else:
            i += 1  # Переходим к следующему блоку

def add_file(name, size):
    """
    Добавляет файл на диск.
    
    :param name: Имя файла
    :param size: Размер файла в байтах
    """
    # Находим наилучший свободный блок для размещения файла
    best = min(
        (b for b in disk["free"] if b[1] - b[0] + 1 >= size),
        key=lambda x: x[1] - x[0],
        default=None,
    )
    if best:
        start, end = best[0], best[0] + size - 1  # Определяем начальную и конечную позиции файла
        disk["free"].remove(best)  # Удаляем выбранный блок из списка свободных
        if end < best[1]:  # Если блок не полностью занят
            disk["free"].append([end + 1, best[1]])  # Добавляем оставшуюся часть блока
        disk["files"].append([name, start, end])  # Добавляем файл в список занятых блоков
    else:
        # Если нет подходящего свободного блока, пытаемся добавить файл в конец диска
        last = max(f[2] for f in disk["files"]) if disk["files"] else -1  # Находим последний занятый блок
        start, end = last + 1, last + size  # Определяем начальную и конечную позиции файла
        if end >= TOTAL_SIZE:  # Проверяем, достаточно ли места
            raise MemoryError("Недостаточно места")
        disk["files"].append([name, start, end])  # Добавляем файл в список занятых блоков
    merge_blocks()  # Объединяем смежные свободные блоки
    disk["files"].sort(key=lambda x: x[1])  # Сортируем список занятых блоков по началу

def delete_file(name):
    """
    Удаляет файл с диска.
    
    :param name: Имя файла
    """
    for i, f in enumerate(disk["files"]):
        if f[0] == name:  # Находим файл по имени
            file = disk["files"].pop(i)  # Удаляем файл из списка занятых блоков
            disk["free"].append([file[1], file[2]])  # Добавляем освободившийся блок в список свободных
            merge_blocks()  # Объединяем смежные свободные блоки
            return
    raise ValueError("Файл не найден")  # Если файл не найден, выбрасываем исключение

def print_disk():
    """
    Выводит текущее состояние диска.
    """
    print("\nЗанято:")
    for f in sorted(disk["files"], key=lambda x: x[1]):  # Сортируем и выводим занятые блоки
        print(f"{f[0]}: {f[1]}-{f[2]} ({f[2] - f[1] + 1} байт)")
    print("\nСвободно:")
    for b in disk["free"]:  # Выводим свободные блоки
        print(f"{b[0]}-{b[1]} ({b[1] - b[0] + 1} байт)")
    used = sum(f[2] - f[1] + 1 for f in disk["files"])  # Считаем использованное место
    print(f"\nИспользовано: {used}/{TOTAL_SIZE} ({used / TOTAL_SIZE:.1%})")  # Выводим общую статистику

def main():
    """
    Интерфейс управления диском.
    """
    while True:
        print("\n1. Добавить 2. Удалить 3. Просмотр 4. Выход")
        cmd = input("> ").strip()  # Получаем команду от пользователя
        try:
            if cmd == "1":
                name = input("Имя: ").strip()  # Вводим имя файла
                if any(f[0] == name for f in disk["files"]):  # Проверяем, не занят ли уже этот файл
                    print("Ошибка: имя занято")
                    continue
                size = int(input("Размер: "))  # Вводим размер файла
                if not MIN_SIZE <= size <= MAX_SIZE:  # Проверяем, допустим ли размер файла
                    print(f"Допустимо {MIN_SIZE}-{MAX_SIZE}")
                    continue
                add_file(name, size)  # Добавляем файл
                print("Файл добавлен")
            elif cmd == "2":
                name = input("Имя: ").strip()  # Вводим имя файла
                delete_file(name)  # Удаляем файл
                print("Файл удален")
            elif cmd == "3":
                print_disk()  # Выводим состояние диска
            elif cmd == "4":
                break  # Выходим из программы
        except Exception as e:
            print(f"Ошибка: {str(e)}")  # Обрабатываем исключения

if __name__ == "__main__":
    main()  # Запускаем основную функцию программы