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
# SQL и PostgreSQL
## Основы работы с реляционными базами данных

---
**SQL** (Structured Query Language) - язык структурированных запросов

**Для чего нужен:**
- Создание и управление базами данных
- Извлечение и анализ данных
- Обновление и удаление данных
- Создание отчётов

**SQL - стандарт для работы с реляционными БД**

---
# Что такое PostgreSQL?

**PostgreSQL** - мощная объектно-реляционная СУБД с открытым исходным кодом

- Поддержка сложных запросов
- ACID-совместимость (надёжность транзакций)
- Расширяемость и масштабируемость
- Кроссплатформенность

**Инструмент:** pgAdmin - графический интерфейс для работы с PostgreSQL

---
# Реляционная модель данных

**Данные хранятся в таблицах:**
- **Строки** (records/rows) - отдельные записи
- **Столбцы** (columns) - атрибуты/характеристики
- **Ключи** - связи между таблицами

**Пример таблицы Customers:**

| customer_id | name        | email              | city       |
|-------------|-------------|--------------------|------------|
| 1           | Иван Петров | ivan@mail.ru       | Москва     |
| 2           | Анна Иванова| anna@gmail.com     | Санкт-Петербург |

---
# Типы данных в PostgreSQL

| Тип         | Описание                    | Пример           |
|-------------|-----------------------------|------------------|
| INTEGER     | Целые числа                 | 42, -10          |
| DECIMAL     | Числа с фиксированной точностью | 99.99        |
| VARCHAR(n)  | Строка переменной длины     | 'Иван'           |
| TEXT        | Текст неограниченной длины  | 'Описание...'    |
| DATE        | Дата                        | '2026-01-29'     |
| TIMESTAMP   | Дата и время                | '2026-01-29 14:30:00' |
| BOOLEAN     | Логический тип              | TRUE, FALSE      |

---
# Создание базы данных и таблицы

**Создание базы данных:**
```sql
CREATE DATABASE shop_db;
```

**Создание таблицы:**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```

---
# Ключи и ограничения

**PRIMARY KEY** - первичный ключ (уникальный идентификатор)
```sql
product_id SERIAL PRIMARY KEY
```

**FOREIGN KEY** - внешний ключ (связь с другой таблицей)
```sql
customer_id INTEGER REFERENCES customers(customer_id)
```

**NOT NULL** - поле не может быть пустым
**UNIQUE** - все значения должны быть уникальными

---
# Основные SQL операции: CRUD

**C**reate - создание данных
**R**ead - чтение данных
**U**pdate - обновление данных
**D**elete - удаление данных

---
# INSERT - добавление данных

**Добавление одной записи:**
```sql
INSERT INTO products (name, category, price, stock)
VALUES ('Ноутбук', 'Электроника', 75000.00, 10);
```

**Добавление нескольких записей:**
```sql
INSERT INTO products (name, category, price, stock)
VALUES 
    ('Клавиатура', 'Электроника', 3500.00, 25),
    ('Мышь', 'Электроника', 1500.00, 50),
    ('Монитор', 'Электроника', 25000.00, 15);
```

---
# SELECT - чтение данных

**Выбрать все столбцы:**
```sql
SELECT * FROM products;
```

**Выбрать конкретные столбцы:**
```sql
SELECT name, price FROM products;
```

**С условием WHERE:**
```sql
SELECT name, price 
FROM products
WHERE price > 5000;
```

---
# WHERE - фильтрация данных

**Операторы сравнения:**
```sql
WHERE price = 1500           -- равно
WHERE price > 5000           -- больше
WHERE price <= 10000         -- меньше или равно
WHERE price <> 1500          -- не равно
WHERE price BETWEEN 1000 AND 5000  -- диапазон
```

**Текстовые условия:**
```sql
WHERE category = 'Электроника'
WHERE name LIKE 'Мо%'        -- начинается с 'Мо'
WHERE name LIKE '%тор%'      -- содержит 'тор'
```

---
**AND - все условия должны быть истинны:**
```sql
SELECT * FROM products
WHERE category = 'Электроника' AND price < 10000;
```
**OR - хотя бы одно условие истинно:**
```sql
SELECT * FROM products
WHERE category = 'Электроника' OR category = 'Одежда';
```
**IN - значение из списка:**
```sql
SELECT * FROM products
WHERE category IN ('Электроника', 'Одежда', 'Книги');
```

---

**По возрастанию (по умолчанию):**
```sql
SELECT name, price FROM products
ORDER BY price;
```

**По убыванию:**
```sql
SELECT name, price FROM products
ORDER BY price DESC;
```

**По нескольким столбцам:**
```sql
SELECT name, category, price FROM products
ORDER BY category, price DESC;
```

---
# LIMIT - ограничение результатов

**Первые 5 записей:**
```sql
SELECT * FROM products
LIMIT 5;
```

**ТОП-5 самых дорогих товаров:**
```sql
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 5;
```


---
# UPDATE - обновление данных

**Обновить одно поле:**
```sql
UPDATE products
SET price = 3000.00
WHERE product_id = 2;
```

**Обновить несколько полей:**
```sql
UPDATE products
SET price = price * 1.1,
    stock = stock + 10
WHERE category = 'Электроника';
```

---
# DELETE - удаление данных

**Удалить конкретные записи:**
```sql
DELETE FROM products
WHERE stock = 0;
```

**Удалить с условием:**
```sql
DELETE FROM products
WHERE created_at < '2025-01-01';
```


---
# Агрегатные функции


```sql
-- Количество товаров
SELECT COUNT(*) FROM products;

-- Средняя цена
SELECT AVG(price) FROM products;

-- Максимальная и минимальная цена
SELECT MAX(price), MIN(price) FROM products;

-- Общая сумма на складе
SELECT SUM(price * stock) FROM products;
```