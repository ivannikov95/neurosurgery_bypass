import streamlit as st
import requests
from requests.exceptions import ConnectionError

ip_api = '127.0.0.1'
port_api = '5000'

st.title('Модель прогнозирования вероятности развития несостоятельности ЭИКМА')

st.write('Введите данные ультразвукового исследования')

lsk = st.text_input('ЛСК артерии-донора', value=10)
if not lsk.isdigit():
    st.error('Пожалуйста, введите корректное число')

ok = st.text_input('ОК артерии-донора', value=100)
if not ok.isdigit():
    st.error('Пожалуйста, введите корректное число')

age = st.text_input('Возраст', value=10)
if not ok.isdigit():
    st.error('Пожалуйста, введите корректное число')

diam = st.text_input('Диаметр артерии-донора', value=10)
if not ok.isdigit():
    st.error('Пожалуйста, введите корректное число')

if st.button('Predict'):
    if lsk.isdigit() and ok.isdigit() and age.isdigit() and diam.isdigit():
        data = {
            'ЛСК_донора': float(lsk),
            'ОК_донора': float(ok),
            'Возраст': int(age),
            'Диам_донора_х_10': int(diam)
        }

        try:
            response = requests.post(
                f'http://{ip_api}:{port_api}/predict_model',
                json=data  # ← вот это ключевое
                )

            if response.status_code == 200:
                res = response.json()
                proba = res['probability']
                st.success(f'Вероятность развития несостоятельности анастомоза: {proba}%')
                st.progress(int(proba))
            else:
                st.error(f'Request failed with status code {response.status_code}')
        except ConnectionError as e:
            st.error(f'Failed to connect to the server')
    else:
        st.error('Please fill in all fields with valid numbers')