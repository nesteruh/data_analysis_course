# Практические задачи по SQL 
## Подзапросы и CASE WHEN

---

### Задача 1: Товары дороже средней цены
Найдите все товары, цена которых выше средней цены по всем товарам. Выведите название, категорию и цену.

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;
```
</details>

---

### Задача 2: Товары дороже средней цены в своей категории
Найдите товары, которые стоят дороже средней цены **в своей категории**. Используйте подзапрос с корреляцией.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p1.name,
    p1.category,
    p1.price,
    ROUND((SELECT AVG(price) 
           FROM products p2 
           WHERE p2.category = p1.category), 2) as category_avg_price
FROM products p1
WHERE p1.price > (
    SELECT AVG(price) 
    FROM products p2 
    WHERE p2.category = p1.category
)
ORDER BY p1.category, p1.price DESC;
```
</details>

---

### Задача 3: Клиенты с заказами (используя IN)
Найдите всех клиентов, которые делали хотя бы один заказ. Используйте оператор IN.

<details>
<summary>Решение</summary>

```sql
SELECT 
    customer_id,
    name,
    email,
    city
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id 
    FROM orders
)
ORDER BY name;
```
</details>

---

### Задача 4: Клиенты без заказов (используя NOT IN)
Найдите клиентов, которые не сделали ни одного заказа. Используйте NOT IN.

<details>
<summary>Решение</summary>

```sql
SELECT 
    customer_id,
    name,
    email,
    city
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id 
    FROM orders
    WHERE customer_id IS NOT NULL
)
ORDER BY name;
```

**Важно:** добавили `WHERE customer_id IS NOT NULL` в подзапросе, чтобы избежать проблем с NULL.

</details>

---

### Задача 5: Клиенты с заказами (используя EXISTS)
Напишите тот же запрос, что и в задаче 3, но используйте EXISTS вместо IN.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.city
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
)
ORDER BY c.name;
```
</details>

---

### Задача 6: Количество заказов для каждого клиента
Выведите всех клиентов с количеством их заказов. Используйте подзапрос в SELECT.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.city,
    (SELECT COUNT(*) 
     FROM orders o 
     WHERE o.customer_id = c.customer_id) as order_count
FROM customers c
ORDER BY order_count DESC, c.name;
```
</details>

---

### Задача 7: Категории товаров - ценовая сегментация
Используйте CASE WHEN для разделения товаров на ценовые сегменты:
- "Бюджет" (< 5000)
- "Средний" (5000-20000)
- "Премиум" (> 20000)

Выведите название, цену и сегмент.

<details>
<summary>Решение</summary>

```sql
SELECT 
    name,
    category,
    price,
    CASE 
        WHEN price < 5000 THEN 'Бюджет'
        WHEN price BETWEEN 5000 AND 20000 THEN 'Средний'
        ELSE 'Премиум'
    END as price_segment
FROM products
ORDER BY price;
```
</details>

---

### Задача 8: Количество товаров по сегментам
Подсчитайте количество товаров в каждом ценовом сегменте из предыдущей задачи.

<details>
<summary>Решение</summary>

```sql
SELECT 
    CASE 
        WHEN price < 5000 THEN 'Бюджет'
        WHEN price BETWEEN 5000 AND 20000 THEN 'Средний'
        ELSE 'Премиум'
    END as price_segment,
    COUNT(*) as product_count,
    ROUND(AVG(price), 2) as avg_price
FROM products
GROUP BY price_segment
ORDER BY 
    CASE price_segment
        WHEN 'Бюджет' THEN 1
        WHEN 'Средний' THEN 2
        ELSE 3
    END;
```
</details>

---

### Задача 9: Статус заказа на русском
Создайте запрос, который показывает заказы с переведённым статусом:
- pending → Ожидает
- shipped → Отправлен
- completed → Завершён

<details>
<summary>Решение</summary>

```sql
SELECT 
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    CASE status
        WHEN 'pending' THEN 'Ожидает'
        WHEN 'shipped' THEN 'Отправлен'
        WHEN 'completed' THEN 'Завершён'
        ELSE 'Неизвестный'
    END as status_ru
FROM orders
ORDER BY order_date DESC;
```
</details>

