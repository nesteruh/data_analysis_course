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
    align-items: start;
  }
  code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
  }
  pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 5px;
  }
---

<!-- _class: centered -->

# ML: Лучшие практики

### Как строить модели правильно


---


Но хорошая модель - это не просто `model.fit(X, y)`.

**Частые ошибки:**
- Модель хорошо на train, плохо на тестовых данных
- Метрика accuracy = 95%, но модель бесполезна
- Добавили больше признаков - модель стала хуже
- Везде используют одни и те же параметры по умолчанию



---

```
1. Overfitting / Underfitting
   └─ Диагностика модели

2. Cross-Validation
   └─ Надёжная оценка качества

3. Регуляризация (L1 / L2)
   └─ Борьба с переобучением

4. Несбалансированные данные
   └─ Когда accuracy обманывает

5. Pipeline
   └─ Воспроизводимость и чистота кода
```

---

<!-- _class: centered -->

## Блок 1
# Overfitting / Underfitting

---

# Bias-Variance Tradeoff

**Ошибка модели состоит из трёх частей:**

$$\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}$$

| Компонент | Что это | Симптом |
|-----------|---------|---------|
| **Bias** | Систематическая ошибка | Underfitting |
| **Variance** | Чувствительность к данным | Overfitting |
| **Noise** | Шум в данных | Неустранимо |

> Цель: найти баланс между bias и variance

---

 Underfitting (высокий Bias)

- Слишком простая модель (линейная на нелинейных данных)
- Слишком мало признаков
- Слишком высокая регуляризация

**Решения:**
- Усложнить модель (больше деревьев, глубже нейросеть)
- Добавить признаки (feature engineering)
- Уменьшить регуляризацию

---

 Overfitting (высокая Variance)


**Причины:**
- Слишком сложная модель
- Слишком мало обучающих данных
- Слишком много признаков

**Решения:**
- Регуляризация
- Уменьшить сложность модели (pruning, max_depth)
- Cross-validation для честной оценки

---

# Диагностика: Learning Curves

**Learning Curve** - как меняется ошибка при увеличении обучающих данных

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='neg_mean_squared_error'
)
```

---

# Как читать Learning Curves

<div class="two-columns">

<div>

**Underfitting:**
- Train score плохой
- Val score плохой
- Оба примерно одинаковы

**Что делать:** усложнить модель

</div>

<div>

**Overfitting:**
- Train score отличный
- Val score плохой
- Большой разрыв между ними

**Что делать:** регуляризация, больше данных

</div>
</div>

> Хорошая модель: train ≈ val, оба достаточно хорошие

---

# Validation Curve

**Как меняется качество при изменении гиперпараметра?**

```python
from sklearn.model_selection import validation_curve

train_scores, val_scores = validation_curve(
    model, X, y,
    param_name='max_depth',
    param_range=[1, 2, 3, 5, 7, 10, 15, 20],
    cv=5, scoring='accuracy'
)
```

> Помогает найти оптимальное значение гиперпараметра

---

<!-- _class: centered -->

## Блок 2
# Cross-Validation

---

# Проблема простого Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

- Результат зависит от случайного разбиения (`random_state`)
- При малом датасете test может не быть репрезентативным
- Мы "тратим" 20% данных только на оценку

> Как узнать - модель хороша или нам просто повезло с разбиением?

---

# K-Fold Cross-Validation

**Идея:** разбить данные на K частей (folds), обучать K раз

```
Данные: [F1 | F2 | F3 | F4 | F5]

Итерация 1: Train=[F2,F3,F4,F5] | Val=[F1]
Итерация 2: Train=[F1,F3,F4,F5] | Val=[F2]
Итерация 3: Train=[F1,F2,F4,F5] | Val=[F3]
Итерация 4: Train=[F1,F2,F3,F5] | Val=[F4]
Итерация 5: Train=[F1,F2,F3,F4] | Val=[F5]

Финальная оценка: mean(score_1, ..., score_5)
```

---

# K-Fold в коде

```python
from sklearn.model_selection import cross_val_score, KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(
    model, X, y,
    cv=kf,
    scoring='accuracy'
)

print(f"Scores: {scores}")
print(f"Mean:   {scores.mean():.4f}")
print(f"Std:    {scores.std():.4f}")
```


---

# StratifiedKFold

Если классов мало, один fold может содержать только один класс

**StratifiedKFold** сохраняет пропорции классов в каждом fold:

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(
    model, X, y,
    cv=skf,
    scoring='f1'
)
```

> Для классификации всегда используйте `StratifiedKFold`!

---

# Как выбрать K?

| K | Плюсы | Минусы |
|---|-------|--------|
| **5** | Быстро, стандарт | Менее точная оценка |
| **10** | Стандарт для исследований | Медленнее |
| **Большой (n)** | Максимально точная оценка | Очень медленно |
| **Leave-One-Out** | Всё обуч. множество | Экстремально медленно |

