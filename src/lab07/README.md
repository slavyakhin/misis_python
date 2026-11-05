# ЛР7 — Поиск, сортировка и измерение времени

# Задание A. Поиск (`search.py`)

## `linear_search(nums, x) -> int`
— индекс первого вхождения, иначе `-1`

``` python
    for i, num in enumerate(nums):
        if num == x:
            return i

    return -1
```

## `binary_search(sorted_nums, x) -> int`
— индекс любого вхождения, иначе `-1`;

``` python
    if not sorted_nums:
        return -1

    l, r = 0, len(sorted_nums)
    while (r-l > 1):
        m = (l+r) // 2
        if sorted_nums[m] <= x:
            l = m
        else:
            r = m
    if sorted_nums[l] == x:
        return l
    return -1
```
 
## `two_sum_brute(nums, target) -> tuple[int, int] | None`
— пара индексов `(i, j)`, `i < j`, или `None`
Решение за O(n^2)

``` python
    for i in range(len(nums)-1):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)

    return None
```

## `two_sum_fast(nums, target) tuple[int, int] | None`
— то же через словарь за один проход; при нескольких ответах выбирается с самым маленьким вторым индексом j.

``` python
    for i in range(len(nums)-1):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)

    return None
```
<br><br>

# Задание B. Сортировки (`sorting.py`)

## `bubble_sorted(nums) -> list`
Сортировка пузырьком имеет квадратичную сложность O(n^2).

Пока список не отсортирован, проходимся по нему, сравнивая пары соседов. Если пара не упорядочена, меняем соседей местами. Таким образом самый крупный неотсортированный элемент "всплывает" на своё место в конце списка. Конец списка отсортирован. Если нечего менять местами, весь список отсортирован.

``` python
    unsorted_count = len(nums_new)
    swapped = True
    while swapped:
        swapped = False
        for i in range(unsorted_count-1):
            if nums_new[i+1] < nums_new[i]:
                nums_new[i], nums_new[i+1] = nums_new[i+1], nums_new[i]
                swapped = True
        unsorted_count -= 1
```

## `insertion_sorted(nums) - > list`
Сортировка вставками имеет квадратичную сложность O(n^2).

Каждую итерацию добавляется элемент в отсортированный префикс списка. Каждый следующий элемент "вставляется" на нужное место - меняется с соседями за O(n).

``` python
    nums_new = nums.copy()

    for i in range(len(nums_new)):
        for j in range(i, 0, -1):
            if nums_new[j] < nums_new[j-1]:
                nums_new[j], nums_new[j-1] = nums_new[j-1], nums_new[j]
```

## `selection_sorted(nums) - > list`
Сортировка выбором имеет квадратичную сложность O(n^2).

Префикс отсортирован. n раз выбирается минимальный элемент за O(n) и меняется местами с элементом сразу после префикса.

``` python
    sorted_count = 0
    while sorted_count < len(nums_new):
        cur_min_ind = sorted_count
        for i in range(sorted_count, len(nums_new)):
            if nums_new[i] < nums_new[cur_min_ind]:
                cur_min_ind = i
        nums_new[sorted_count], nums_new[cur_min_ind] = nums_new[cur_min_ind], nums_new[sorted_count]
        sorted_count += 1
```

## `merge_sorted(nums) -> list` **без рекурсии**
Сортировка слиянием имеет сложность O(nlogn)

Слияние двух отсортированных списков имеет сложность O(n).
Слияние подсписков друг с другом также имеет сложность O(n).

Поделим список сначала на пары элементов - отсортированные списки длины один. Сольём все пары. Получаются отсортированные подсписки длины 2.
Теперь возьмём пары подсписков длины 2 элементов и сольём их. Затем длины 4, 8,... Таких итераций будет logn (логарифм с основанием 2). На последней итерации будем сливать две (возможно неравные) отсортированные половины списка.


