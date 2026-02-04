# Практические задачи по SQL 
## Агрегатные функции и GROUP BY

---

### Задача 1: Общее количество товаров
Подсчитайте общее количество товаров в базе данных.

<details>
<summary>Решение</summary>

```sql
SELECT COUNT(*) as total_products 
FROM products;
```
</details>

---

### Задача 2: Количество уникальных категорий
Найдите количество уникальных категорий товаров.

<details>
<summary>Решение</summary>

```sql
SELECT COUNT(DISTINCT category) as unique_categories 
FROM products;
```
</details>

---

### Задача 3: Средняя цена товаров
Найдите среднюю цену всех товаров (округлите до 2 знаков).

<details>
<summary>Решение</summary>

```sql
SELECT ROUND(AVG(price), 2) as average_price 
FROM products;
```
</details>

---

### Задача 4: Самый дешёвый и самый дорогой товар
Найдите минимальную и максимальную цену товаров.

<details>
<summary>Решение</summary>

```sql
SELECT 
    MIN(price) as min_price,
    MAX(price) as max_price
FROM products;
```
</details>

---

### Задача 5: Общее количество на складе
Подсчитайте общее количество всех товаров на складе (сумма stock).

<details>
<summary>Решение</summary>

```sql
SELECT SUM(stock) as total_stock 
FROM products;
```
</details>

---

### Задача 6: Товары по категориям
Подсчитайте количество товаров в каждой категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    COUNT(*) as product_count
FROM products
GROUP BY category
ORDER BY product_count DESC;
```
</details>

---

### Задача 7: Средняя цена по категориям
Найдите среднюю цену товаров для каждой категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    ROUND(AVG(price), 2) as avg_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;
```
</details>

---

### Задача 8: Запасы по категориям
Для каждой категории найдите общее количество товаров на складе.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    SUM(stock) as total_stock
FROM products
GROUP BY category
ORDER BY total_stock DESC;
```
</details>

---

### Задача 9: Общая стоимость запасов
Рассчитайте общую стоимость всех товаров на складе (цена × количество) для каждой категории. (в sql есть математические операции, например можно умножать числовые колонки - price * stock)

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    SUM(price * stock) as inventory_value
FROM products
GROUP BY category
ORDER BY inventory_value DESC;
```
</details>

---

### Задача 10: Категории с большим количеством товаров
Найдите категории, в которых больше 5 товаров.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    COUNT(*) as product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 5;
```
</details>

---

### Задача 11: Дорогие категории
Найдите категории, где средняя цена товаров выше 5000.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    ROUND(AVG(price), 2) as avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 5000
ORDER BY avg_price DESC;
```
</details>

---

### Задача 12: Клиенты по городам
Подсчитайте количество клиентов в каждом городе.

<details>
<summary>Решение</summary>

```sql
SELECT 
    city,
    COUNT(*) as customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC;
```
</details>

---

### Задача 13: Средняя цена электроники
Найдите среднюю цену товаров категории "Электроника".

<details>
<summary>Решение</summary>

```sql
SELECT 
    ROUND(AVG(price), 2) as avg_electronics_price
FROM products
WHERE category = 'Электроника';
```
</details>

---

### Задача 14: Количество дорогих товаров
Подсчитайте количество товаров дороже 10000 в каждой категории.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    COUNT(*) as expensive_products
FROM products
WHERE price > 10000
GROUP BY category
ORDER BY expensive_products DESC;
```
</details>

---

### Задача 15: Категории с малым запасом
Найдите категории, где общий запас товаров меньше 100 штук.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    SUM(stock) as total_stock
FROM products
GROUP BY category
HAVING SUM(stock) < 100
ORDER BY total_stock;
```
</details>

---

### Задача 16: Города с несколькими клиентами
Найдите города, в которых зарегистрировано более 2 клиентов.

<details>
<summary>Решение</summary>

```sql
SELECT 
    city,
    COUNT(*) as customer_count
FROM customers
GROUP BY city
HAVING COUNT(*) > 2
ORDER BY customer_count DESC;
```
</details>

---

### Задача 17: Самая дешёвая категория
Найдите категорию с самой низкой средней ценой.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    ROUND(AVG(price), 2) as avg_price
FROM products
GROUP BY category
ORDER BY avg_price ASC
LIMIT 1;
```
</details>

---

### Задача 18: Комплексная аналитика
Создайте полный отчёт по категориям, включающий:
- Название категории
- Количество товаров
- Минимальную цену
- Максимальную цену
- Среднюю цену (округлённую)
- Общий запас
- Общую стоимость запасов

Отсортируйте по общей стоимости по убыванию.

<details>
<summary>Решение</summary>

```sql
SELECT 
    category,
    COUNT(*) as total_products,
    MIN(price) as min_price,
    MAX(price) as max_price,
    ROUND(AVG(price), 2) as avg_price,
    SUM(stock) as total_stock,
    SUM(price * stock) as total_value
FROM products
GROUP BY category
ORDER BY total_value DESC;