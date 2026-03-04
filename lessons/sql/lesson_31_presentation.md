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
# SQL:
## CTE, Индексы, Представления, Ограничения целостности

---
# Что мы уже знаем

- **SELECT, WHERE, ORDER BY, LIMIT**
- **GROUP BY, HAVING, агрегатные функции**
- **JOIN** - объединение таблиц
- **Подзапросы и CASE WHEN**
- **Оконные функции** (ROW_NUMBER, RANK, LAG, LEAD)

---
<!-- _class: centered -->
# CTE
## Common Table Expressions

---
# Проблема: сложные подзапросы

**Без CTE - трудно читать:**
```sql
SELECT name, order_count
FROM (
    SELECT 
        c.name,
        COUNT(o.order_id) as order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
) as customer_stats
WHERE order_count > 2
ORDER BY order_count DESC;
```

---

**WITH** определяет временную именованную таблицу:

```sql
WITH customer_stats AS (
    SELECT 
        c.name,
        COUNT(o.order_id) as order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT name, order_count
FROM customer_stats
WHERE order_count > 2
ORDER BY order_count DESC;
```

---

```sql
WITH имя_cte AS (
    -- запрос
),
второй_cte AS (
    -- можно ссылаться на первый
)
SELECT ...
FROM имя_cte
JOIN второй_cte ON ...;
```

- CTE существует только в рамках одного запроса
- Можно создавать несколько CTE через запятую
- Читается сверху вниз 

---

**Анализ продаж по клиентам и городам:**

```sql
WITH 
top_customers AS (
    SELECT customer_id, SUM(total_amount) as total_spent
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total_amount) > 50000
),
customer_info AS (
    SELECT c.customer_id, c.name, c.city, t.total_spent
    FROM customers c
    JOIN top_customers t ON c.customer_id = t.customer_id
)
SELECT city, COUNT(*) as vip_count, AVG(total_spent) as avg_spent
FROM customer_info
GROUP BY city
ORDER BY avg_spent DESC;
```

---

```sql
SELECT name FROM (
    SELECT name, 
           AVG(price) as avg_p
    FROM products
    GROUP BY name
) sub WHERE avg_p > 5000;
```

```sql
WITH stats AS (
    SELECT name,
           AVG(price) as avg_p
    FROM products
    GROUP BY name
)
SELECT name
FROM stats
WHERE avg_p > 5000;
```



---
 Для иерархических данных (категории, сотрудники, дерево):

```sql
WITH RECURSIVE org_chart AS (
    -- база рекурсии: сотрудники без руководителя
    SELECT employee_id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- рекурсивный шаг: сотрудники с руководителем
    SELECT e.employee_id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT * FROM org_chart ORDER BY level, name;
```

---
<!-- _class: centered -->
# Индексы
## CREATE INDEX

---
# Зачем нужны индексы?

**Без индекса** - PostgreSQL читает каждую строку (Sequential Scan):
```
Таблица: 1 000 000 строк
Запрос: WHERE customer_id = 555
-> Проверяет все 1 000 000 строк
```

**С индексом** - моментальный поиск (Index Scan):
```
-> Находит нужную строку напрямую
```


---

**Простой индекс:**
```sql
CREATE INDEX idx_customers_city
ON customers(city);
```

**Составной индекс** (по нескольким столбцам):
```sql
CREATE INDEX idx_orders_customer_date
ON orders(customer_id, order_date);
```

**Уникальный индекс:**
```sql
CREATE UNIQUE INDEX idx_customers_email
ON customers(email);
```

---
**Создавать:**
- Столбцы в условии WHERE часто
- Столбцы в JOIN
- Столбцы в ORDER BY на больших таблицах
- Внешние ключи

**Не создавать:**
- Маленькие таблицы (< 1000 строк)
- Столбцы с малым количеством уникальных значений 
- Таблицы с частыми INSERT/UPDATE - индексы замедляют запись

---
**Посмотреть индексы таблицы:**
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'customers';
```

**Удалить индекс:**
```sql
DROP INDEX idx_customers_city;
```

**Переименовать:**
```sql
ALTER INDEX idx_customers_city 
RENAME TO idx_cust_city;
```

---
<!-- _class: centered -->
# Представления (Views)

---

**View** - сохранённый SQL-запрос, к которому можно обращаться как к таблице

```sql
CREATE VIEW vw_order_details AS
SELECT 
    o.order_id,
    c.name AS customer_name,
    c.city,
    o.order_date,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

