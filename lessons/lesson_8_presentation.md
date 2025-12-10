---
marp: true
paginate: false

style: |
  table {
    font-size: 0.6em;
  }
  section {
    font-size: 2.5em;
  }
  section.centered {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }
---
<!-- _class: centered -->
# Практика и повторение

---

# Изучение данных

| Задача | Функция |
|--------|---------|
| Первые N строк | `df.head(n)` |
| Размер таблицы | `df.shape` |
| Типы данных | `df.dtypes` |
| Структура | `df.info()` |
| Статистика | `df.describe()` |
| Пропуски | `df.isna().sum()` |
| Уникальные | `df['col'].unique()` |
| Частота | `df['col'].value_counts()` |

---

# Очистка данных

| Задача | Код |
|--------|-----|
| Заполнить пропуски | `df['col'].fillna(value)` |
| Удалить пропуски | `df.dropna()` |
| Удалить дубликаты | `df.drop_duplicates()` |
| Нижний регистр | `df['col'].str.lower()` |
| Убрать пробелы | `df['col'].str.strip()` |
| Смена типа | `df['col'].astype(type)` |
| Фильтрация | `df[df['col'] > 5]` |

---

# Статистика

| Показатель | Функция |
|------------|---------|
| Среднее | `df['col'].mean()` |
| Медиана | `df['col'].median()` |
| Мода | `df['col'].mode()[0]` |
| Стд. отклонение | `df['col'].std()` |
| Размах | `max() - min()` |
| Квартили | `df['col'].quantile(0.25)` |
| Корреляция | `df['col1'].corr(df['col2'])` |

---

# Визуализация

| График | Функция |
|--------|---------|
| Гистограмма | `sns.histplot(df['col'])` |
| Boxplot | `sns.boxplot(x=df['col'])` |
| Countplot | `sns.countplot(data=df, x='col')` |
| Scatter | `sns.scatterplot(data=df, x='a', y='b')` |
| Barplot | `sns.barplot(data=df, x='a', y='b')` |
| Heatmap | `sns.heatmap(df.corr())` |
| KDE | `sns.kdeplot(df['col'])` |

---

# Feature Engineering

| Метод | Пример |
|-------|--------|
| Математика | `df['age'] = 2024 - df['year']` |
| Объединение | `df['total'] = df['a'] + df['b']` |
| Бинарный флаг | `df['is_old'] = (df['age'] > 10).astype(int)` |
| Категоризация | `pd.cut(df['col'], bins=3)` |
| Квантили | `pd.qcut(df['col'], q=4)` |

---

# Масштабирование

| Метод | Когда использовать |
|-------|-------------------|
| Min-Max | Нейросети, нет выбросов [0, 1] |
| Standard | Линейные модели, SVM |
| Robust | Есть выбросы |
| Log | Правый хвост |
| Box-Cox | Нужна нормальность |

---
---

# Пайплайн

1. Загрузка данных
2. Изучение (head, info, describe)
3. Очистка (пропуски, дубликаты, типы)
4. Визуализация
5. Статистика
6. Feature Engineering
7. Масштабирование
8. Выводы