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
# SQL: GROUP BY

---
# Что мы уже знаем:
 **Агрегатные функции:**
- COUNT(*), SUM(), AVG(), MIN(), MAX()

**Базовые запросы:**
```sql
SELECT COUNT(*) FROM products;
SELECT AVG(price) FROM products;
```

**Проблема:** как получить статистику **по каждой категории**

---
# DISTINCT - уникальные значения

**DISTINCT** удаляет дубликаты из результата:

```sql
SELECT DISTINCT category FROM products;
```
**Результат:** список уникальных категорий
```
category
-------------
Электроника
Мебель
Аксессуары
Книги
```

---
# COUNT(DISTINCT column)

**Подсчёт уникальных значений:**

```sql
SELECT COUNT(DISTINCT category) as unique_categories
FROM products;
```

**Результат:**
```
unique_categories
-----------------
                5
```

---
# Проблема: анализ по группам

**Вопрос:** Какая средняя цена в **каждой** категории?

**Неправильно:** 
```sql
SELECT category, AVG(price)
FROM products;
```

Нельзя смешивать обычные столбцы с агрегатными функциями

**Решение:** GROUP BY 

---
# GROUP BY - группировка данных

**GROUP BY** разбивает данные на группы и применяет агрегатные функции к **каждой группе**

**Синтаксис:**
```sql
SELECT column, AGG_FUNCTION(column)
FROM table
GROUP BY column;
```

---

**Количество товаров в каждой категории:**
```sql
SELECT 
    category,
    COUNT(*) as product_count
FROM products
GROUP BY category;
```

**Результат:**
```
category     | product_count
-------------+--------------
Электроника  |           10
Мебель       |            6
Аксессуары   |            5
```

---

**Правило:** Все столбцы в SELECT (кроме агрегатных) должны быть в GROUP BY

 **Правильно:**
```sql
SELECT category, COUNT(*)
FROM products
GROUP BY category;
```

 **Неправильно:**
```sql
SELECT category, name, COUNT(*)
FROM products
GROUP BY category;
```

---
**ROUND(число, знаков)** - округление результата:
```sql
SELECT 
    category,
    ROUND(AVG(price), 2) as avg_price  
FROM products
GROUP BY category;
```

**AS** - псевдоним для читаемости:
```sql
SELECT 
    COUNT(*) as total_products,        -- вместо count
    SUM(price * stock) as total_value  -- понятное название
FROM products;
```

---

```sql
SELECT  
    category,
    COUNT(*) as total_items,
    ROUND(AVG(price), 2) as avg_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;
```

**Результат:**
```
category     | total_items | avg_price
-------------+-------------+-----------
Электроника  |          10 |  23670.00
Мебель       |           6 |   9166.67
Аксессуары   |           5 |   1860.00
```

---
# Несколько агрегатных функций

```sql
SELECT 
    category,
    COUNT(*) as total_items,
    MIN(price) as cheapest,
    MAX(price) as most_expensive,
    ROUND(AVG(price), 2) as avg_price,
    SUM(stock) as total_stock
FROM products
GROUP BY category
ORDER BY total_stock DESC;
```

Получаем полную аналитику по каждой категории

---

**Средняя цена товаров в наличии (stock > 0):**
```sql
SELECT 
    category,
    ROUND(AVG(price), 2) as avg_price
FROM products
WHERE stock > 0
GROUP BY category;
```

**Порядок выполнения:**
1. WHERE - фильтрация строк
2. GROUP BY - группировка
3. Агрегатные функции

---
**HAVING** фильтрует после группировки (работает с агрегатными функциями)

**Категории, где больше 5 товаров:**
```sql
SELECT 
    category,
    COUNT(*) as total
FROM products
GROUP BY category
HAVING COUNT(*) > 5;
```

---
**WHERE:**
- Фильтрует **строки**
- Работает **перед** группировкой
- Нельзя использовать агрегатные функции

**HAVING:**
- Фильтрует **группы**
- Работает **после** группировки
- Можно использовать агрегатные функции

---
# Пример WHERE c HAVING

```sql
SELECT 
    category,
    COUNT(*) as total,
    AVG(price) as avg_price
FROM products
WHERE stock > 10              -- фильтр строк
GROUP BY category
HAVING AVG(price) > 5000      -- фильтр групп
ORDER BY avg_price DESC;
```


---
# Практический пример

**Найти категории со средней ценой выше 3000:**

```sql
SELECT 
    category,
    COUNT(*) as items,
    ROUND(AVG(price), 2) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM products
GROUP BY category
HAVING AVG(price) > 3000
ORDER BY avg_price DESC;
```

---
# Группировка клиентов по городам

```sql
SELECT 
    city,
    COUNT(*) as customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC;
```

**Результат:**
```
city             | customer_count
-----------------+---------------
Москва           |            6
Санкт-Петербург  |            2
```

---
# Полный порядок SQL запроса

```sql
SELECT              -- 1. Выбор столбцов
FROM                -- 2. Определение таблицы
WHERE               -- 3. Фильтрация строк
GROUP BY            -- 4. Группировка
HAVING              -- 5. Фильтрация групп
ORDER BY            -- 6. Сортировка
LIMIT               -- 7. Ограничение
```


---
# Типичные ошибки

 **Столбец не в GROUP BY:**
```sql
SELECT category, name, COUNT(*)
FROM products
GROUP BY category;  
```

 **Агрегатная функция в WHERE:**
```sql
SELECT category, AVG(price)
FROM products
WHERE AVG(price) > 5000;  
GROUP BY category;
```

---
# Практические примеры

**1. Категории с минимальным запасом < 50:**
```sql
SELECT category, SUM(stock) as total_stock
FROM products
GROUP BY category
HAVING SUM(stock) < 50;
```

**2. Средняя цена товаров в наличии:**
```sql
SELECT ROUND(AVG(price), 2) as avg_price
FROM products
WHERE stock > 0;
```

---
# Краткая шпаргалка

| Функция | Описание | Пример |
|---------|----------|--------|
| COUNT(*) | Количество строк | `COUNT(*)` |
| COUNT(DISTINCT col) | Уникальные значения | `COUNT(DISTINCT city)` |
| SUM(col) | Сумма | `SUM(price * stock)` |
| AVG(col) | Среднее | `AVG(price)` |
| MIN(col) | Минимум | `MIN(price)` |
| MAX(col) | Максимум | `MAX(stock)` |
| ROUND(num, n) | Округление | `ROUND(AVG(price), 2)` |
