# ЛР2 — Коллекции и матрицы (list/tuple/set/dict)

Репозиторий переведен на модульную архитектуру для удобного запуска тестов, импорта переиспользуемых функций. Добавлены файлы **\_\_init\_\_.py**, обозначающие модуль.

Переиспользуемые функции сохранены в **src/lib**.

Для тестирования выбран фреймворк **pytest**. Для запуска тестов `python3 -m pytest tests/lab02` (из корня проекта).

## Задание 1 — `arrays.py`

Реализованы три функции:

### 1. `min_max(nums: list[float | int]) -> tuple[float | int, float | int]`
Сперва принимает первый елемент за максимум и минимум. Затем в цикле перебирает каждый элемент и сравнивает с текущим результатом, выбирая самый маленьких и самый большой элементы в списке.
``` python
    cur_min, cur_max = nums[0], nums[0]
    for num in nums:
        if num < cur_min:
            cur_min = num
        if cur_max < num:
            cur_max = num
```

![min_max_run](../../misc/img/lab02/min_max_run.png)

### 2. `unique_sorted(nums: list[float | int]) -> list[float | int] `
Уникальность элементов достигается явным приведением списка к set и обратно - неупорядоченному набору уникальных элементов (хэш-таблица). Затем список сортируется при помощи сортировки слиянием, дополнительно реализованной в src.lib.merge_sort.
``` python
    unique_nums = list(set(nums))
    unique_nums = merge_sorted(unique_nums)
```

![unique_sorted_run](../../misc/img/lab02/unique_sorted_run.png)

### 3. `flatten(mat: list[list | tuple]) -> list`
Сериализация матрицы. В двух циклах перебираются все элементы матрицы и поочередно добавляются в результирующий список.
``` python
    result = []
    for row in mat:
        for element in row:
            result.append(element) # any type allowed
```

![flatten_run](../../misc/img/lab02/flatten_run.png)

В каждой функции проверяется тип вводимых значений: тип коллекции и каждого их элемента. min_max дополнительно поднимает `ValueError` при пустом списке на входе.

## Задание B — `matrix.py`

Создарны три фукции:

### 1. `transpose(mat: list[list[float | int]]) -> list[list]`
Транспонирование матрицы. Строго проверяются типы входного списка. Результат - новый список списков, созданный при помощи генераторов.
``` python
    result = [ [mat[i][j] for i in range(len(mat))]
              for j in range(len(mat[0])) ]
```

![transpose_run](../../misc/img/lab02/transpose_run.png)

### 2. `row_sums(mat: list[list[float | int]]) -> list[float]`
Функция возвращает вектор - суммы элементов в строках. Строго проверяются типы входного списка. Результат формируется в заранее подготовленном списке длины столбца.
``` python
    result = [ 0.0 for _ in range(len(mat)) ]

    for i, row in enumerate(mat):
        for element in row:
            result[i] += float(element)
```
Заметим, что стандартный вывод в REPL не точно совпадает с требуемым результатам - целые числа сопровождаются лишними нулями в десятичной части. Чтобы выводить целые `float` без нулей, напишем обертку над `float` `FloatIntFormatted` (поменяем `__repr__`) и `displayhook` к нему, который будет проверять, является ли число целым. Обёртку можно найти в _lib/float_int_formatted.py_

![row_sums_run](../../misc/img/lab02/row_sums_run.png)

### 3. `col_sums(mat: list[list[float | int]]) -> list[float]`
Функция возвращает вектор - суммы элементов в столбцах. Строго проверяются типы входного списка. Результат формируется в заранее подготовленном списке длины строки.
``` python
    result = [ 0.0 for _ in range(len(mat[0]))]

    for row in mat:
        for j, element in enumerate(row):
            result[j] += float(element)
```

![col_sums_run](../../misc/img/lab02/col_sums_run.png)

## Задание C — `tuples.py`
Создан _type alias_ на кортеж (см. PEP 695 pytohn 3.12) `Rec` - тип записи студента.
\
\
`format_record(rec: Rec) -> str`\
возвращает строку вида\
`Иванов И.И., гр. BIVT-25, GPA 4.60`
Строго проверяются типы входной записи. Проверяется попадает ли _gpa_ в отрезок [0.0, 5.0].\
``` python
    if rec[2] <= 0.0 or 5.5 <= rec[2]:
        raise ValueError("gpa must be in [0.0, 5.0]")
```
В ФИО полной остаётся только фамилия, с первой заглавной и остальными строчными буквами (метод `capitalize()`). К фамилии добавляются инициалы имени и отчества (при наличии) конкатенацией строк оператором сложения `+`.
``` python
    fio_list = rec[0].split()
    if len(fio_list) < 2 or 3 < len(fio_list):
        raise ValueError("fio must contain 2 or 3 words")

    fio_str = fio_list[0].capitalize() + ' ' + ''.join(name[0].upper() + '.' for name in fio_list[1:])
```

![format_record_run](../../misc/img/lab02/format_record_run.png)