``` python
    section_len = 1
    while section_len < len(nums_new):

        for section_a_begin in range(0, len(nums_new), section_len*2):
            section_a_end = min(section_a_begin + section_len, len(nums_new))
            section_b_begin = section_a_end
            section_b_end = min(section_b_begin + section_len, len(nums_new))

            merged_sections = []

            i, j = section_a_begin, section_b_begin
            while i < section_a_end and j < section_b_end:
                if nums_new[i] < nums_new[j]:
                    merged_sections.append(nums_new[i])
                    i += 1
                else:
                    merged_sections.append(nums_new[j])
                    j += 1
            while i < section_a_end:
                merged_sections.append(nums_new[i])
                i += 1
            while j < section_b_end:
                merged_sections.append(nums_new[j])
                j += 1

            for i, value in enumerate(merged_sections):
                nums_new[section_a_begin + i] = value
        
        section_len *= 2
```

## `counting_sorted(nums, lo, hi)` для целых в известном диапазоне
Сортировка подсчётом имеет сложность O(n), однако работает только если входные данные ограничены (варианты с хэш-функциями пока не рассматриваем).

Для каждого значения храним количество его вхождений.

``` python
    counter = [0] * (hi + 1 - lo)
    for value in nums:
        if value < lo or hi < value:
            raise ValueError("nums value not in range [lo, hi]")
        counter[value - lo] += 1

    result = []
    for i, count in enumerate(counter):
        result.extend([i+lo] * count)
```
<br><br>

# Задание C. Проверка против эталона (`check.py`)

В ходе проверки `check` некоторые функции были доработаны. В особенности полезной оказалась сверка своего `binary_search` с `index`. Понадобилось как минимум 3 прогона, чтобы разобраться с upper_bound и lower_bound вариантами бинарного поиска. Результат бинпоиска варьируется в зависимости от строгости условия цикла `while(l < r)` или `while(l <= r)`, от условия в теле цикла и от выбора возвращаемого индекса `l` или `r`.

Таким образом был выбран вариант `lower_bound` - первый в списке или первый больший.

## `check_sorting(fn, trials=100) -> None`

Генерирует случайные списки, выполняет данную сортовку, сравнивает результат с `sorted`
``` python
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {nums}: {result}"
        assert nums == original, f"{fn.__name__} изменила исходный список"
```

## `check_search() -> None`

Генерирует случайные списки, случайно выбирает цель из списка или выбирает число вообще не из диапазона. В случаее, если числа нет в списке, `index` поднимает ошибку, проверяемые функции возвращают `-1`.

``` python
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        nums.sort()

        if not n == 0:
            x = random.choice((nums[random.randint(0, n-1)], 150))
        else:
            x = 150

        result = fn(nums, x)
        try:
            index_result = nums.index(x)
        except ValueError: # not in list
            index_result = -1
        assert result == index_result, f"{fn.__name__} ошиблась на {nums}, {x}: {result}"
```


## `check_two_sum(trials=100) -> None`

Случайно выбирает пару числе из списка и складывает. Решения "two sum" могут быть разные, поэтому сравниваем только факт нахождения и сумму.

``` python
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        i, j = random.randint(0, n-1), random.randint(0, n-1)
        su = random.choice((nums[i] + nums[j], 201))

        result_brute = two_sum_brute(nums, su)
        result_fast = two_sum_fast(nums, su)

        assert (result_brute is None and result_fast is None) \
             or (result_brute is not None and result_fast is not None \
                 and nums[result_brute[0]] + nums[result_brute[1]] == nums[result_fast[0]] + nums[result_fast[1]]), f"результаты не совпадают на {nums}: {result_brute} != {result_fast}"
```
<br><br>

# Задание D. Бенчмарк (`bench.py`)

Модуль замеряющий время выполнения функций при помощи `timeit`.

## `_timeit_worker`
Для реализации __timeout__  функция `timeit` выполняется воркером в подпроцессе. `timeit` выполняется для каждого запроса - пары `args, kwargs`.

Timeit выполняет по **number** одинаковых запусков и суммирует их время выполнения, повторяет это **repeat** раз. Выбираем лучшее из **repeat** повторений и делим сумму на **number** - получаем среднее арифметическое время. Это позволяет минимизировать погрешность измерений и ошибки нестабильной системы. Однако стоит учитывать, что общее время исполнения увеличивается **в number * repeat раз**! Что критично для долгих алгоритмов и больших объёмов данных. Например для O(n^2) при n=10^5 будем использовать только одно измерение.

