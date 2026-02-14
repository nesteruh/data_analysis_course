---
marp: true
paginate: false

style: |
  table {
    font-size: 0.7em;
  }
  section {
    font-size: 3em;
  }
  section.centered {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }
  .two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    align-items: center;
  }
---
<!-- _class: centered -->
# SQL: Window Functions
## Оконные функции для продвинутой аналитики

---
# Что мы уже знаем

**Агрегатные функции:**
- SUM(), AVG(), COUNT(), MIN(), MAX()
- Работают с GROUP BY
- **Проблема:** теряем детализацию строк

---
# Что такое Window Functions?

**Оконные функции** вычисляют значения для набора строк, **сохраняя детализацию**

```sql
SELECT 
    name,
    category,
    price,
    AVG(price) OVER () as avg_price
FROM products;
```

**Результат:** каждая строка показывает свой товар + среднюю цену по всем товарам

---
# GROUP BY и Window Functions

**GROUP BY:**
```sql
SELECT category, AVG(price)
FROM products
GROUP BY category;
```

**Window Function:**
```sql
SELECT name, category, price,
       AVG(price) OVER (PARTITION BY category) as category_avg
FROM products;
```

---

# Синтаксис OVER()

```sql
функция() OVER (
    PARTITION BY колонка1, колонка2
    ORDER BY колонка3
    ROWS/RANGE ...
)
```

**PARTITION BY** - разделение на группы (аналог GROUP BY)
**ORDER BY** - сортировка внутри окна
**ROWS/RANGE** - рамка окна

---
# ROW_NUMBER() - нумерация строк

**Присваивает уникальный номер каждой строке**

```sql
SELECT 
    name,
    category,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) as row_num
FROM products;
```

**Результат:** товары пронумерованы от самого дорогого к дешёвому

---
# ROW_NUMBER() с PARTITION BY

**Нумерация внутри каждой категории:**

```sql
SELECT 
    name,
    category,
    price,
    ROW_NUMBER() OVER (
        PARTITION BY category 
        ORDER BY price DESC
    ) as rank_in_category
FROM products
ORDER BY category, rank_in_category;
```

---
# RANK() и DENSE_RANK()

**RANK()** - ранг с пропусками при одинаковых значениях
**DENSE_RANK()** - ранг без пропусков

```sql
SELECT 
    name,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) as row_num,
    RANK() OVER (ORDER BY price DESC) as rank,
    DENSE_RANK() OVER (ORDER BY price DESC) as dense_rank
FROM products
ORDER BY price DESC;
```

---
# Разница между ранжирующими функциями

**Пример с одинаковыми ценами:**

| Цена  | ROW_NUMBER | RANK | DENSE_RANK |
|-------|------------|------|------------|
| 75000 | 1          | 1    | 1          |
| 75000 | 2          | 1    | 1          |
| 55000 | 3          | 3    | 2          |
| 45000 | 4          | 4    | 3          |
| 45000 | 5          | 4    | 3          |
| 25000 | 6          | 6    | 4          |

---
# топ 3 товара в категории
```sql
SELECT * FROM (
    SELECT 
        name,
        category,
        price,
        RANK() OVER (
            PARTITION BY category 
            ORDER BY price DESC
        ) as rank
    FROM products
) ranked
WHERE rank <= 3
ORDER BY category, rank;
```

---
# LAG() - предыдущее значение

**LAG()** возвращает значение из предыдущей строки

```sql
SELECT 
    order_id,
    order_date,
    total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) as prev_amount,
    total_amount - LAG(total_amount) OVER (ORDER BY order_date) as diff
FROM orders
ORDER BY order_date;
```

**Использование:** сравнение с предыдущим периодом, расчёт разницы

---
# LEAD() - следующее значение

**LEAD()** возвращает значение из следующей строки

```sql
SELECT 
    order_id,
    customer_id,
    order_date,
    LEAD(order_date) OVER (
        ORDER BY order_date
    ) as next_order_date
FROM orders

```


---
# LAG() и LEAD() с параметрами

```sql
LAG(колонка, смещение, значение_по_умолчанию)
LEAD(колонка, смещение, значение_по_умолчанию)
```

**Пример:**
```sql
SELECT 
    order_id,
    total_amount,
    LAG(total_amount, 1, 0) OVER (ORDER BY order_date) as prev,
    LEAD(total_amount, 1, 0) OVER (ORDER BY order_date) as next
FROM orders;
```


---
# SUM() OVER - накопительная сумма


```sql
SELECT 
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date
    ) as running_total
FROM orders
ORDER BY order_date;
```

**Результат:** общая сумма всех заказов до текущей даты включительно

---
# SUM() OVER с PARTITION BY

**Накопительная сумма по каждому клиенту:**

```sql
SELECT 
    customer_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as customer_running_total
FROM orders
ORDER BY customer_id, order_date;
```


---
# AVG() OVER - скользящее среднее

**Средняя цена товаров до текущего:**

