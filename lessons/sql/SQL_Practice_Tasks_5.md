# Практические задачи по SQL 
## Window Functions (Оконные функции)

---

### Задача 1: Нумерация товаров по цене
Пронумеруйте все товары от самого дорогого к самому дешёвому. Используйте ROW_NUMBER().

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) as row_num
FROM products
ORDER BY row_num;
```
</details>

---

### Задача 2: Топ-3 товара в каждой категории
Найдите 3 самых дорогих товара в каждой категории. Используйте RANK() с PARTITION BY.

<details>
<summary>Решение</summary>

```sql
SELECT *
FROM (
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
</details>

---

### Задача 3: Разница между ранжирующими функциями
Выведите топ-10 товаров по цене, показав ROW_NUMBER, RANK и DENSE_RANK. Объясните разницу.

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) as row_num,
    RANK() OVER (ORDER BY price DESC) as rank,
    DENSE_RANK() OVER (ORDER BY price DESC) as dense_rank
FROM products
ORDER BY price DESC
LIMIT 10;
```

**Разница:**
- ROW_NUMBER: всегда уникальный номер (1, 2, 3, 4...)
- RANK: одинаковые значения получают одинаковый ранг, следующий пропускается (1, 1, 3, 4...)
- DENSE_RANK: одинаковые значения получают одинаковый ранг, следующий НЕ пропускается (1, 1, 2, 3...)

</details>

---

### Задача 4: Номер товара в своей категории
Для каждого товара покажите его порядковый номер внутри категории, отсортированный по возрастанию цены.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    name,
    price,
    ROW_NUMBER() OVER (
        PARTITION BY category 
        ORDER BY price ASC
    ) as num_in_category
FROM products
ORDER BY category, num_in_category;
```
</details>

---

### Задача 5: Средняя цена и отклонение
Для каждого товара покажите среднюю цену в его категории и отклонение товара от этой средней.

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price,
    ROUND(AVG(price) OVER (PARTITION BY category), 2) as category_avg,
    ROUND(price - AVG(price) OVER (PARTITION BY category), 2) as diff_from_avg
FROM products
ORDER BY category, price DESC;
```
</details>

---

### Задача 6: Доля цены товара от общей суммы категории
Рассчитайте, какую долю (в процентах) составляет цена каждого товара от суммы цен всех товаров в его категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price,
    SUM(price) OVER (PARTITION BY category) as category_total,
    ROUND(
        price * 100.0 / SUM(price) OVER (PARTITION BY category), 
        2
    ) as percent_of_category
FROM products
ORDER BY category, percent_of_category DESC;
```
</details>

---

### Задача 7: Накопительная сумма заказов
Рассчитайте накопительную сумму (running total) всех заказов по дате. Покажите дату, сумму заказа и накопительный итог.

<details>
<summary>Решение</summary>

```sql
SELECT 
    order_date::date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date
    ) as running_total
FROM orders
ORDER BY order_date;
```
</details>

---

### Задача 8: Накопительная сумма по клиентам
Для каждого клиента рассчитайте накопительную сумму его заказов. Покажите имя клиента, дату заказа, сумму и накопительный итог.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    o.order_date::date,
    o.total_amount,
    SUM(o.total_amount) OVER (
        PARTITION BY c.customer_id 
        ORDER BY o.order_date
    ) as customer_running_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.name, o.order_date;
```
</details>

---

### Задача 9: Сравнение с предыдущим заказом
Для каждого заказа покажите сумму предыдущего заказа (по дате) и разницу между текущим и предыдущим. Используйте LAG().

<details>
<summary>Решение</summary>

```sql
SELECT 
    order_id,
    order_date::date,
    total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) as prev_amount,
    total_amount - LAG(total_amount) OVER (ORDER BY order_date) as diff