``` python
def _timeit_worker(
    writer_conn: Connection,
    fn: Callable,
    reqs: Sequence[tuple[tuple, dict]], # Sequence of pairs (args, kwargs)
    number: int,
    repeat: int,
) -> None:
    with writer_conn: # Close connection automatically
        total_time = 0
        for args, kwargs in reqs:
            times = timeit.repeat(lambda: fn(*args, **kwargs), number=number, repeat=repeat)
            best = min(times) / number
            total_time += best
            
        writer_conn.send(total_time)
```

## `exec_worker_with_timeout`
Запускает на выполнение переданную функцию в дочернем процессе. В случае исхода __timeout__ поднимается исключение `TimeoutError`. Возвращает результат, переданный дочерним процессом в канал `mp.Pipe`.

``` python
def exec_worker_with_timeout(
    worker: Callable,
    args: tuple = (),
    kwargs: dict = {},
    timeout: float | int = TIMEOUT,
):
    reader_conn, writer_conn = mp.Pipe(duplex=False)

    process = mp.Process(target=worker, args=(writer_conn, *args), kwargs=kwargs)

    try:
        process.start()
        writer_conn.close()

        if not reader_conn.poll(timeout):
            raise TimeoutError("Timeout exceeded.")

        try:
            result = reader_conn.recv()
        except EOFError:
            raise RuntimeError("Worker process crashed before sending data.")

        return result

    finally:
        reader_conn.close()
        writer_conn.close()

        if process.is_alive():
            process.terminate()
            process.join(timeout=1)

        if process.is_alive():
            process.kill()

        process.join()
```

## `src.lib.gen_numbers`
Дополнительный скрипт для генерации входных данных

``` python
write_csv([(random.randint(min_value, max_value),) for _ in range(n)], out_path , header=HEADER)
```
<br><br>

## `bench`

Запускает один "тестовый случай" — **"test case"** (см. подзаголовок test case). Вызывает `exec_worker_with_timeout`, в качестве воркера `_timeit_worker`, в аргументы тестируемая функция и запросы.

Возвращает время выполнения тестов или `None`, если истёк **timeout**.

``` python
def bench(
    fn: Callable,
    reqs: Sequence[tuple[tuple, dict]], # Sequence of pairs (args, kwargs)
    repeat: int = REPEAT,
    number: int = NUMBER,
    timeout: float | int = TIMEOUT,
) -> float | None:

    try:
        t = exec_worker_with_timeout(
            worker=_timeit_worker,
            kwargs={
                "fn": fn,
                "reqs": reqs,
                "number": number,
                "repeat": repeat
            },
            timeout=timeout
            )
        return t
    except TimeoutError:
        return None
```

## test cases
Для удобного декларативного описания тестов определена структура `test` и `test case` - словари.

- `test` — прообраз строки в отчетной таблице.

- `test case` — прообраз ячейки в отчетной таблице.

#### Спецификация test
| Поле | Type hint | Значение | Пример |
|------|-----------|----------|--------|
| **"name"** | `str` | название теста | "O(n^2)" |
| **"fn"** | `Callable`  | тестируемая функция | `bubble_sorted` |
| **"complexity"** | `str` | сложность | "O(n^2)" |
| **"cases"** | `list[test case]` | список тестовый случаев | см. таблицу о test case

#### Спецификация test case
| Поле | Type hint | Значение | Пример |
|------|-----------|----------|--------|
| **"name"** | `str` | название тестового случая (колонки таблицы) | "n=10^3" |
| **"reqs"** | `list[tuple[tuple, dict]]` | список запросов - пар **(args, kwargs)** | `[((nums), {"lo": 10}), ((), {})]` |
| **"args"** | `tuple` | **args** (в случае одного запроса) | `(nums)` |
| **"kwargs"** | `dict` | **kwargs** (в случае одного запроса) | `{"lo": 10, "hi": 20}` |
| **"number"** | `int` | `timeit` number | 5 |
| **"repeat"** | `int` | `timeit` repeat | 10 |
| **"timeout"** | `float \| int` | таймаут, секундд | 60 |

