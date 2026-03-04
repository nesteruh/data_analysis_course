# Практические задачи
## CTE, Индексы, Views, Ограничения целостности

---

##  CTE (Common Table Expressions)

### Задача 1: Первый CTE
Используя CTE, найдите всех клиентов, у которых сумма всех заказов превышает 100 000. Выведите имя клиента, город и общую сумму.

<details>
<summary>Решение</summary>

```sql
WITH customer_totals AS (
    SELECT 
        customer_id,
        SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.name,
    c.city,
    ct.total_spent
FROM customers c
JOIN customer_totals ct ON c.customer_id = ct.customer_id
WHERE ct.total_spent > 100000
ORDER BY ct.total_spent DESC;
```
</details>

---

### Задача 2: Несколько CTE
Найдите категории товаров, в которых:
- средняя цена выше средней цены по всем товарам
- количество товаров больше 3

Выведите категорию, среднюю цену и количество товаров.

<details>
<summary>Решение</summary>

```sql
WITH overall_avg AS (
    SELECT AVG(price) AS avg_all
    FROM products
),
category_stats AS (
    SELECT 
        category,
        ROUND(AVG(price), 2) AS avg_price,
        COUNT(*) AS product_count
    FROM products
    GROUP BY category
)
SELECT 
    cs.category,
    cs.avg_price,
    cs.product_count
FROM category_stats cs, overall_avg oa
WHERE cs.avg_price > oa.avg_all
  AND cs.product_count > 3
ORDER BY cs.avg_price DESC;
```
</details>

---

### Задача 3: CTE вместо подзапроса
Перепишите следующий запрос с подзапросом через CTE:

```sql
SELECT c.name, sub.order_count, sub.total_spent
FROM customers c
JOIN (
    SELECT customer_id, 
           COUNT(*) AS order_count,
           SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
) sub ON c.customer_id = sub.customer_id
WHERE sub.order_count >= 3
ORDER BY sub.total_spent DESC;
```

<details>
<summary>Решение</summary>

```sql
WITH order_summary AS (
    SELECT 
        customer_id,
        COUNT(*) AS order_count,
        SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.name,
    os.order_count,
    os.total_spent
FROM customers c
JOIN order_summary os ON c.customer_id = os.customer_id
WHERE os.order_count >= 3
ORDER BY os.total_spent DESC;
```
</details>

---

### Задача 4: CTE с оконными функциями
Используя CTE и оконные функции, найдите топ-2 самых дорогих товара в каждой категории. Выведите категорию, название товара, цену и ранг.

<details>
<summary>Решение</summary>

```sql
WITH ranked_products AS (
    SELECT 
        category,
        name,
        price,
        RANK() OVER (PARTITION BY category ORDER BY price DESC) AS price_rank
    FROM products
)
SELECT category, name, price, price_rank
FROM ranked_products
WHERE price_rank <= 2
ORDER BY category, price_rank;
```
</details>

---

## Индексы

### Задача 5: Создание индексов
Создайте подходящие индексы для следующих частых запросов:

```sql
-- Запрос 1: поиск заказов по клиенту
SELECT * FROM orders WHERE customer_id = 5;

-- Запрос 2: поиск товаров по категории и цене
SELECT * FROM products WHERE category = 'Электроника' AND price < 10000;

-- Запрос 3: поиск клиентов по email
SELECT * FROM customers WHERE email = 'ivan@mail.ru';
```

<details>
<summary>Решение</summary>

```sql
-- Индекс 1: по customer_id в orders
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Индекс 2: составной по category и price
CREATE INDEX idx_products_category_price ON products(category, price);

-- Индекс 3: уникальный по email (email должен быть уникальным)
CREATE UNIQUE INDEX idx_customers_email ON customers(email);
```
</details>

---

### Задача 6: Просмотр и удаление индексов
1. Посмотрите все индексы таблицы `orders`
2. Удалите индекс `idx_orders_customer_id`
3. Убедитесь, что он удалён

<details>
<summary>Решение</summary>

```sql
-- 1. Просмотр индексов
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'orders';

-- 2. Удаление
DROP INDEX idx_orders_customer_id;

-- 3. Проверка - индекс больше не отобразится
SELECT indexname
FROM pg_indexes
WHERE tablename = 'orders';
```
</details>

---

## Представления (Views)

### Задача 7: Создание View
Создайте представление `vw_customer_orders`, которое для каждого клиента показывает:
- имя и город клиента
- количество заказов
- общую сумму заказов
- дату последнего заказа

<details>
<summary>Решение</summary>

```sql
CREATE VIEW vw_customer_orders AS
SELECT 
    c.name AS customer_name,
    c.city,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city;
```
</details>

---

### Задача 8: Использование View
Используя созданное представление `vw_customer_orders`:
1. Найдите клиентов из Москвы с более чем 2 заказами
2. Выведите топ-3 клиентов по сумме заказов

<details>
<summary>Решение</summary>

