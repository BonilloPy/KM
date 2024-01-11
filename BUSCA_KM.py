import streamlit as st
import pandas as pd
import requests
import base64
from io import BytesIO

# Função para calcular a distância entre origem e destino
def calcular_distancia(origem, destino, api_key):
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origem,
        "destination": destino,
        "key": api_key,
        "mode": "driving",
        "alternatives": "true",
        "route": "10"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        values = []

        for route in data.get('routes', []):
            for leg in route.get('legs', []):
                value = leg.get('distance', {}).get('value')
                if value is not None:
                    values.append(value)

        menor_distancia = min(values) if values else None

        return menor_distancia / 1000

    except requests.exceptions.RequestException as e:
        st.error(f"Erro na chamada da API: {e}")
        return None

# Função para fazer o download do arquivo
def download_file(data, filename):
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    b64 = base64.b64encode(excel_data.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Clique aqui para fazer o download da planilha</a>'
    return href

# Configuração da interface Streamlit
st.title("CÁLCULO DE DISTÂNCIAS - (Busca da menor Rota usando a API Directions) ")
file = st.file_uploader("Faça o upload de uma planilha Excel", type=["xlsx"])

api_key = st.text_input("Coloque sua chave de API aqui")

if st.button("Calcular Distâncias") and file is not None:
    with st.spinner("Calculando distâncias... Aguarde!"):
        distancias = []

        planilha = pd.read_excel(file)

        for index, row in planilha.iterrows():
            origem = row['ORIGEM']
            destino = row['DESTINO']

            distancia = calcular_distancia(origem, destino, api_key)

            if distancia is not None:
                distancias.append(distancia)
            else:
                distancias.append(None)

        planilha['DISTANCIA'] = distancias

        st.success("Cálculo de distâncias concluído!")

        #st.write("Aguarde enquanto geramos o link de download...")
        href = download_file(planilha, 'planilha_com_distancia')
        st.markdown(href, unsafe_allow_html=True)
        

#st.text("Fim!")
