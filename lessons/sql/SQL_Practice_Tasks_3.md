# Практические задачи по SQL 
## JOIN - объединение таблиц

---

### Задача 1: Список заказов с именами клиентов
Выведите список всех заказов с именами клиентов, которые их сделали. Покажите order_id, имя клиента, дату заказа и сумму заказа.

<details>
<summary>Решение</summary>

```sql
SELECT 
    o.order_id,
    c.name AS customer_name,
    o.order_date,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date;
```
</details>

---

### Задача 2: Заказы из Москвы
Найдите все заказы от клиентов из Москвы. Выведите имя клиента, email, сумму заказа.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.email,
    o.order_date,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE c.city = 'Москва'
ORDER BY o.total_amount DESC;
```
</details>

---

### Задача 3: Количество заказов каждого клиента
Подсчитайте, сколько заказов сделал каждый клиент. Покажите имя клиента, город и количество заказов. Отсортируйте по количеству заказов.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.city,
    COUNT(o.order_id) AS order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY order_count DESC;
```
</details>

---

### Задача 4: Топ-5 клиентов по сумме заказов
Найдите 5 клиентов, которые потратили больше всего денег. Выведите имя, город и общую сумму заказов.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.city,
    SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC
LIMIT 5;
```
</details>

---

### Задача 5: Все клиенты, включая тех, кто не делал заказов
Выведите список всех клиентов с количеством их заказов. Используйте LEFT JOIN, чтобы включить клиентов без заказов (у них будет 0 заказов).

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.email,
    c.city,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.city
ORDER BY order_count DESC;
```
</details>

---

### Задача 6: Клиенты без заказов
Найдите клиентов, которые ещё не сделали ни одного заказа. Выведите их имя и email.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.email,
    c.city
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```
</details>

---

### Задача 7: Детали заказов с названиями товаров
Выведите все позиции заказов (order_items) с названиями товаров. Покажите order_id, название товара, количество, цену.

<details>
<summary>Решение</summary>

```sql
SELECT 
    oi.order_id,
    p.name AS product_name,
    oi.quantity,
    oi.price,
    (oi.quantity * oi.price) AS item_total
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY oi.order_id;
```
</details>

---

### Задача 8: Полная информация о заказах
Выведите полную информацию о заказах: имя клиента, город, название товара, количество, цена. Объедините три таблицы: customers, orders, order_items, products.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name AS customer_name,
    c.city,
    o.order_date,
    p.name AS product_name,
    oi.quantity,
    oi.price,
    (oi.quantity * oi.price) AS item_total
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_date, o.order_id;
```
</details>

---

### Задача 9: Самые популярные товары
Найдите 10 самых популярных товаров (по количеству проданных единиц). Выведите название товара, категорию, количество заказов и общее количество проданных единиц.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.name,
    p.category,
    COUNT(oi.order_item_id) AS times_ordered,
    SUM(oi.quantity) AS total_sold
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_sold DESC
LIMIT 10;
```
</details>

---

### Задача 10: Выручка по категориям
Подсчитайте общую выручку по каждой категории товаров. Выведите категорию и сумму выручки, отсортируйте по выручке.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.category,
    SUM(oi.quantity * oi.price) AS revenue
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```
</details>

---

### Задача 11: Средний чек клиентов по городам
Найдите средний размер заказа для клиентов из каждого города. Выведите город и средний чек.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.city,
    COUNT(o.order_id) AS total_orders,
    ROUND(AVG(o.total_amount), 2) AS average_order
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY average_order DESC;
```
</details>

---

### Задача 12: Клиенты, купившие электронику
Найдите всех клиентов, которые покупали товары из категории "Электроника". Выведите уникальный список клиентов с их городами.

<details>
<summary>Решение</summary>

```sql
SELECT DISTINCT
    c.name,
    c.city,
    c.email
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE p.category = 'Электроника'
ORDER BY c.name;
```
</details>

---

### Задача 13: Заказы за последние 7 дней
Найдите все заказы, сделанные за последние 7 дней. Покажите имя клиента, дату заказа и сумму.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    o.order_date,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY o.order_date DESC;
```
</details>

---

### Задача 14: Клиенты с одним заказом
Найдите клиентов, которые сделали ровно один заказ. Выведите их имя, email и сумму единственного заказа.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.email,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, c.email
HAVING COUNT(o.order_id) = 1;
```
</details>

---

### Задача 15: Товары, которые никто не покупал
Найдите товары, которые ещё никто не заказал. Используйте LEFT JOIN.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.product_id,
    p.name,
    p.category,
    p.price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.order_item_id IS NULL
ORDER BY p.category, p.name;
```
</details>

---

## Продвинутые задачи

### Задача 16: Анализ покупок каждого клиента
Для каждого клиента выведите: имя, количество заказов, общую потраченную сумму, среднюю сумму заказа и дату последнего заказа. Используйте LEFT JOIN, чтобы включить всех клиентов.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.city,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    ROUND(COALESCE(AVG(o.total_amount), 0), 2) AS avg_order,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC;
```
</details>

---

### Задача 17: Категории товаров по городам
Какие категории товаров наиболее популярны в каждом городе? Выведите город, категорию и количество проданных товаров этой категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.city,
    p.category,
    SUM(oi.quantity) AS total_quantity
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY c.city, p.category
ORDER BY c.city, total_quantity DESC;
```
</details>

---

### Задача 18: Детальная статистика по товарам
Для каждого товара выведите: название, категорию, количество уникальных клиентов, купивших его, общее количество проданных единиц, общую выручку.

<details>
<summary>Решение</summary>

```sql
SELECT 
    p.name,
    p.category,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.order_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_revenue DESC;
```
</details>

---

### Задача 19: Клиенты, потратившие более 50000
Найдите клиентов, чья общая сумма заказов превышает 50000 рублей. Покажите их данные и сколько они потратили.

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.name,
    c.email,
    c.city,
    SUM(o.total_amount) AS total_spent,
    COUNT(o.order_id) AS order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.city
HAVING SUM(o.total_amount) > 50000
ORDER BY total_spent DESC;
```
</details>

---