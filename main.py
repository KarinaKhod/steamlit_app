import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import yfinance as yf
import warnings 
warnings.filterwarnings('ignore')

# Функция для загрузки данных 
def get_apple_data(period="1y"):
    apple = yf.Ticker("AAPL")
    data = apple.history(period=period)
    return data

def save_plot_as_image(data, file_name="apple_stock_chart.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index, data['Close'], label='Закрытие')
    ax.set_title("График изменения цен акций Apple")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Цена (USD)")
    ax.legend()
    plt.savefig(file_name)
    plt.close()

# Настройка страницы
st.set_page_config(page_title="Котировки Apple", layout="wide")
st.title("Котировки компании Apple")

# Бок
st.sidebar.title("Настройки")
st.sidebar.markdown("""В этой панели можно выбрать период для отображения данных или загрузить свой файл.""")
period = st.sidebar.selectbox("Выберите период:", ["1d", "5d", "1mo", "3mo", "1y", "5y", "max"])

# Загрузка CSV
uploaded_file = st.sidebar.file_uploader("Загрузить CSV файл с котировками", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data['Date'] = pd.to_datetime(data['Date'])  # Преобразуем столбец с датой в формат datetime
    data.set_index('Date', inplace=True)
    st.subheader("Загруженные данные:")
    st.write(data.head(10))
    
    file_name = "apple_stock_chart.png"
    save_plot_as_image(data, file_name)
    st.download_button(
        label="Скачать график",
        data=open(file_name, "rb").read(),
        file_name=file_name,
        mime="image/png"
    )
else:
    # Если файл не загружен, загружаем данные о котировках Apple
    data = get_apple_data(period)
    st.sidebar.subheader(f"Данные за период: {period}")
    st.subheader("Исторические данные о котировках:")
    st.write(data.head(10))

    # График
    st.subheader("График изменения цен акций Apple:")
    st.line_chart(data['Close'])
    file_name = "apple_stock_chart.png"
    save_plot_as_image(data, file_name)
    st.download_button(
        label="Скачать график",
        data=open(file_name, "rb").read(),
        file_name=file_name,
        mime="image/png"
    )