```sql
-- 1. Клиенты из Москвы с более чем 2 заказами
SELECT customer_name, order_count, total_spent
FROM vw_customer_orders
WHERE city = 'Москва' AND order_count > 2
ORDER BY total_spent DESC;

-- 2. Топ-3 по сумме
SELECT customer_name, city, total_spent
FROM vw_customer_orders
ORDER BY total_spent DESC
LIMIT 3;
```
</details>

---

### Задача 9: Обновление и удаление View
1. Обновите представление `vw_customer_orders` - добавьте столбец `avg_order_amount` (средняя сумма одного заказа)
2. Удалите представление

<details>
<summary>Решение</summary>

```sql
-- 1. Обновление через CREATE OR REPLACE
CREATE OR REPLACE VIEW vw_customer_orders AS
SELECT 
    c.name AS customer_name,
    c.city,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    ROUND(COALESCE(AVG(o.total_amount), 0), 2) AS avg_order_amount,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city;

-- 2. Удаление
DROP VIEW vw_customer_orders;
```
</details>

---

## Ограничения целостности

### Задача 10: Добавление ограничений
Добавьте к таблице `products` следующие ограничения:
1. Цена не может быть отрицательной
2. Остаток на складе не может быть меньше 0
3. Скидка (если есть столбец `discount`) - от 0 до 100

<details>
<summary>Решение</summary>

```sql
ALTER TABLE products
ADD CONSTRAINT chk_price_positive CHECK (price >= 0);

ALTER TABLE products
ADD CONSTRAINT chk_stock_non_negative CHECK (stock >= 0);

ALTER TABLE products
ADD CONSTRAINT chk_discount_range CHECK (discount BETWEEN 0 AND 100);
```
</details>

---

### Задача 11: FOREIGN KEY с правилами удаления
Создайте таблицу `reviews` (отзывы на товары), где:
- `review_id` - первичный ключ
- `product_id` - ссылка на `products`, при удалении товара отзывы тоже удаляются
- `customer_id` - ссылка на `customers`, при удалении клиента `customer_id` становится NULL
- `rating` - от 1 до 5
- `comment` - текст отзыва

<details>
<summary>Решение</summary>

```sql
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id) ON DELETE CASCADE,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE SET NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
</details>

---

### Задача 12: Проверка ограничений
Попробуйте нарушить ограничения из задачи 10 и задачи 11, убедитесь что PostgreSQL возвращает ошибку. Затем удалите одно из ограничений.

<details>
<summary>Решение</summary>

```sql
-- Нарушение CHECK: отрицательная цена → ошибка
INSERT INTO products (name, price, stock)
VALUES ('Тест', -100, 10);
-- ERROR: new row for relation "products" violates check constraint "chk_price_positive"

-- Нарушение FOREIGN KEY: несуществующий product_id → ошибка
INSERT INTO reviews (product_id, rating)
VALUES (99999, 5);
-- ERROR: insert or update on table "reviews" violates foreign key constraint

-- Нарушение CHECK в reviews: рейтинг > 5 → ошибка
INSERT INTO reviews (product_id, rating)
VALUES (1, 10);
-- ERROR: new row for relation "reviews" violates check constraint

-- Удаление ограничения
ALTER TABLE products
DROP CONSTRAINT chk_discount_range;
```
</details>

---

## Комплексные задачи

### Задача 13: Всё вместе
Используя CTE, создайте View `vw_category_analysis`, которое показывает по каждой категории:
- количество товаров
- среднюю цену
- флаг `is_premium` (TRUE если средняя цена выше 10 000)
- ранг категории по средней цене (1 = самая дорогая)

<details>
<summary>Решение</summary>

```sql
CREATE VIEW vw_category_analysis AS
WITH category_stats AS (
    SELECT 
        category,
        COUNT(*) AS product_count,
        ROUND(AVG(price), 2) AS avg_price
    FROM products
    GROUP BY category
)
SELECT 
    category,
    product_count,
    avg_price,
    avg_price > 10000 AS is_premium,
    RANK() OVER (ORDER BY avg_price DESC) AS price_rank
FROM category_stats;
```
</details>

---

### Задача 14: Анализ продаж через CTE
Используя несколько CTE, найдите клиентов, которые:
1. Сделали более 2 заказов
2. Хотя бы один из заказов превышает 50 000
3. Выведите: имя, город, количество заказов, максимальный заказ, общую сумму

<details>
<summary>Решение</summary>

```sql
WITH order_stats AS (
    SELECT 
        customer_id,
        COUNT(*) AS order_count,
        MAX(total_amount) AS max_order,
        SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
),
qualified_customers AS (
    SELECT customer_id, order_count, max_order, total_spent
    FROM order_stats
    WHERE order_count > 2
      AND max_order > 50000
)
SELECT 
    c.name,
    c.city,
    qc.order_count,
    qc.max_order,
    qc.total_spent
FROM customers c
JOIN qualified_customers qc ON c.customer_id = qc.customer_id
ORDER BY qc.total_spent DESC;
```
</details>
