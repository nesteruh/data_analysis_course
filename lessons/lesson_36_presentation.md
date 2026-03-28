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

# Streamlit: ML приложения

### Как превратить модель в интерактивное веб-приложение



---

# Что мы будем делать

1. **Загружаем pre-trained модель** - регрессия для предсказания цены
2. **Создаём UI** - ползунки для ввода параметров
3. **Оптимизируем** - кэширование моделей `@st.cache_data`
4. **Deploy** - публикуем на Streamlit Cloud 


---

# Кэширование: @st.cache_data


```python
@st.cache_data
def train_model():
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    return model

model = train_model()  # Обучаем один раз
```

**Результат:** приложение работает быстро 

---

# Развёртывание (Deployment)

**Streamlit Cloud:**
1. Загружаем код на GitHub
2. Подключаем репозиторий в Streamlit Cloud
3. Приложение live за 1 минуту

```
https://your-username-app-name.streamlit.app
```



---

# Структура сегодняшнего приложения

```python
1. Загружаем датасет с ценами домов
2. @st.cache_data - обучаем модель один раз
3. Streamlit UI:
   - Ползунки для ввода площади, комнат, возраста
4. Предсказание:
   - Модель выдаёт предсказанную цену
   - Показываем доверительный интервал
```