```sql
SELECT 
    name,
    category,
    price,
    ROUND(AVG(price) OVER (
        PARTITION BY category 
        ORDER BY price
    ), 2) as avg_up_to_current
FROM products
ORDER BY category, price;
```


---
# COUNT() OVER - подсчёт в окне

```sql
SELECT 
    c.name,
    o.order_id,
    o.order_date,
    o.total_amount,
    COUNT(*) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as order_number
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.name, o.order_date;
```


---

**FIRST_VALUE()** - первое значение в окне
**LAST_VALUE()** - последнее значение в окне

```sql
SELECT 
    name,
    category,
    price,
    FIRST_VALUE(name) OVER (
        PARTITION BY category 
        ORDER BY price DESC
    ) as most_expensive_in_category
FROM products
ORDER BY category, price DESC;
```


---
# NTILE() - разделение на группы

**NTILE(n)** делит строки на n равных групп (квартили, децили)

```sql
SELECT 
    name,
    price,
    NTILE(4) OVER (ORDER BY price) as price_quartile
FROM products
ORDER BY price;
```


---
# Практический пример: Рост продаж


```sql
SELECT 
    order_date,
    total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) as prev_amount,
    ROUND(
        (total_amount - LAG(total_amount) OVER (ORDER BY order_date)) 
        / LAG(total_amount) OVER (ORDER BY order_date) * 100, 
        2
    ) as growth_pct
FROM orders
ORDER BY order_date;
```

**Результат:** процент роста/падения суммы заказа

---
# Практический пример: Доля от общей суммы


```sql
SELECT 
    order_id,
    total_amount,
    SUM(total_amount) OVER () as total_revenue,
    ROUND(
        total_amount * 100.0 / SUM(total_amount) OVER (), 
        2
    ) as percent_of_total
FROM orders
ORDER BY total_amount DESC;
```

---
# ROWS BETWEEN - рамка окна

**Управление размером окна:**

```sql
ROWS BETWEEN начало AND конец
```

- `UNBOUNDED PRECEDING` - от начала
- `CURRENT ROW` - текущая строка
- `UNBOUNDED FOLLOWING` - до конца
- `N PRECEDING` - N строк назад
- `N FOLLOWING` - N строк вперёд

---
# Скользящее среднее (Moving Average)


```sql
SELECT 
    order_date,
    total_amount,
    ROUND(AVG(total_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as moving_avg_3
FROM orders
ORDER BY order_date;
```

**Использование:** сглаживание колебаний, анализ трендов

---
# Комбинация нескольких Window Functions

```sql
SELECT 
    p.name,
    p.category,
    p.price,
    RANK() OVER (PARTITION BY category ORDER BY price DESC) as rank,
    ROUND(price * 100.0 / SUM(price) OVER (PARTITION BY category), 2) as pct_of_category,
    price - AVG(price) OVER (PARTITION BY category) as diff_from_avg,
    FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price DESC) as highest_priced
FROM products p
ORDER BY category, rank;
```

**Результат:** комплексный анализ товаров в категории

---
# Когда использовать Window Functions?

**Идеальные сценарии:**
- Ранжирование (топ-N в группах)
- Сравнение с предыдущими/следующими значениями
- Накопительные суммы и скользящие средние
- Процент от общей суммы
- Анализ временных рядов


---
# Сравнение подходов

**Без Window Functions (подзапрос):**
```sql
SELECT p1.name, p1.price,
    (SELECT AVG(price) FROM products p2 WHERE p2.category = p1.category)
FROM products p1;
```

**С Window Functions:**
```sql
SELECT name, price,
    AVG(price) OVER (PARTITION BY category)
FROM products;
```

Window Functions: проще, читаемее, часто быстрее

---
# Типичные ошибки

 **Использование WHERE с window functions:**
```sql
SELECT name, price,
    RANK() OVER (ORDER BY price DESC) as rank
WHERE rank <= 5;  -- НЕ РАБОТАЕТ!
```
 **Используйте подзапрос:**
```sql
SELECT * FROM (
    SELECT name, price,
        RANK() OVER (ORDER BY price DESC) as rank
    FROM products
) WHERE rank <= 5;
```

---
# Краткая шпаргалка

| Функция | Описание | Пример |
|---------|----------|--------|
| ROW_NUMBER() | Уникальный номер | Нумерация строк |
| RANK() | Ранг с пропусками | Топ-5 с учётом дублей |
| DENSE_RANK() | Ранг без пропусков | Рейтинг |
| LAG() | Предыдущее значение | Сравнение с прошлым |
| LEAD() | Следующее значение | Прогноз следующего |
| SUM() OVER | Накопительная сумма | Running total |
| AVG() OVER | Скользящее среднее | Moving average |

---
# Краткая шпаргалка (продолжение)

| Функция | Описание | Пример |
|---------|----------|--------|
| FIRST_VALUE() | Первое в группе | Лучший по категории |
| LAST_VALUE() | Последнее в группе | Худший по категории |
| NTILE(n) | Разделить на n групп | Квартили, децили |
| COUNT() OVER | Подсчёт в окне | Номер в последовательности |