- Малый датасет (< 1000): K = 10 или LOO
- Средний датасет: K = 5 или 10
- Большой датасет (> 100k): K = 3

---

# cross_validate - больше деталей

```python
from sklearn.model_selection import cross_validate

results = cross_validate(
    model, X, y,
    cv=5,
    scoring=['accuracy', 'f1', 'roc_auc'],
    return_train_score=True  # видим train vs val
)

print(f"Train accuracy: {results['train_accuracy'].mean():.4f}")
print(f"Val   accuracy: {results['test_accuracy'].mean():.4f}")
# Большая разница => overfitting!
```

---

<!-- _class: centered -->

## Блок 3
# Регуляризация

---


**Проблема:** При обучении модель может присвоить огромные веса шумным признакам

**Пример:**
```
y = 0.5*x1 + 0.3*x2 + 0.1*x3

Но модель выучила:
y = 100*x1 - 99.5*x2 + 0.5*x3 + ...
```

**Регуляризация:** добавляем штраф за большие веса в функцию потерь

$$\text{Loss} = \text{MSE} + \lambda \cdot \text{penalty}$$

---

# L2 Регуляризация (Ridge)

$$\text{Loss} = \text{MSE} + \lambda \sum w_i^2$$

- Штрафует **квадрат** весов
- Все веса уменьшаются, но не до нуля

**Когда использовать:**
- Все признаки важны, но нужно уменьшить их влияние
- Мультиколлинеарность признаков

```python
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)   # alpha = λ
```

---

# L1 Регуляризация (Lasso)

$$\text{Loss} = \text{MSE} + \lambda \sum |w_i|$$

- Некоторые веса обнуляются полностью
- Автоматический **feature selection**!

**Когда использовать:**
- Много признаков, часть из них шумные
- Нужна интерпретируемая, "разреженная" модель

```python
from sklearn.linear_model import Lasso
model = Lasso(alpha=1.0)   # alpha = λ
```

---

# L1 и L2: визуальный смысл

<div class="two-columns">

<div>

**Ridge (L2):**
- Ограничение - сфера
- Минимум функции потерь редко попадает в угол
- Веса близки к нулю, но ≠ 0

</div>

<div>

**Lasso (L1):**
- Ограничение - ромб
- Минимум часто попадает в **угол ромба**
- Часть весов = 0 (разреженность)

</div>
</div>

> **ElasticNet** - комбинация L1 + L2

```python
from sklearn.linear_model import ElasticNet
model = ElasticNet(alpha=1.0, l1_ratio=0.5)
```

---

# Параметр alpha (λ)

**alpha** контролирует силу регуляризации:

| alpha | Эффект |
|-------|--------|
| **0** | Нет регуляризации (обычная линейная регрессия) |
| **0.01** | Слабая регуляризация |
| **1.0** | Стандартное значение |
| **100** | Сильная регуляризация, модель очень проста |

**Как выбрать alpha:** через `RidgeCV` / `LassoCV` или `GridSearchCV`

```python
from sklearn.linear_model import RidgeCV
model = RidgeCV(alphas=[0.01, 0.1, 1.0, 10, 100], cv=5)
```

---

# Регуляризация для деревьев

У деревьев нет L1/L2, но есть свои параметры регуляризации:

| Параметр | Эффект |
|----------|--------|
| `max_depth` | Ограничивает глубину дерева |
| `min_samples_split` | Мин. кол-во точек для разбиения |
| `min_samples_leaf` | Мин. кол-во точек в листе |
| `max_features` | Сколько признаков рассматривать |
| `n_estimators` | Для RF/GBM: больше = стабильнее |

> Все эти параметры подбираем через GridSearchCV и cross-validation

---

<!-- _class: centered -->

## Блок 4
# Несбалансированные данные

---

# Проблема дисбаланса классов

**Пример:** датасет мошеннических транзакций
- 99% - нормальные транзакции
- 1% - мошеннические

**"Умная" модель:** предсказывает всегда класс 0
- Accuracy = **99%** 
- Но fraud не обнаруживает вообще

> Accuracy бесполезна при несбалансированных данных

---

# Правильные метрики для дисбаланса

**Confusion Matrix:**

|  | Predicted 0 | Predicted 1 |
|--|-------------|-------------|
| **Actual 0** | TN | FP |
| **Actual 1** | FN | TP |

---
![w:1200](../images/precision_recall.png)

---

# Когда что важнее?

<div class="two-columns">

<div>

**Высокий Recall важнее:**
- Онкология: лучше лишний раз проверить
- Fraud detection: лучше заблокировать лишний раз
- Спам: лучше пропустить спам, чем важное письмо

</div>

