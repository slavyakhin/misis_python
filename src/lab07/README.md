# ЛР7 — Поиск, сортировка и измерение времени




## Задание A. Поиск (`search.py`)

### `linear_search(nums, x) -> int`
— индекс первого вхождения, иначе `-1`

``` python
    for i, num in enumerate(nums):
        if num == x:
            return i

    return -1
```

### `binary_search(sorted_nums, x) -> int`
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
 
### `two_sum_brute(nums, target) -> tuple[int, int] | None`
— пара индексов `(i, j)`, `i < j`, или `None`
Решение за O(n^2)

``` python
    for i in range(len(nums)-1):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)

    return None
```

### `two_sum_fast(nums, target) tuple[int, int] | None`
— то же через словарь за один проход; при нескольких ответах выбирается с самым маленьким вторым индексом j.

``` python
    for i in range(len(nums)-1):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)

    return None
```

## Задание B. Сортировки (`sorting.py`)


### `bubble_sort(nums) -> list`
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

### `insertion_sort(nums) - > list`
Сортировка вставками имеет квадратичную сложность O(n^2).

Каждую итерацию добавляется элемент в отсортированный префикс списка. Каждый следующий элемент "вставляется" на нужное место - меняется с соседями за O(n).

``` python
    nums_new = nums.copy()

    for i in range(len(nums_new)):
        for j in range(i, 0, -1):
            if nums_new[j] < nums_new[j-1]:
                nums_new[j], nums_new[j-1] = nums_new[j-1], nums_new[j]
```

### `selection_sort(nums) - > list`
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

### `merge_sort(nums) -> list` **без рекурсии**
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

### `counting_sort(nums, lo, hi)` для целых в известном диапазоне
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

## Задание C. Проверка против эталона (`check.py`)

### `check_sorting(fn, trials=100) -> None`
случайные списки длиной от 0 до 50, значения от −100 до 100, с повторами; `assert fn(nums) == sorted(nums)`; плюс `assert nums == копия` — исходный не изменён

### `check_search() -> None`
на случайных списках `linear_search` против `list.index` (и `-1` против `ValueError`); `binary_search` — на отсортированных, включая `x`, которого нет, и крайние элементы

### `check_two_sum(trials=100) -> None`
оба способа должны давать пару с нужной суммой или оба `None`

`python -m src.lab07.check` — прогоняет всё и печатает `OK: N проверок` или падает на первом расхождении

## Задание D. Бенчмарк (`bench.py`)

---
 - `lab07/README.md` - Отчёт по ЛР7. Должен содержать:
    - таблицу бенчмарка (можно скриншотом, лучше — текстом из CSV)
    - **два абзаца выводов**:
        - почему пузырёк при росте `n` в 10 раз замедляется в ~100 раз, а `sorted` — в ~12
        - почему бинарный поиск бесполезен без предварительной сортировки, и когда она окупается
        - что показал `check.py`: сколько прогонов, нашёл ли расхождения, как исправили

---

Показать в бенчмарке случай, когда подсчёт **обгоняет** `sorted`
график из `bench.csv`: время от `n` для всех сортировок, ось Y — логарифмическая

- одни и те же случайные данные для всех алгоритмов, `random.seed(42)`
- сортировки: `n = 1_000, 10_000, 100_000`; квадратичные на 10⁵ — ограничить (`> 60 с` в таблице допустимо)
- поиск: список из 100 000, 10 000 случайных запросов; для бинарного — **включить** время сортировки отдельной строкой
- Two Sum: `n = 1_000, 10_000`, `target` гарантированно существует
- таблица в консоль с выравниванием (f-строки из Л1) и `data/lab07/bench.csv` через `write_csv`