FROM orders
ORDER BY order_date;
```
</details>

---

### Задача 10: Процент роста от предыдущего заказа
Рассчитайте процент изменения суммы каждого заказа по сравнению с предыдущим.

<details>
<summary>Решение</summary>

```sql
SELECT 
    order_id,
    order_date::date,
    total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) as prev_amount,
    ROUND(
        (total_amount - LAG(total_amount) OVER (ORDER BY order_date)) * 100.0
        / NULLIF(LAG(total_amount) OVER (ORDER BY order_date), 0),
        2
    ) as growth_pct
FROM orders
ORDER BY order_date;
```

**Примечание:** NULLIF предотвращает деление на ноль.

</details>

---

### Задача 11: Следующий заказ клиента
Для каждого заказа покажите дату следующего заказа этого же клиента. Используйте LEAD().

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    o.order_id,
    o.order_date::date,
    LEAD(o.order_date) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    )::date as next_order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.name, o.order_date;
```
</details>

---

### Задача 12: Время между заказами
Рассчитайте количество дней между текущим и следующим заказом для каждого клиента.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    o.order_id,
    o.order_date::date,
    LEAD(o.order_date) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    )::date as next_order_date,
    LEAD(o.order_date) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    )::date - o.order_date::date as days_to_next_order
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.name, o.order_date;
```
</details>

---

### Задача 13: Номер заказа клиента
Для каждого заказа покажите, какой это по счёту заказ данного клиента (1-й, 2-й, 3-й...).

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    o.order_id,
    o.order_date::date,
    o.total_amount,
    ROW_NUMBER() OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    ) as order_number
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.name, order_number;
```
</details>

---

### Задача 14: Первый и последний заказ клиента
Для каждого заказа покажите дату первого и последнего заказа этого клиента. Используйте FIRST_VALUE() и LAST_VALUE().

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    o.order_date::date,
    o.total_amount,
    FIRST_VALUE(o.order_date) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
    )::date as first_order_date,
    LAST_VALUE(o.order_date) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    )::date as last_order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.name, o.order_date;
```

**Важно:** ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING нужен для LAST_VALUE, чтобы видеть все строки в партиции.

</details>

---

### Задача 15: Самый дорогой товар в категории
Для каждого товара покажите название самого дорогого товара в его категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price,
    FIRST_VALUE(name) OVER (
        PARTITION BY category 
        ORDER BY price DESC
    ) as most_expensive_in_category,
    FIRST_VALUE(price) OVER (
        PARTITION BY category 
        ORDER BY price DESC
    ) as highest_price
FROM products
ORDER BY category, price DESC;
```
</details>

---

### Задача 16: Квартили товаров по цене
Разделите все товары на 4 квартиля по цене. Используйте NTILE(4).

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price,
    NTILE(4) OVER (ORDER BY price) as price_quartile,
    CASE NTILE(4) OVER (ORDER BY price)
        WHEN 1 THEN 'Очень дешёвые (Q1)'
        WHEN 2 THEN 'Дешёвые (Q2)'
        WHEN 3 THEN 'Дорогие (Q3)'
        WHEN 4 THEN 'Очень дорогие (Q4)'
    END as quartile_label
FROM products
ORDER BY price;
```
</details>

---

### Задача 17: Топ-5 товаров по продажам
Найдите 5 самых продаваемых товаров (по количеству). Покажите название, категорию, количество продаж и ранг.

<details>
<summary>Решение</summary>

```sql
SELECT *
FROM (
    SELECT 
        p.name,
        p.category,
        COALESCE(SUM(oi.quantity), 0) as total_sold,
        RANK() OVER (ORDER BY COALESCE(SUM(oi.quantity), 0) DESC) as rank
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.name, p.category
) ranked
WHERE rank <= 5
ORDER BY rank;
```
</details>

---

### Задача 18: Ранжирование товаров в категории по продажам
Для каждого товара покажите его ранг по продажам внутри своей категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.name,
    p.category,
    COALESCE(SUM(oi.quantity), 0) as total_sold,
    RANK() OVER (
        PARTITION BY p.category 
        ORDER BY COALESCE(SUM(oi.quantity), 0) DESC
    ) as rank_in_category
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY p.category, rank_in_category;
```
</details>