<div>

**Высокий Precision важнее:**
- Рекомендации: лучше меньше, но релевантнее
- Юридические системы: ложное обвинение = плохо

</div>
</div>

> **AUC-ROC** - универсальная метрика, не зависит от порога

---

# Стратегии борьбы с дисбалансом

**1. class_weight='balanced' (самый простой способ):**
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(class_weight='balanced', random_state=42)
```
Модель учитывает редкий класс с бо́льшим весом.

---

**2. Undersampling - уменьшить мажоритарный класс:**
```python
from sklearn.utils import resample

majority = df[df.target == 0]
minority = df[df.target == 1]

majority_down = resample(majority,
                         n_samples=len(minority),
                         random_state=42)
balanced_df = pd.concat([majority_down, minority])
```
- Быстро, теряем данные
- Подходит при очень большом датасете

---

**3. Oversampling - увеличить миноритарный класс:**
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

**SMOTE** (Synthetic Minority Over-sampling Technique):
- Создаёт **синтетические** примеры миноритарного класса
- Не просто дублирует, а интерполирует между соседями
- Только на train данных! Никогда не трогать test.

---

# Чеклист для несбалансированных данных

 Проверить баланс классов: `y.value_counts()`  
 Не использовать accuracy как основную метрику  
 Выбрать метрику: F1, Precision, Recall, AUC-ROC  
 Стратегия: `class_weight`, undersampling или SMOTE  
 При CV использовать `StratifiedKFold`  
 SMOTE применять **только после** разбиения на train/test  

---

<!-- _class: centered -->

## Блок 5
# Pipeline

---



```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # не fit!

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
```

**Проблемы:**
- Легко забыть `transform` вместо `fit_transform` на тесте
- При CV нужно повторять всё вручную
- Код сложно читать и воспроизводить

---


**Data Leakage:** когда информация из тестовых данных "просачивается" в обучение

```python
# НЕПРАВИЛЬНО: scaler обучен на всех данных!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # ← видит тестовые данные

X_train, X_test = train_test_split(X_scaled, ...)
```

**Правильно: scaler обучается только на train:**
```python
X_train, X_test = train_test_split(X, ...)
scaler.fit(X_train)             # ← только train
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)
```


---

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  LogisticRegression())
])

pipe.fit(X_train, y_train)   # scaler.fit_transform + model.fit
y_pred = pipe.predict(X_test)  # scaler.transform + model.predict
```

**Pipeline гарантирует:**
- scaler никогда не видит тестовые данные
- Всё в одном месте, легко читать

---

# Pipeline и Cross-Validation

```python
from sklearn.model_selection import cross_val_score

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', Ridge(alpha=1.0))
])

# На каждом fold: fit только на train, transform train и val
scores = cross_val_score(pipe, X, y, cv=5, scoring='r2')
print(f"R² = {scores.mean():.4f} ± {scores.std():.4f}")
```

> Это единственный правильный способ делать CV с preprocessing!

---


**Реальные данные:** разные типы признаков требуют разной обработки

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
```

---

```python
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', RandomForestClassifier(n_estimators=100))
])

full_pipeline.fit(X_train, y_train)
y_pred = full_pipeline.predict(X_test)
```

> Один объект, который делает всё: заполняет пропуски, масштабирует, кодирует, обучает

---

# Pipeline + GridSearchCV

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'model__alpha': [0.01, 0.1, 1.0, 10, 100],
    # формат: 'имя_шага__параметр'
}

grid_search = GridSearchCV(
    pipe, param_grid,
    cv=5, scoring='r2'
)
grid_search.fit(X_train, y_train)
print(f"Лучший alpha: {grid_search.best_params_}")
```

---

# Чеклист ML-проекта

| Шаг | Что делаем |
|-----|------------|
| **1. Split** | Train/Test разбиение до любого preprocessing |
| **2. Baseline** | Простая модель для сравнения |
| **3. Диагностика** | Learning curve - overfit или underfit? |
| **4. CV** | StratifiedKFold для честной оценки |
| **5. Регуляризация** | Ridge/Lasso/ElasticNet при переобучении |
| **6. Дисбаланс** | class_weight / SMOTE + правильные метрики |
| **7. Pipeline** | Весь preprocessing внутри Pipeline |
| **8. Финальный test** | В самом конце |

---

# Главные правила

 **Тестовые данные - священны.** Смотреть на них можно только один раз - в конце.

 **Preprocessing внутри Pipeline.** Никогда не делать `fit_transform` на всём датасете.

 **Cross-validation вместо одного split.** 

 **Accuracy - худшая метрика при дисбалансе.** F1 / AUC-ROC.

 **Regularization - первый инструмент при overfitting.**

---

