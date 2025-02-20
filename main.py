import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings 
warnings.filterwarnings('ignore')

st.sidebar.title('Название')

uploaded_file = st.sidebar.file_uploader('Загрузи CSV файл', type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head(5))
else:
    st.stop()


missed_values = df.isna().sum()
missed_values = missed_values[missed_values > 0]

if len(missed_values) > 0:
    fig, ax = plt.subplots()
    sns.barplot(x=missed_values.index, y=missed_values.values)
    ax.set_title('Пропуски в столбцах')
    ax.set_ylabel('Количество пропусков')
    st.pyplot(fig)
else:
    st.write('нЕТ пропусков')
    st.stop()

if len(missed_values) != 0:
    button = st.button('Заполнить пропуски')
    if button:
        df_filled = df[missed_values.index].copy()

        for col in df_filled.columns:
            if df_filled[col].dtype == 'object':
                df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
            else:
                df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        st.write(df_filled.head(5))

        download_button = st.download_button(label='Скачать файл цсв',
                   data=df_filled.to_csv(),
                   file_name='filled_fate.csv')
