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
# SQL: JOIN
## Объединение таблиц

---
# Зачем нужны JOIN?

**Реляционные базы данных** хранят данные в **разных таблицах**, чтобы избежать дублирования

**Пример:** интернет-магазин

- **products** - товары
- **customers** - клиенты  
- **orders** - заказы

**Пример:** получить информацию о заказе с именем клиента и названием товара

---
# Связи между таблицами

**FOREIGN KEY** (внешний ключ) - связывает таблицы

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2)
);
```

`customer_id` в orders -> `customer_id` в customers

---

**Таблица customers:**
```
customer_id | name          | email              | city
------------+---------------+--------------------+--------
1           | Иван Петров   | ivan@mail.ru       | Москва
2           | Анна Иванова  | anna@gmail.com     | СПб
```

**Таблица orders:**
```
order_id | customer_id | order_date           | total_amount
---------+-------------+----------------------+-------------
1        | 1           | 2026-01-15 10:30     | 80500.00
2        | 2           | 2026-01-16 14:20     | 45000.00
3        | 1           | 2026-01-20 09:15     | 12000.00
```

---
# INNER JOIN - основное объединение

**INNER JOIN** возвращает **только совпадающие записи** из обеих таблиц

**Синтаксис:**
```sql
SELECT columns
FROM table1
INNER JOIN table2 ON table1.column = table2.column;
```

---
# INNER JOIN - пример

**Получить заказы с именами клиентов:**

```sql
SELECT 
    orders.order_id,
    customers.name,
    customers.city,
    orders.order_date,
    orders.total_amount
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;
```

---
# Результат INNER JOIN

```
order_id | name         | city   | order_date          | total_amount
---------+--------------+--------+---------------------+-------------
1        | Иван Петров  | Москва | 2026-01-15 10:30    | 80500.00
2        | Анна Иванова | СПб    | 2026-01-16 14:20    | 45000.00
3        | Иван Петров  | Москва | 2026-01-20 09:15    | 12000.00
```

Если у клиента нет заказов, он **не попадёт** в результат

---
**Для краткости используют псевдонимы:**

```sql
SELECT 
    o.order_id,
    c.name,
    c.city,
    o.total_amount
FROM orders AS o
INNER JOIN customers AS c ON o.customer_id = c.customer_id;
```

`AS` можно опустить:
```sql
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
```

---
# JOIN с WHERE

**Объединение и фильтрация:**

```sql
SELECT 
    c.name,
    o.order_date,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE c.city = 'Москва' AND o.total_amount > 50000
ORDER BY o.order_date DESC;
```

Сначала объединяем, потом фильтруем

---
# JOIN с GROUP BY

**Сколько заказов у каждого клиента:**

```sql
SELECT 
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
```

---
# Три таблицы

**Структура:**
- orders (order_id, customer_id)
- order_items (order_id, product_id, quantity, price)
- products (product_id, name, category)

**Задача:** какие товары заказал каждый клиент?

---
# JOIN трёх таблиц

```sql
SELECT 
    c.name AS customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.price
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY c.name, o.order_id;
```

---
# LEFT JOIN (LEFT OUTER JOIN)

**LEFT JOIN** возвращает **все записи из левой таблицы**, даже если нет совпадений

```sql
SELECT 
    c.name,
    o.order_id,
    o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**Результат:** все клиенты, включая тех, у кого **нет заказов** (order_id будет NULL)

---
# LEFT JOIN - визуально

**customers (левая)** ← **orders (правая)**

```
name          | order_id | total_amount
--------------+----------+-------------
Иван Петров   | 1        | 80500.00
Иван Петров   | 3        | 12000.00
Анна Иванова  | 2        | 45000.00
Петр Сидоров  | NULL     | NULL         ← нет заказов!
Мария Смирнова| NULL     | NULL         ← нет заказов!
```

---
# LEFT JOIN - поиск клиентов без заказов

**Найти клиентов, которые ничего не заказали:**

```sql
SELECT 
    c.customer_id,
    c.name,
    c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**Ключевое условие:** `WHERE o.order_id IS NULL`

---
# RIGHT JOIN (RIGHT OUTER JOIN)

**RIGHT JOIN** - всё из **правой таблицы**

```sql
SELECT 
    c.name,
    o.order_id
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
```


---
# FULL OUTER JOIN

**FULL OUTER JOIN** возвращает **все записи из обеих таблиц**

```sql
SELECT 
    c.name,
    o.order_id
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```

**Результат:**
- Клиенты без заказов (order_id = NULL)
- Заказы без клиентов (name = NULL) 

---
# Типы JOIN - сравнение

| Тип | Описание |
|-----|----------|
| **INNER JOIN** | Только совпадения |
| **LEFT JOIN** | Все из левой + совпадения |
| **RIGHT JOIN** | Все из правой + совпадения |
| **FULL OUTER JOIN** | Все из обеих таблиц |


---
# Практический пример

**Топ-5 клиентов по сумме заказов:**

```sql
SELECT 
    c.name,
    c.city,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC
LIMIT 5;
```


---
# Самые популярные товары

```sql
SELECT 
    p.name,
    p.category,
    COUNT(oi.order_item_id) as times_ordered,
    SUM(oi.quantity) as total_quantity
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_quantity DESC
LIMIT 10;
```
---
# COALESCE - замена NULL

**COALESCE** возвращает первое NOT NULL значение:

```sql
SELECT 
    c.name,
    COALESCE(SUM(o.total_amount), 0) as total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

Без COALESCE клиенты без заказов имели бы total = NULL

---

# Клиенты и их последний заказ

```sql
SELECT 
    c.name,
    c.city,
    MAX(o.order_date) as last_order_date,
    COUNT(o.order_id) as total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY last_order_date DESC;
```