| Проблема | Решение |
|---------|---------|
| Overfitting | Регуляризация, больше данных, упрощение модели |
| Underfitting | Сложнее модель, новые признаки |
| Нестабильная оценка | Cross-Validation |
| Дисбаланс классов | class_weight, SMOTE, правильные метрики |
| Data Leakage | Pipeline |

---

<!-- _class: centered -->

## Блок 6
# Как выбирать модель на практике

---

# Шаг 1: определить задачу и формат данных

| Что предсказываем | Тип задачи | Примеры моделей |
|-------------------|------------|-----------------|
| Число (цена, спрос, время) | Регрессия | Linear/Ridge/Lasso, RandomForestRegressor, XGBoostRegressor |
| Класс (0/1 или несколько) | Классификация | LogisticRegression, SVC, DecisionTree, RandomForest, XGBoost |
| Группы без target | Кластеризация | KMeans, DBSCAN |
| Сжатие/визуализация признаков | Снижение размерности | PCA, t-SNE (визуализация) |


---

# Регрессия: когда какую модель брать

| Ситуация | Что пробовать первым | Когда усиливать |
|----------|----------------------|-----------------|
| Небольшой/средний датасет, нужна интерпретация | LinearRegression | Ridge/Lasso при переобучении или мультиколлинеарности |
| Много признаков, есть шум | Lasso / ElasticNet | RandomForest/XGBoost, если есть нелинейности |
| Сильные нелинейные зависимости | RandomForestRegressor | Gradient Boosting/XGBoost при высоких требованиях к качеству |
| Есть выбросы и нестабильность | MAE как метрика + robust preprocessing | Ансамбли + feature engineering |

**Техники:**
- Метрики: `MAE`, `RMSE`, `R²`
- Валидация: `KFold` + `cross_val_score`
- Подбор: `GridSearchCV` или `RandomizedSearchCV`

---

# Классификация: выбор по бизнес-цели

| Условие | Базовая модель | Что важно настроить |
|---------|----------------|---------------------|
| Нужна объяснимость (скоринг, риск) | LogisticRegression | Регуляризация `C`, порог классификации |
| Много нелинейностей/взаимодействий | RandomForest / XGBoost | `max_depth`, `n_estimators`, `learning_rate` |
| Чистые числовые признаки, сложная граница | SVC | `kernel`, `C`, `gamma`, обязательный scaling |
| Быстрый и простой baseline для текста | Naive Bayes | Тип NB (Gaussian/Multinomial/Bernoulli) |

---


| Цель | Подход | Когда применять |
|------|--------|-----------------|
| Разделить клиентов/объекты на группы | KMeans | Есть гипотеза о числе кластеров, признаки масштабированы |
| Найти плотные группы и выбросы | DBSCAN | Кластеры произвольной формы, есть шум |
| Сжать пространство признаков | PCA | Много коррелированных числовых признаков |
- Перед KMeans/DBSCAN/PCA обычно нужен `StandardScaler`
- Для KMeans подбирать `n_clusters` через elbow/silhouette
- Оценивать кластеры ещё и бизнес-интерпретацией

---


| Тип данных | Что делать в preprocessing | Какие модели часто лучше |
|------------|-----------------------------|---------------------------|
| Табличные числовые | `imputer` + scaling | Линейные модели, SVM, KNN, PCA |
| Табличные смешанные (число + категории) | `ColumnTransformer` + OneHotEncoder | LogisticRegression, деревья, RandomForest, boosting |
| Много пропусков | Явная импутация + индикатор пропуска | Деревья/ансамбли часто устойчивее |
| Очень много признаков | L1/ElasticNet, PCA, отбор признаков | Линейные с регуляризацией, boosting |
| Мало данных | Простые модели + сильная CV | Logistic/Linear, неглубокие деревья |

---


1. **Baseline:** простая модель (Linear/Logistic/Decision Tree) + понятная метрика.
2. **Честная оценка:** `cross-validation` (для классов - `StratifiedKFold`).
3. **Диагностика:** learning/validation curves, анализ ошибок по группам.
4. **Усиление модели:** регуляризация, tuning, ансамбли.
5. **Контроль качества:** сравнение с baseline на отложенном test.
6. **Продакшн-готовность:** весь preprocessing и  `Pipeline`.


---

# Быстрая карта решений

| Если... | То начать с... | Затем попробовать... |
|---------|----------------|----------------------|
| Нужна объяснимая регрессия | LinearRegression | Ridge/Lasso/ElasticNet |
| Нужна объяснимая классификация | LogisticRegression | Threshold tuning + class_weight |
| Важна максимальная точность на табличных данных | RandomForest | XGBoost/LightGBM/CatBoost |
| Нужна сегментация без target | KMeans | DBSCAN + PCA для анализа |
| Сильный дисбаланс классов | class_weight + F1/Recall | SMOTE + порог + calibration |
