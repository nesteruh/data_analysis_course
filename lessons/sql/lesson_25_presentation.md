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
# SQL: Подзапросы и CASE WHEN
## Условная логика и вложенные запросы

---
# Что такое подзапрос?

**Подзапрос** - это запрос внутри другого запроса

```sql
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

**Внешний запрос:** выбирает товары
**Подзапрос:** `(SELECT AVG(price) FROM products)` - вычисляет среднюю цену

---
# Подзапрос в WHERE

**Задача:** найти товары дороже средней цены

```sql
SELECT name, category, price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;
```

**Порядок выполнения:**
1. Подзапрос вычисляет среднюю цену
2. Внешний запрос сравнивает с этим значением

---
# Подзапрос с IN

**Оператор IN** проверяет вхождение в список

**Найти клиентов, которые делали заказы:**

```sql
SELECT name, email, city
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id 
    FROM orders
);
```

**Подзапрос возвращает:** список ID клиентов с заказами

---
# Подзапрос с NOT IN

**Найти клиентов БЕЗ заказов:**

```sql
SELECT name, email, city
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id 
    FROM orders
);
```

**Альтернатива:** LEFT JOIN с WHERE ... IS NULL
Какой способ лучше зависит от данных и производительности

---
# Подзапрос в SELECT

**Подзапрос может вычислять значение для каждой строки**

**Показать количество заказов для каждого клиента:**

```sql
SELECT 
    name,
    city,
    (SELECT COUNT(*) 
     FROM orders o 
     WHERE o.customer_id = c.customer_id) as order_count
FROM customers c
ORDER BY order_count DESC;
```
---
# Подзапрос в FROM

**Получить категории со средней ценой выше общей средней:**

```sql
SELECT category, avg_price
FROM (
    SELECT 
        category,
        AVG(price) as avg_price
    FROM products
    GROUP BY category
) as category_stats
WHERE avg_price > (SELECT AVG(price) FROM products)
ORDER BY avg_price DESC;
```


---
# EXISTS и NOT EXISTS

**EXISTS** проверяет, есть ли хотя бы одна строка в подзапросе

**Клиенты, у которых есть заказы:**

```sql
SELECT name, email
FROM customers c
WHERE EXISTS (
    SELECT * 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
);
```

**Преимущество:** останавливается при первом совпадении

---
# NOT EXISTS

**Клиенты без заказов:**

```sql
SELECT name, email, city
FROM customers c
WHERE NOT EXISTS (
    SELECT *
    FROM orders o 
    WHERE o.customer_id = c.customer_id
);
```
---
# CASE WHEN - условная логика

**CASE WHEN** работает как if-else в программировании

**Простой пример:**

```sql
SELECT 
    name,
    price,
    CASE 
        WHEN price < 1000 THEN 'Дёшево'
        WHEN price < 10000 THEN 'Средняя цена'
        ELSE 'Дорого'
    END as price_category
FROM products;
```

---
# CASE WHEN - синтаксис

```sql
CASE 
    WHEN условие1 THEN результат1
    WHEN условие2 THEN результат2
    WHEN условие3 THEN результат3
    ELSE результат_по_умолчанию
END
```

- Условия проверяются **по порядку**
- Первое совпадение возвращает результат
- ELSE необязателен (без него вернётся NULL)

---
# CASE WHEN - категории товаров

**Разделить товары на ценовые сегменты:**

```sql
SELECT 
    category,
    COUNT(*) as total,
    SUM(CASE WHEN price < 5000 THEN 1 ELSE 0 END) as budget,
    SUM(CASE WHEN price BETWEEN 5000 AND 20000 THEN 1 ELSE 0 END) as medium,
    SUM(CASE WHEN price > 20000 THEN 1 ELSE 0 END) as premium
FROM products
GROUP BY category;
```

**Результат:** сколько в каждой категории бюджетных/средних/премиум товаров

---
# CASE WHEN в GROUP BY

**Группировать по вычисленному полю:**

```sql
SELECT 
    CASE 
        WHEN price < 5000 THEN 'Бюджет'
        WHEN price < 20000 THEN 'Средний'
        ELSE 'Премиум'
    END as segment,
    COUNT(*) as product_count,
    ROUND(AVG(price), 2) as avg_price
FROM products
GROUP BY segment
ORDER BY avg_price;
```

---
# CASE WHEN для статуса заказов

**Перевести статусы на русский:**

```sql
SELECT 
    order_id,
    total_amount,
    status,
    CASE status
        WHEN 'pending' THEN 'Ожидает'
        WHEN 'shipped' THEN 'Отправлен'
        WHEN 'completed' THEN 'Завершён'
        ELSE 'Неизвестно'
    END as status_ru
FROM orders;
```

**Упрощённый синтаксис:** `CASE status WHEN ...`

---

## Показать товары с меткой популярности:

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
ORDER BY total_sold DESC;
```

---
### Разделить клиентов по сумме покупок:

```sql
SELECT 
    name,
    city,
    COALESCE(
        (SELECT SUM(total_amount) 
         FROM orders o 
         WHERE o.customer_id = c.customer_id), 
        0
    ) as total_spent,
    CASE 
        WHEN (SELECT SUM(total_amount) 
              FROM orders o 
              WHERE o.customer_id = c.customer_id) > 50000 
        THEN 'VIP'
        WHEN (SELECT SUM(total_amount) 
              FROM orders o 
              WHERE o.customer_id = c.customer_id) > 20000 
        THEN 'Постоянный'
        ELSE 'Обычный'
    END as customer_tier
FROM customers c;
```

---
### Рассчитать скидку в зависимости от суммы заказа:

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
    CASE 
        WHEN total_amount > 50000 THEN '15%'
        WHEN total_amount > 30000 THEN '10%'
        WHEN total_amount > 10000 THEN '5%'
        ELSE '0%'
    END as discount_rate
FROM orders
ORDER BY total_amount DESC;
```
---
# Когда использовать подзапросы?

**Подзапросы:**
- Нужно сравнить с агрегированным значением
- Проверить вхождение в динамический список
- Вычислить значение для каждой строки

**JOIN:**
- Нужны данные из нескольких таблиц
- Часто быстрее для больших данных

---
# Производительность

**Оптимизация запросов:**
- EXISTS обычно быстрее IN для больших таблиц
- Избегайте подзапросов в SELECT для больших датасетов
- JOIN часто эффективнее подзапросов в FROM

**Совет:** сначала пишите понятный код, оптимизируйте при необходимости

---
# Типичные ошибки

 **Подзапрос возвращает больше одной строки:**
```sql
WHERE price > (SELECT price FROM products WHERE category = 'Электроника')
```

 **Используйте агрегацию:**
```sql
WHERE price > (SELECT AVG(price) FROM products WHERE category = 'Электроника')
```

---
# Краткая шпаргалка

| Конструкция | Использование |
|-------------|---------------|
| `WHERE col IN (subquery)` | Проверка вхождения в список |
| `WHERE EXISTS (subquery)` | Проверка существования |
| `SELECT (subquery) FROM` | Вычисление значения |
| `FROM (subquery) alias` | Временная таблица |
| `CASE WHEN ... THEN ... END` | Условная логика |

