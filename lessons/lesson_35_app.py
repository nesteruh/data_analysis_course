import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Lesson 35", layout = "wide")
st.title("Урок 35")


@st.cache_data
def load_csv(uploaded_file):
    return pd.read_csv(uploaded_file)


def validate_dataset(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    errors = []
    
    if df.empty:
        errors.append("Файл пустой")
    
    missing_columns = [column for column in required_columns if column not in df.columns]
    
    if missing_columns:
        errors.append("Отсутствуют обязательные колонки")
        
    return errors

    


with st.sidebar:
    st.header("Инструкция:")
    st.write("Загрузите CSV -> Выберите фильтр")

uploaded_file = st.file_uploader("Загрузите CSV файл", type= ["csv"])

if uploaded_file is None:
    st.info("Загрузите файл, для того чтобы начать анализ")
    st.stop()


try:
    df = load_csv(uploaded_file)
except Exception as exception:
    st.error(f"Ошибка чтения файла, код ошибки - {exception}")
    st.stop()

required_columns = []
validation_errors = validate_dataset(df, required_columns)
st.subheader(f"Проверка данных")

if validation_errors:
    for error in validation_errors:
        st.error(error)
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.metric("Строк", df.shape[0])
with col2:
    st.metric("Колонок", df.shape[1])

missing_values = df.isnull().sum().sort_values(ascending = False)
missing_values = missing_values[missing_values>0]

if missing_values.empty:
    st.success("Пропусков не найдено")
else:
    st.warning("Есть пропущенные значения")
    
    
st.subheader("Предпросмотр")
st.dataframe(df.head(20))

categorical_columns = df.select_dtypes(include = ["category", "object"]).columns.tolist()
numerical_columns = df.select_dtypes(include = ["number"]).columns.tolist()

if categorical_columns:
    selected_category = st.selectbox("Колонка для фильтрации данных", categorical_columns)
    category_values = sorted(df[selected_category].dropna().astype(str).unique().tolist())
    selected_value = st.selectbox("Уникальные значения этой категории",category_values)
    filtered_df = df[df[selected_category].astype(str) == selected_value].copy()
else:
    st.info("Категориальных данных не существует")
    filtered_df = df.copy()
    
st.subheader("Результат фильтра")
st.dataframe(filtered_df)
st.metric("Строк после фильтра", filtered_df.shape[0])

if numerical_columns:
    selected_numeric = st.selectbox("Колонка для графика", numerical_columns)
    selected_numerical_column = filtered_df[selected_numeric].dropna()
    if selected_numerical_column.empty:
        st.info("Нет числовых значений для графика")
    else:
        histogram = pd.cut(selected_numerical_column, bins = 40).value_counts().sort_index()
        histogram_df = histogram.reset_index()
        histogram_df.columns = ["Интервал","Количество"]
        histogram_df["Интервал"] = histogram_df["Интервал"].astype(str)
        
st.bar_chart(data = histogram_df, x = "Интервал", y = "Количество")


st.subheader("Статистика(description)")
st.dataframe(filtered_df[selected_numeric].describe().T, use_container_width = True)
