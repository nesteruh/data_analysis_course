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
# Support Vector Machines (SVM)
## Классификация с максимальным зазором

---
# Основная идея SVM

**Support Vector Machine** находит гиперплоскость с **максимальным зазором** (margin) между классами.

**Ключевые идеи:**
- Граница должна проходить **далеко** от обоих классов
- Более устойчива к шуму и лучше обобщается
- **Support vectors** - точки на границе margin, определяют модель
- Остальные точки не влияют на границу

---
# Визуализация SVM
![w:500](/images/svm_example.png)
**Support vectors** определяют положение гиперплоскости  
**Margin** = расстояние между гиперплоскостью и ближайшими точками. **Цель SVM:** Максимизировать margin

---
**Hard Margin SVM:**
- Все точки должны быть правильно классифицированы
- **Проблема:** не работает, если данные не линейно разделимы

**Soft Margin SVM:**
- Допускает некоторые ошибки
- Баланс между максимизацией margin и минимизацией ошибок
- Контролируется параметром **C**
---
![w:1000](/images/hard_soft_margin.png)

---
**C** - штраф за неправильную классификацию(regularization)

**Большой C (например, 100):**
- Жесткий штраф за ошибки
- Узкий margin, меньше ошибок на train
- Риск **overfitting**

**Малый C (например, 0.01):**
- Мягкий штраф за ошибки
- Широкий margin, больше ошибок на train
- Риск **underfitting**

---
# Kernel Trick

**Проблема:** Что если данные не линейно разделимы?
![w:900](/images/kernel_trick.png)

**Решение:** Kernel trick - проецирование в высшие измерения

---
![w:900](/images/types_of_kernels.png)

---
**Gaussian RBF:**
$$K(x, y) = e^{-\gamma ||x - y||^2}$$

**Параметр γ (gamma):**
- **Большая γ** - узкие "колокола", влияние только близких точек -> overfitting
- **Малая γ** - широкие "колокола", влияние дальних точек-> underfitting

**RBF может создавать круговые/эллиптические границы**

---
![w:900](/images/kernels_formula.png)

---
# Основные гиперпараметры SVM

| Параметр | Описание | Типичные значения |
|----------|----------|------------------|
| `C` | Штраф за ошибки | 0.1, 1, 10, 100 |
| `kernel` | Тип ядра | 'linear', 'rbf', 'poly' |
| `gamma` | Коэффициент для rbf/poly |  0.001, 0.01 |
| `degree` | Степень для poly | 2, 3, 4 |

**По умолчанию:** `C=1.0`, `kernel='rbf'`

---
**SVC** (Support Vector Classification):
- Поддерживает все kernels
- Медленнее на больших данных
- Использует libsvm

**LinearSVC**:
- Только linear kernel
- Быстрее на больших данных
- Использует liblinear

---
**Хорошо подходит:**
- Высокоразмерные данные (много признаков)
- Четкое разделение между классами
- Малое/среднее количество примеров
- Нелинейные границы (с RBF kernel)
- Классификация текстов, изображений

**Не подходит:**
- Очень большие данные (> 100,000 примеров)
- Много шума и перекрытий между классами

---
# Преимущества SVM

Эффективен в высоких размерностях  
Работает, когда признаков больше, чем примеров  
Kernel trick для нелинейных границ  
Робастен к overfitting (при правильном C)  
Только support vectors влияют на модель (компактность)

---
# Недостатки SVM

Медленный на больших данных  
Чувствителен к масштабу признаков  
Выбор kernel и параметров требует экспериментов  
Нет вероятностных предсказаний (по умолчанию)  
Сложно интерпретировать (особенно с RBF)  
Только бинарная классификация (One-vs-Rest для multiclass)

---

```python
# 1. Подготовка
X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 2. Подбор параметров

from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
    'kernel': ['linear', 'rbf']
}

grid = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy')
grid.fit(X_train_scaled, y_train)

print(f"Лучшие параметры: {grid.best_params_}")
```

---
# Вероятностные предсказания

**По умолчанию:** SVC возвращает только классы (0 или 1)

**Для вероятностей:**
```python
svm = SVC(kernel='rbf', C=1, probability=True)
svm.fit(X_train, y_train)

proba = svm.predict_proba(X_test)  # [[P(0), P(1)]]
```


---
**Для multiclass (> 2 классов):**
- **One-vs-Rest (OvR)** - по умолчанию
  - N классов -> N моделей
  - Каждая модель: класс i vs все остальные
  
- **One-vs-One (OvO)**
  - N классов -> N*(N-1)/2 моделей
  - Каждая модель: класс i vs класс j

```python
svm = SVC(decision_function_shape='ovr')  # или 'ovo'
```

---
**Основная идея:** Найти границу с максимальным margin

**Ключевые параметры:**
- **C** - штраф за ошибки (0.1, 1, 10, 100)
- **kernel** - linear или rbf
- **gamma** - для rbf (0.001, 0.01, 0.1)

**Критично важно:**
- StandardScaler перед обучением
- GridSearchCV для подбора параметров
- Проверить количество support vectors

**Когда использовать:** Малые/средние данные, высокая размерность, нелинейные границы