---

### Задача 10: Категории с товарами дороже порогового значения
Найдите категории, в которых есть хотя бы один товар дороже 30000. Используйте подзапрос с EXISTS.

<details>
<summary>Решение</summary>

```sql
SELECT DISTINCT category
FROM products p1
WHERE EXISTS (
    SELECT 1 
    FROM products p2 
    WHERE p2.category = p1.category 
      AND p2.price > 30000
)
ORDER BY category;
```
</details>

---

### Задача 11: Товары со статусом продаж
Для каждого товара покажите, был ли он продан или нет. Используйте CASE WHEN с подзапросом.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.product_id,
    p.name,
    p.category,
    p.price,
    CASE 
        WHEN EXISTS (
            SELECT 1 
            FROM order_items oi 
            WHERE oi.product_id = p.product_id
        ) THEN 'Продан'
        ELSE 'Не продан'
    END as sales_status
FROM products p
ORDER BY sales_status, p.name;
```
</details>

---

### Задача 12: Популярность товаров с подсчётом продаж
Покажите товары с количеством проданных единиц и категорией популярности:
- "Популярный" (>= 3 продано)
- "Средний" (1-2 продано)
- "Не продан" (0 продано)

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.name,
    p.category,
    p.price,
    COALESCE(SUM(oi.quantity), 0) as total_sold,
    CASE 
        WHEN COALESCE(SUM(oi.quantity), 0) >= 3 THEN 'Популярный'
        WHEN COALESCE(SUM(oi.quantity), 0) >= 1 THEN 'Средний'
        ELSE 'Не продан'
    END as popularity
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category, p.price
ORDER BY total_sold DESC, p.name;
```
</details>

---

### Задача 13: Распределение товаров по категориям и сегментам
Для каждой категории покажите, сколько в ней товаров из каждого ценового сегмента.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    COUNT(*) as total_products,
    SUM(CASE WHEN price < 5000 THEN 1 ELSE 0 END) as budget,
    SUM(CASE WHEN price BETWEEN 5000 AND 20000 THEN 1 ELSE 0 END) as medium,
    SUM(CASE WHEN price > 20000 THEN 1 ELSE 0 END) as premium
FROM products
GROUP BY category
ORDER BY total_products DESC;
```
</details>

---

### Задача 14: Ранжирование клиентов
Создайте список клиентов с их общей суммой покупок и категорией клиента:
- "VIP" (> 50000)
- "Постоянный" (20000-50000)
- "Обычный" (< 20000 или нет заказов)

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.city,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    CASE 
        WHEN SUM(o.total_amount) > 50000 THEN 'VIP'
        WHEN SUM(o.total_amount) >= 20000 THEN 'Постоянный'
        ELSE 'Обычный'
    END as customer_tier
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC;
```
</details>

---

### Задача 15: Расчёт скидки для заказов
Рассчитайте скидку для каждого заказа по правилам:
- 15% для заказов > 50000
- 10% для заказов > 30000
- 5% для заказов > 10000
- 0% для остальных

Выведите order_id, сумму, размер скидки и итоговую сумму.

<details>
<summary>Решение</summary>

```sql
SELECT 
    order_id,
    total_amount,
    CASE 
        WHEN total_amount > 50000 THEN total_amount * 0.15
        WHEN total_amount > 30000 THEN total_amount * 0.10
        WHEN total_amount > 10000 THEN total_amount * 0.05
        ELSE 0
    END as discount,
    total_amount - CASE 
        WHEN total_amount > 50000 THEN total_amount * 0.15
        WHEN total_amount > 30000 THEN total_amount * 0.10
        WHEN total_amount > 10000 THEN total_amount * 0.05
        ELSE 0
    END as final_amount
FROM orders
ORDER BY total_amount DESC;
```
</details>

---

### Задача 16: Заказы выше среднего для клиента
Найдите заказы, сумма которых выше средней суммы заказов этого же клиента.

<details>
<summary>Решение</summary>

