# Практические задачи по SQL

## Базовый уровень

### Задача 1: Простая выборка
Напишите запрос, который выведет все товары категории "Мебель".

<details>
<summary>Решение</summary>

```sql
SELECT * 
FROM products 
WHERE category = 'Мебель';
```
</details>

---

### Задача 2: Сортировка
Выведите все товары, отсортированные по цене от самого дешевого к самому дорогому.

<details>
<summary>Решение</summary>

```sql
SELECT name, price 
FROM products 
ORDER BY price ASC;
```
</details>

---

### Задача 3: ТОП-3
Найдите 3 самых дорогих товара.

<details>
<summary>Решение</summary>

```sql
SELECT name, category, price 
FROM products 
ORDER BY price DESC 
LIMIT 3;
```
</details>

---

### Задача 4: Диапазон цен
Найдите все товары в ценовом диапазоне от 5000 до 15000.

<details>
<summary>Решение</summary>

```sql
SELECT name, price 
FROM products 
WHERE price BETWEEN 5000 AND 15000 
ORDER BY price;
```
</details>

---

### Задача 5: Поиск по части названия
Найдите все товары, в названии которых есть слово "для".

<details>
<summary>Решение</summary>

```sql
SELECT name, category, price 
FROM products 
WHERE name LIKE '%для%';
```
</details>

---

### Задача 6: Количество товаров
Подсчитайте общее количество товаров в базе данных.

<details>
<summary>Решение</summary>

```sql
SELECT COUNT(*) 
FROM products;
```
</details>

---

### Задача 7: Средняя цена
Найдите среднюю цену всех товаров.

<details>
<summary>Решение</summary>

```sql
SELECT AVG(price) 
FROM products;
```
</details>

---

### Задача 8: Клиенты из Москвы
Выведите имена и email всех клиентов из Москвы.

<details>
<summary> Решение</summary>

```sql
SELECT name, email, city 
FROM customers 
WHERE city = 'Москва';
```
</details>

---
### Задача 9: Товары с низким запасом
Найдите товары, которых на складе меньше 15 штук.

<details>
<summary>Решение</summary>

```sql
SELECT name, stock 
FROM products 
WHERE stock < 15 
ORDER BY stock;
```
</details>