---

### Задача 19: Доля выручки каждого заказа
Рассчитайте, какую долю (в процентах) составляет каждый заказ от общей выручки.

<details>
<summary>Решение</summary>

```sql
SELECT 
    order_id,
    order_date::date,
    total_amount,
    SUM(total_amount) OVER () as total_revenue,
    ROUND(
        total_amount * 100.0 / SUM(total_amount) OVER (), 
        2
    ) as percent_of_total
FROM orders
ORDER BY percent_of_total DESC;
```
</details>

---

### Задача 20: Доля выручки по городам
Рассчитайте долю выручки каждого города от общей выручки всех заказов.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.city,
    SUM(o.total_amount) as city_revenue,
    SUM(SUM(o.total_amount)) OVER () as total_revenue,
    ROUND(
        SUM(o.total_amount) * 100.0 / SUM(SUM(o.total_amount)) OVER (), 
        2
    ) as percent_of_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY percent_of_total DESC;
```
</details>

---

### Задача 21: Скользящее среднее (Moving Average)
Рассчитайте скользящее среднее за 3 заказа (текущий и два предыдущих) для сумм заказов.

<details>
<summary>Решение</summary>

```sql
SELECT 
    order_id,
    order_date::date,
    total_amount,
    ROUND(AVG(total_amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as moving_avg_3
FROM orders
ORDER BY order_date;
```
</details>

---

### Задача 22: Топ клиентов по городам
Найдите топ-3 клиентов по общей сумме заказов в каждом городе.

<details>
<summary>Решение</summary>

```sql
SELECT *
FROM (
    SELECT 
        c.city,
        c.name,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as total_spent,
        RANK() OVER (
            PARTITION BY c.city 
            ORDER BY SUM(o.total_amount) DESC
        ) as rank_in_city
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.city, c.name
) ranked
WHERE rank_in_city <= 3
ORDER BY city, rank_in_city;
```
</details>

---

### Задача 23: Сравнение заказа со средним по клиенту
Для каждого заказа покажите, больше или меньше он средней суммы заказов этого клиента.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    o.order_id,
    o.total_amount,
    ROUND(AVG(o.total_amount) OVER (
        PARTITION BY o.customer_id
    ), 2) as customer_avg,
    CASE 
        WHEN o.total_amount > AVG(o.total_amount) OVER (PARTITION BY o.customer_id) 
        THEN 'Выше среднего'
        WHEN o.total_amount < AVG(o.total_amount) OVER (PARTITION BY o.customer_id) 
        THEN 'Ниже среднего'
        ELSE 'Средний'
    END as comparison
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.name, o.order_date;
```
</details>

---

### Задача 24: Распределение товаров по ценовым сегментам в категориях
Для каждой категории разделите товары на 3 сегмента (дешёвые, средние, дорогие) с помощью NTILE(3).

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    name,
    price,
    NTILE(3) OVER (
        PARTITION BY category 
        ORDER BY price
    ) as price_tier,
    CASE NTILE(3) OVER (PARTITION BY category ORDER BY price)
        WHEN 1 THEN 'Бюджетный'
        WHEN 2 THEN 'Средний'
        WHEN 3 THEN 'Премиум'
    END as tier_label
FROM products
ORDER BY category, price;
```
</details>

---

### Задача 25: Динамика продаж товара
Для каждого товара покажите все его продажи с накопительным количеством проданных единиц.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.name,
    o.order_date::date,
    oi.quantity,
    SUM(oi.quantity) OVER (
        PARTITION BY p.product_id 
        ORDER BY o.order_date
    ) as cumulative_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
ORDER BY p.name, o.order_date;
```
</details>

---

### Задача 26: Анализ частоты покупок
Рассчитайте среднее время между заказами для каждого клиента (у кого больше одного заказа).

<details>
<summary>Решение</summary>

```sql
WITH order_gaps AS (
    SELECT 
        c.customer_id,
        c.name,
        o.order_date,
        LEAD(o.order_date) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
        ) as next_order_date,
        LEAD(o.order_date) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
        ) - o.order_date as days_gap
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
)
SELECT 
    customer_id,
    name,
    COUNT(*) as gaps_count,
    ROUND(AVG(EXTRACT(EPOCH FROM days_gap) / 86400), 1) as avg_days_between_orders
FROM order_gaps
WHERE days_gap IS NOT NULL
GROUP BY customer_id, name
ORDER BY avg_days_between_orders;
```
</details>

---

### Задача 27: Комплексный анализ товаров
Для каждого товара покажите:
- Ранг по цене в категории
- Отклонение цены от средней по категории
- Долю цены от максимальной в категории
- Является ли товар самым дорогим в категории

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price,
    RANK() OVER (PARTITION BY category ORDER BY price DESC) as price_rank,
    ROUND(price - AVG(price) OVER (PARTITION BY category), 2) as diff_from_avg,
    ROUND(price * 100.0 / MAX(price) OVER (PARTITION BY category), 2) as pct_of_max,
    CASE 
        WHEN price = MAX(price) OVER (PARTITION BY category) 
        THEN 'Да' 
        ELSE 'Нет' 
    END as is_most_expensive
FROM products
ORDER BY category, price_rank;
```
</details>

---

### Задача 28: Анализ первых покупок
Для каждого клиента покажите его первый заказ и сравните с его средней суммой заказа.

<details>
<summary>Решение</summary>

```sql
SELECT DISTINCT
    c.customer_id,
    c.name,
    FIRST_VALUE(o.order_date) OVER (
        PARTITION BY c.customer_id 
        ORDER BY o.order_date
    )::date as first_order_date,
    FIRST_VALUE(o.total_amount) OVER (
        PARTITION BY c.customer_id 
        ORDER BY o.order_date
    ) as first_order_amount,
    ROUND(AVG(o.total_amount) OVER (
        PARTITION BY c.customer_id
    ), 2) as avg_order_amount,
    COUNT(o.order_id) OVER (
        PARTITION BY c.customer_id
    ) as total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NOT NULL
ORDER BY c.name;
```
</details>

---

### Задача 29: Категории товаров с наибольшим разбросом цен
Для каждой категории рассчитайте разницу между максимальной и минимальной ценой. Покажите это для каждого товара.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    name,
    price,
    MIN(price) OVER (PARTITION BY category) as min_price,
    MAX(price) OVER (PARTITION BY category) as max_price,
    MAX(price) OVER (PARTITION BY category) - 
    MIN(price) OVER (PARTITION BY category) as price_range,
    ROUND(
        (price - MIN(price) OVER (PARTITION BY category)) * 100.0 /
        NULLIF(MAX(price) OVER (PARTITION BY category) - MIN(price) OVER (PARTITION BY category), 0),
        2
    ) as position_in_range_pct
FROM products
ORDER BY category, price;
```
</details>

---

### Задача 30: Анализ лояльности клиентов
Создайте сегментацию клиентов по количеству заказов и общей сумме:
- VIP: топ-20% по сумме
- Постоянный: топ-50% по сумме
- Обычный: остальные

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.city,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    NTILE(5) OVER (ORDER BY COALESCE(SUM(o.total_amount), 0) DESC) as revenue_quintile,
    CASE NTILE(5) OVER (ORDER BY COALESCE(SUM(o.total_amount), 0) DESC)
        WHEN 1 THEN 'VIP'
        WHEN 2 THEN 'Постоянный'
        WHEN 3 THEN 'Постоянный'
        ELSE 'Обычный'
    END as customer_segment
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC;
```
</details>

---