```sql
SELECT * FROM vw_order_details WHERE city = 'Астана';
```

---
### Зачем нужны Views?

**1. Упрощение сложных запросов**
Пишем JOIN один раз - обращаемся многократно

**2. Безопасность**
Скрываем чувствительные данные - пользователь видит только то, что нужно

**3. Консистентность**
Одно определение - везде одинаковый результат

**4. Абстракция**
Переименовываем столбцы, прячем детали реализации

---

**Изменить View:**
```sql
CREATE OR REPLACE VIEW vw_order_details AS
SELECT 
    o.order_id,
    c.name AS customer_name,
    c.city,
    o.order_date,
    o.total_amount,
    o.status  -- добавили новый столбец
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

**Удалить View:**
```sql
DROP VIEW vw_order_details;
```

---
# Materialized View

**Обычный View** - выполняет запрос при каждом обращении

**Materialized View** - сохраняет результат на диске:

```sql
CREATE MATERIALIZED VIEW mv_sales_summary AS
SELECT 
    category,
    COUNT(*) as total_orders,
    SUM(total_amount) as revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY category;
```



---
# View и Materialized View

| | View | Materialized View |
|-|------|-------------------|
| Хранит данные | Нет | Да |
| Скорость запроса | Как сам запрос | Быстро |
| Актуальность данных | Всегда | Нужен REFRESH |
| Можно индексировать | Нет | Да |
| Применение | Логика/безопасность | Тяжёлые агрегации |

---
<!-- _class: centered -->
# Ограничения целостности
## Constraints

---
# Зачем нужны ограничения?

**Ограничения** обеспечивают качество данных на уровне БД

```sql
-- Без ограничений - любой мусор попадает в БД
INSERT INTO orders (total_amount) VALUES (-999999);
INSERT INTO customers (email) VALUES (NULL);
INSERT INTO order_items (product_id) VALUES (99999); -- несуществующий товар
```

**Ограничения не дают этому произойти**

---
# PRIMARY KEY

Уникальный идентификатор строки:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
```

- Автоматически **NOT NULL + UNIQUE**
- Одна таблица - один PRIMARY KEY
- PostgreSQL создаёт индекс автоматически

---
# FOREIGN KEY

**Связь между таблицами и целостность:**

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Попытка вставить несуществующего клиента -> ошибка:**
```sql
INSERT INTO orders (customer_id) VALUES (9999);
-- ERROR: insert or update on table "orders" violates foreign key constraint
```

---
# ON DELETE / ON UPDATE


```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id)
        ON DELETE CASCADE    -- удалить заказы при удалении клиента
        ON UPDATE CASCADE    -- обновить при изменении customer_id
);
```

| Опция | Поведение |
|-------|-----------|
| CASCADE | Удалить/обновить зависимые строки |
| SET NULL | Установить NULL в зависимых строках |
| RESTRICT | Запретить удаление, если есть зависимости |
| NO ACTION | То же что RESTRICT (по умолчанию) |

---
# CHECK - проверка условий

**Ограничение на значения столбца:**

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) CHECK (price >= 0),
    stock INTEGER CHECK (stock >= 0),
    discount DECIMAL(5, 2) CHECK (discount BETWEEN 0 AND 100)
);
```

```sql
INSERT INTO products (name, price) VALUES ('Товар', -500);
-- ERROR: new row for relation "products" violates check constraint
```

---

**Уникальность значений в столбце:**

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) UNIQUE
);
```

**Составная уникальность:**
```sql
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    UNIQUE (student_id, course_id)  -- пара должна быть уникальной
);
```

---

```sql
-- Добавить CHECK
ALTER TABLE products
ADD CONSTRAINT chk_price_positive CHECK (price >= 0);

-- Добавить UNIQUE
ALTER TABLE customers
ADD CONSTRAINT uq_customer_email UNIQUE (email);

-- Добавить FOREIGN KEY
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Удалить ограничение
ALTER TABLE products
DROP CONSTRAINT chk_price_positive;
```

---
# Шпаргалка

```sql
-- CTE
WITH cte_name AS (SELECT ...) SELECT ... FROM cte_name;

-- Индекс
CREATE INDEX idx_name ON table(column);

-- View
CREATE VIEW vw_name AS SELECT ...;

-- Ограничения
price DECIMAL CHECK (price >= 0)
FOREIGN KEY (col) REFERENCES other_table(col) ON DELETE CASCADE
ADD CONSTRAINT name CHECK (...) / UNIQUE (...)
```
