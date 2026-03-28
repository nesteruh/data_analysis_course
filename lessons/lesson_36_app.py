import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing
 
from sklearn.metrics import mean_squared_error, r2_score
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Lesson 36", layout="wide")
st.title("Предсказание цены жилья с использованием обученной модели")

@st.cache_data
def load_and_train_model():
    """Загружаем датасет и обучаем модель (выполняется один раз)"""
    housing = fetch_california_housing()
    X = pd.DataFrame(housing.data, columns=housing.feature_names)
    y = pd.Series(housing.target, name="Price")
    
    y = y * 100  
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=15) 
    model.fit(X, y)
    
    y_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2 = r2_score(y, y_pred)
    
    return model, X, y, rmse, r2

def explain_prediction(model, X_full, input_values, prediction):
    """Объясняет как веса влияют на предсказание"""
    mean_values = X_full.mean()
    
    deviations = input_values[0] - mean_values.values
    
    explanation_df = pd.DataFrame({
        'Признак': X_full.columns,
        'Среднее в датасете': mean_values.values,
        'Ваше значение': input_values[0],
        'Отклонение': deviations,
        'Важность': model.feature_importances_
    })
    
    explanation_df['|Отклонение|'] = np.abs(explanation_df['Отклонение'])
    explanation_df = explanation_df.sort_values('|Отклонение|', ascending=False)
    
    return explanation_df
model, X_full, y_full, rmse, r2 = load_and_train_model()


with st.sidebar:
    st.header("О модели")
    st.write("**Тип:** Random Forest Regression")
    st.write("**Датасет:** California Housing")
    st.write(f"**Примеров в обучении:** {len(X_full):,}")
    st.metric("RMSE", f"${rmse:.2f}k")
    st.metric("R² Score", f"{r2:.3f}")
    
    st.divider()
    st.subheader("Инструкция:")
    st.write("""
    1. Выберите значения параметров слева
    2. Нажмите кнопку "Предсказать"
    3. Посмотрите на результат и график важности признаков
    """)

st.subheader("Параметры для предсказания")

col1, col2 = st.columns(2)

with col1:
    st.write("Базовые параметры")
    median_income = st.slider(
        "Средний доход семьи",
        min_value=0.5,
        max_value=15.0,
        value=3.0,
        step=0.5,
        help="В единицах $10,000 (например, 3.0 = $30,000)"
    )
    
    house_age = st.slider(
        "Возраст дома",
        min_value=1,
        max_value=52,
        value=25,
        step=1,
        help="В годах"
    )
    
    ave_rooms = st.slider(
        "Среднее комнат на дом",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5,
        help="Средний размер дома в районе"
    )

with col2:
    st.write("Параметры населения")
    ave_bedrooms = st.slider(
        "Среднее спален на дом",
        min_value=0.5,
        max_value=5.0,
        value=1.1,
        step=0.1,
        help="Средний размер спален в районе"
    )
    
    population = st.slider(
        "Население блока",
        min_value=0,
        max_value=35000,
        value=1500,
        step=500,
        help="Примерное население в районе"
    )
    
    ave_occupancy = st.slider(
        "Среднее людей на домохозяйство",
        min_value=1.0,
        max_value=10.0,
        value=3.0,
        step=0.5,
        help="Среднее количество жильцов на дом"
    )


st.divider()
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

with col_btn1:
    predict_button = st.button(
        "Предсказать цену",
        type="primary",
        use_container_width=True
    )

with col_btn2:
    reset_button = st.button(
        "Сброс",
        use_container_width=True
    )


if predict_button:
    with st.spinner("Предсказание..."):
        input_data = np.array([[
            median_income,
            house_age,
            ave_rooms,
            ave_bedrooms,
            population,
            ave_occupancy
        ]])
        
        input_full = np.concatenate([
            input_data,
            np.array([[35.0, -118.0]])  
        ], axis=1)
        
        prediction = model.predict(input_full)[0]
        
        st.success("Предсказание готово!")
        
        st.subheader("Результат предсказания")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Предсказанная цена",
                f"${prediction*1000:,.0f}",
                help="Цена дома в долларах"
            )
        
        with col2:
            confidence_interval = prediction * 0.15  
            st.metric(
                "Доверительный интервал",
                f"±${confidence_interval*1000:,.0f}",
                help="Примерная ошибка модели (±15%)"
            )
        
        with col3:
            median_price = y_full.median()
            diff_percent = ((prediction - median_price/100) / (median_price/100)) * 100
            st.metric(
                "Медиана цены",
                f"{diff_percent:+.1f}%",
                help="Насколько дороже/дешевле типичного дома"
            )
        
        st.subheader("Использованные параметры:")
        params_df = pd.DataFrame({
            'Параметр': ['Доход ($10k)', 'Возраст дома', 'Комнат/дом', 'Спален/дом', 'Население', 'Люди/дом'],
            'Значение': [f'{median_income}', f'{house_age} лет', f'{ave_rooms:.1f}', f'{ave_bedrooms:.1f}', f'{population}', f'{ave_occupancy:.1f}']
        })
        st.dataframe(params_df, use_container_width=True, hide_index=True)
        
        
        st.divider()
        
        explanation_df = explain_prediction(model, X_full, input_full, prediction)
        
        st.write("**Вклад каждого признака в формирование цены:**")
        
        explanation_display = explanation_df[['Признак', 'Среднее в датасете', 'Ваше значение', 'Отклонение', 'Важность']].copy()
        explanation_display = explanation_display.round(2)
        explanation_display['Важность (%)'] = (explanation_display['Важность'] * 100).round(1).astype(str) + '%'
        explanation_display = explanation_display.drop('Важность', axis=1)
        
        st.dataframe(explanation_display, use_container_width=True, hide_index=True)
        
        contrib_df = explanation_df[['Признак', 'Отклонение', 'Важность']].copy()
        contrib_df['Вес вклада'] = contrib_df['Отклонение'] * contrib_df['Важность']
        contrib_df = contrib_df.sort_values('Вес вклада', key=abs, ascending=True)
        
        colors = ['red' if x < 0 else 'green' for x in contrib_df['Вес вклада']]
        
        fig_contrib = go.Figure()
        fig_contrib.add_trace(go.Bar(
            y=contrib_df['Признак'],
            x=contrib_df['Вес вклада'],
            orientation='h',
            marker=dict(color=colors),
            text=contrib_df['Вес вклада'].apply(lambda x: f'{x:.3f}'),
            textposition='auto'
        ))
        
        fig_contrib.update_layout(
            title="Как каждый признак влияет на цену",
            xaxis_title="Вклад (относительный)",
            yaxis_title="Признак",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_contrib, use_container_width=True)
        
        st.divider()
        st.subheader(" Важность признаков для модели")
        
        feature_importance = pd.DataFrame({
            'Feature': X_full.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                y=feature_importance['Feature'],
                x=feature_importance['Importance'],
                orientation='h',
                marker=dict(color='blue')
            )
        ])
        
        fig.update_layout(
            title="Какие параметры влияют на цену дома",
            xaxis_title="Важность",
            yaxis_title="Признак",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Нажмите кнопку 'Предсказать цену' чтобы получить результат")

st.divider()
st.subheader("Статистика датасета")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Мин. цена", f"${y_full.min()*1000:.0f}")

with col2:
    st.metric("Макс. цена", f"${y_full.max()*1000:.0f}")

with col3:
    st.metric("Средняя цена", f"${y_full.mean()*1000:.0f}")

with col4:
    st.metric("Медиана цены", f"${y_full.median()*1000:.0f}")