``` python
{
    "name": "Bubble sort",
    "fn": bubble_sorted,
    "complexity": "O(n^2)",
    "cases": [
        {
            "name": "n=10^3",
            "kwargs": {"nums": numbers_s},
            "number": 5,
            "repeat": 10,
        },
        {
            "name": "n=10^4",
            "kwargs": {"nums": numbers_m},
            "number": 2,
            "repeat": 2,
        },
        {
            "name": "n=10^5",
            "kwargs": {"nums": numbers_l},
            "number": 1,
            "repeat": 1,
        }
    ],
},
```

## main
Скрипт `bench` выполняет тесты, выводит результаты в консоль, пишет в **csv** и строит график.

```python
    for i, line in enumerate(tests_table):
        result_recs[i]["Algorithm"] = line["name"]
        result_recs[i]["Complexity"] = line["complexity"]

        for j, case in enumerate(line["cases"]):
            t = bench(
                fn=line["fn"],
                reqs=case.get("reqs") or [(case.get("args", ()), case.get("kwargs", {}))],
                number=case.get("number", NUMBER),
                repeat=case.get("repeat", REPEAT),
                timeout=case.get("timeout", args.timeout),
            )

            t_str = _fmt_time(t, args.timeout, spec=f".{args.precision}f")
            result_recs[i][case["name"]] = t_str
    
    rows = recs_to_rows(result_recs)

    print_table(rows)

    if args.csv:
        write_csv(rows, Path(args.csv_str))

    if args.plot:
        show_bench_plot(result_recs)
```

## `src.lib.fmt_table`
Табличный вывод в консоль выполняется f-строками

``` python
    print(f"┌─{'─┬─'.join('─' * width for width in widths)}─┐")
    print(f"│ {' │ '.join(f'{value:^{widths[i]}}' for i, value in enumerate(rows[0]))} │")
    for row in rows[1:]:
        print(f"├─{'─┼─'.join('─' * width for width in widths)}─┤")
        print(f"│ {' │ '.join(f'{value:^{widths[i]}}' for i, value in enumerate(row))} │")
    print(f"└─{'─┴─'.join('─' * width for width in widths)}─┘")
```

![bench_run.png](../../misc/img/lab07/bench_run.png)

### __Почему пузырёк при росте `n` в 10 раз замедляется в ~100 раз, а `sorted` — в ~12?__

Согласно асимптотике пузырька, количество операций $n$ на выполнение ограничено $C * n^2, С - конечное\ число$. $(10*n) ^ 2 = 100 * n ^ 2 $.

Тогда как для `Timsort` асимптотика $O(nlong)$: $10n*log(10n) \approx 10n*log10n $ В разных случаях и для разных видов логарифмической сортировки могут быть разные погрешности порядка 10-30 раз.

### Замеры
`(.venv) slavyakhin@HP-Laptop:~/MISiS/misis_python$ python -m src.lab07.bench --timeout 2400 --csv --plot`

Чтобы получить достоверный график выбран достаточно большой `timeout`, чтобы все алгоритмы полностью выполнились.

|Algorithm     |Complexity|n=10^3|n=10^4 |n=10^5   |
|--------------|----------|------|-------|---------|
|Bubble sort   |O(n^2)    |0.0546|3.8320 |353.3997 |
|Insertion sort|O(n^2)    |0.0257|2.9197 |331.4235 |
|Selection sort|O(n^2)    |0.0144|1.6869 |192.7028 |
|Tim sort      |O(n logn) |0.0001|0.0015 |0.0215   |
|Merge sort    |O(n logn) |0.0012|0.0173 |0.2214   |
|Counting sort |O(n)      |0.0026|0.0032 |0.0087   |
|Linear search |O(n)      |-     |-      |1.9298   |
|Binary search |O(n)      |-     |-      |0.0153   |
|Two sum brute |O(n^2)    |0.2361|19.3090|1703.8976|
|Two sum fast  |O(n)      |0.0016|0.0232 |0.1264   |

На графике заметно как `Two sum fast` и `Counting sort` **O(n)** "обгоняет" `Merge_sort` и `Tim_sort` соответственно  **O(n logn)**  на достаточно больших данных.

![plot](../../misc/img/lab07/plot.png)