```sql
SELECT 
    o1.order_id,
    o1.customer_id,
    o1.total_amount,
    ROUND((SELECT AVG(total_amount) 
           FROM orders o2 
           WHERE o2.customer_id = o1.customer_id), 2) as customer_avg
FROM orders o1
WHERE o1.total_amount > (
    SELECT AVG(total_amount) 
    FROM orders o2 
    WHERE o2.customer_id = o1.customer_id
)
ORDER BY o1.customer_id, o1.total_amount DESC;
```
</details>

---

### Задача 17: Товары с низким запасом
Найдите товары, у которых запас ниже среднего запаса в их категории. Покажите также средний запас категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p1.name,
    p1.category,
    p1.stock,
    ROUND((SELECT AVG(stock) 
           FROM products p2 
           WHERE p2.category = p1.category), 2) as category_avg_stock,
    CASE 
        WHEN p1.stock < 10 THEN 'Критический'
        WHEN p1.stock < 20 THEN 'Низкий'
        ELSE 'Нормальный'
    END as stock_status
FROM products p1
WHERE p1.stock < (
    SELECT AVG(stock) 
    FROM products p2 
    WHERE p2.category = p1.category
)
ORDER BY p1.category, p1.stock;
```
</details>

---

### Задача 18: Анализ категорий товаров
Для каждой категории покажите:
- Общее количество товаров
- Среднюю цену
- Количество товаров с низким запасом (< 10)
- Количество проданных товаров

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.category,
    COUNT(*) as total_products,
    ROUND(AVG(p.price), 2) as avg_price,
    SUM(CASE WHEN p.stock < 10 THEN 1 ELSE 0 END) as low_stock_count,
    SUM(CASE 
        WHEN p.product_id IN (SELECT product_id FROM order_items) 
        THEN 1 
        ELSE 0 
    END) as sold_products
FROM products p
GROUP BY p.category
ORDER BY total_products DESC;
```
</details>

---

### Задача 19: Города с самыми активными клиентами
Найдите города, где общая сумма заказов превышает 100000. Покажите город, количество клиентов и общую сумму.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.city,
    COUNT(DISTINCT c.customer_id) as customer_count,
    SUM(o.total_amount) as total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING SUM(o.total_amount) > 100000
ORDER BY total_revenue DESC;
```
</details>

---

### Задача 20: Комплексный анализ заказов
Для каждого заказа покажите:
- ID заказа
- Имя клиента
- Город клиента
- Сумму заказа
- Категорию заказа: "Крупный" (> 30000), "Средний" (10000-30000), "Мелкий" (< 10000)
- Превышает ли сумма среднюю по всем заказам ("Да"/"Нет")

<details>
<summary>Решение</summary>

```sql
SELECT 
    o.order_id,
    c.name as customer_name,
    c.city,
    o.total_amount,
    CASE 
        WHEN o.total_amount > 30000 THEN 'Крупный'
        WHEN o.total_amount >= 10000 THEN 'Средний'
        ELSE 'Мелкий'
    END as order_category,
    CASE 
        WHEN o.total_amount > (SELECT AVG(total_amount) FROM orders) 
        THEN 'Да'
        ELSE 'Нет'
    END as above_average
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.total_amount DESC;
```
</details>

---

## Дополнительные задачи повышенной сложности

### Задача 21: Товары, которые никогда не заказывали вместе с определённым товаром
Найдите товары, которые никогда не были в одном заказе с товаром "Ноутбук ASUS".

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.product_id,
    p.name,
    p.category
FROM products p
WHERE p.product_id NOT IN (
    SELECT DISTINCT oi1.product_id
    FROM order_items oi1
    WHERE oi1.order_id IN (
        SELECT oi2.order_id
        FROM order_items oi2
        INNER JOIN products p2 ON oi2.product_id = p2.product_id
        WHERE p2.name = 'Ноутбук ASUS'
    )
)
AND p.name != 'Ноутбук ASUS'
ORDER BY p.name;
```
</details>

---

### Задача 22: Клиенты с заказами в каждом статусе
Найдите клиентов, у которых есть заказы во всех трёх статусах (pending, shipped, completed).

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.customer_id,
    c.name,
    c.email
FROM customers c
WHERE 
    EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'pending')
    AND EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'shipped')
    AND EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'completed')
ORDER BY c.name;
```
</details>
