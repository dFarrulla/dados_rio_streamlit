import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime as dt
import folium
from streamlit_folium import st_folium

import streamlit as st
import requests
from datetime import datetime
import folium
from streamlit_folium import st_folium
#########################################################################################
st.title("Vizualizações utilizando as APIs Public Holiday e Open-Meteo Historical ")
#Classificação do Tempo Atual no Rio de Janeiro com mapa
# Função para fazer requisições GET
def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=America/Sao_Paulo"
    response = requests.get(url)
    return response.json()

# Coordenadas do Rio de Janeiro
latitude = -22.9064
longitude = -43.1822

# Obtém os dados do tempo atual
weather_data = get_weather(latitude, longitude)

# Extraindo informações relevantes
temperature = weather_data['current_weather']['temperature']
weather_code = weather_data['current_weather']['weathercode']
wind_speed = weather_data['current_weather']['windspeed']
time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Tabela de códigos WMO
wmo_codes = {
    0: "☀️ Céu limpo",
    1: "🌤️ Céu limpo com poucas nuvens",
    2: "⛅ Parcialmente nublado",
    3: "☁️ Nublado",
    45: "🌫️ Névoa",
    48: "🌫️ Névoa intensa",
    51: "🌦️ Chuva leve",
    53: "🌧️ Chuva moderada",
    55: "🌧️ Chuva forte",
    61: "🌧️ Chuva leve",
    63: "🌧️ Chuva moderada",
    65: "🌧️ Chuva intensa",
    71: "❄️ Neve leve",
    73: "❄️ Neve moderada",
    75: "❄️ Neve forte",
    80: "🌧️ Aguaceiros leves",
    81: "🌧️ Aguaceiros moderados",
    82: "🌧️ Aguaceiros fortes",
}

# Função para classificar o tempo atual
def classify_weather(temp, code):
    if code in [0, 1, 2] and temp >= 25:
        return "Bom"
    elif code in [3, 45, 48] or temp < 25:
        return "Razoável"
    else:
        return "Ruim"

# Classifica o tempo atual
classification = classify_weather(temperature, weather_code)

# Cria o mapa do Rio de Janeiro
m = folium.Map(location=[latitude, longitude], zoom_start=12)
folium.Marker(
    location=[latitude, longitude],
    popup=f"Rio de Janeiro\nTemperatura: {temperature}°C\nClima: {wmo_codes.get(weather_code, 'Desconhecido')}\nVelocidade do Vento: {wind_speed} km/h",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(m)

# Exibindo os dados no Streamlit
st.title("Classificação do Tempo Atual no Rio de Janeiro")

# Exibe o mapa no Streamlit
st_folium(m, width=700)

st.write(f"**Data e Hora:** {time}")
st.write(f"**Temperatura Atual:** {temperature}°C")
st.write(f"**Condições Climáticas:** {wmo_codes.get(weather_code, 'Desconhecido')}")
st.write(f"**Velocidade do Vento:** {wind_speed} km/h")

st.write(f"### Classificação do Tempo: {classification}")


######################################################################################

######################################################################################
# Título da aplicação
st.title("Pergunta 1")
st.title("Análise de Feriados no Brasil em 2024")

# Requisição à API de feriados públicos
url = 'https://date.nager.at/api/v3/publicholidays/2024/BR'

try:
    resposta = requests.get(url)
    resposta.raise_for_status()  # Levanta uma exceção para códigos de status HTTP ruins
    feriados = resposta.json()

    if isinstance(feriados, list):
        st.write(f"Há **{len(feriados)}** feriados em 2024 no Brasil.")

        # Processar dados para análise
        feriados_por_mes = Counter()
        meses_nomes = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 
            6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 
            11: 'Novembro', 12: 'Dezembro'
        }

        for feriado in feriados:
            mes = int(feriado['date'].split('-')[1])
            feriados_por_mes[mes] += 1

        # Convertendo para um DataFrame para facilitar a visualização
        df_feriados = pd.DataFrame(list(feriados_por_mes.items()), columns=['Mês', 'Número de Feriados'])
        df_feriados['Mês'] = df_feriados['Mês'].apply(lambda x: meses_nomes[x])

        # Plotando o gráfico de barras
        st.subheader("Distribuição de Feriados por Mês em 2024")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Mês', y='Número de Feriados', data=df_feriados, palette='viridis')
        plt.xticks(rotation=45)
        plt.xlabel('Mês')
        plt.ylabel('Número de Feriados')
        plt.title('Número de Feriados por Mês em 2024')
        st.pyplot(plt)

    else:
        st.error("Formato inesperado de dados.")
except requests.exceptions.RequestException as e:
    st.error(f"Erro na requisição: {e}")

###################################################

# Título da aplicação
st.title("Pergunta 2")
st.title("Distribuição de Feriados no Brasil em 2024")

# Requisição à API de feriados públicos
url = 'https://date.nager.at/api/v3/publicholidays/2024/BR'

try:
    resposta = requests.get(url)
    resposta.raise_for_status()  # Levanta uma exceção para códigos de status HTTP ruins
    feriados = resposta.json()

    # Inicializa um contador para os meses
    feriados_por_mes = Counter()

    # Itera sobre os feriados, incrementando a contagem para o mês correspondente
    for feriado in feriados:
        mes = feriado.get('date', '')[5:7]  # Extrai o mês da data
        if mes:
            feriados_por_mes[mes] += 1
        else:
            st.warning(f"Aviso: Data inválida em '{feriado}'")

    # Converte o resultado para um DataFrame
    df_feriados = pd.DataFrame(list(feriados_por_mes.items()), columns=['Mês', 'Número de Feriados'])

    # Converte o mês de número para nome (opcional)
    meses_nomes = {
        '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril', '05': 'Maio', 
        '06': 'Junho', '07': 'Julho', '08': 'Agosto', '09': 'Setembro', '10': 'Outubro', 
        '11': 'Novembro', '12': 'Dezembro'
    }
    df_feriados['Mês'] = df_feriados['Mês'].apply(lambda x: meses_nomes.get(x, x))

    # Exibe o DataFrame no Streamlit
    st.dataframe(df_feriados)

    # Cria um gráfico de barras
    st.subheader("Número de Feriados por Mês em 2024")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Mês', y='Número de Feriados', data=df_feriados, palette='coolwarm')
    plt.xticks(rotation=45)
    plt.xlabel('Mês')
    plt.ylabel('Número de Feriados')
    plt.title('Distribuição de Feriados por Mês em 2024')
    st.pyplot(plt)

except requests.exceptions.RequestException as e:
    st.error(f"Erro na requisição: {e}")
    
###################################################################################
from datetime import datetime
# Título da aplicação
st.title("Pergunta 3")

# Pergunta
st.subheader("Quantos feriados em 2024 caem em dias de semana (segunda a sexta-feira)?")

# Função para verificar se uma data cai em um dia da semana
def verifica_dia_da_semana(data_str):
    dia_semana = datetime.strptime(data_str, "%Y-%m-%d").weekday()
    return dia_semana < 5  # 0 = segunda-feira, 4 = sexta-feira

# Requisição à API de feriados públicos
url = 'https://date.nager.at/api/v3/publicholidays/2024/BR'

try:
    resposta = requests.get(url)
    resposta.raise_for_status()  # Levanta uma exceção para códigos de status HTTP ruins
    feriados = resposta.json()

    # Calcula quantos feriados caem em dias de semana
    feriados_em_dia_de_semana = sum(1 for feriado in feriados if verifica_dia_da_semana(feriado['date']))

    # Exibe o resultado
    st.write(f"Há **{feriados_em_dia_de_semana}** feriados em dias de semana.")

    # Preparação dos dados para o gráfico
    dias_da_semana = ['Dias de Semana', 'Fins de Semana']
    contagem = [feriados_em_dia_de_semana, len(feriados) - feriados_em_dia_de_semana]

    # Criação do gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(dias_da_semana, contagem, color=['blue', 'orange'])
    plt.xlabel('Tipo de Dia')
    plt.ylabel('Número de Feriados')
    plt.title('Feriados em Dias de Semana vs Fins de Semana em 2024')

    # Exibe o gráfico no Streamlit
    st.pyplot(plt)

except requests.exceptions.RequestException as e:
    st.error(f"Erro na requisição: {e}")
###########################################################################
from collections import defaultdict  # Importa defaultdict
# Título da aplicação
st.title("Pergunta 4")

# Subtítulo
st.subheader("Qual foi a temperatura média em cada mês?")

# Coordenadas e URL da API
latitude, longitude = -22.9064, -43.1822
url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2024-01-01&end_date=2024-08-01&daily=temperature_2m_max&temperature_unit=celsius&timezone=America/Sao_Paulo"

# Faz a requisição GET à API
resposta = requests.get(url)

if resposta.ok:  # Verifica se a requisição foi bem-sucedida
    dados = resposta.json()

    # Dicionário para armazenar as temperaturas mensais
    temperaturas_mensais = defaultdict(list)

    # Itera sobre as datas e temperaturas, agrupando por mês
    for data, temp_max in zip(dados['daily']['time'], dados['daily']['temperature_2m_max']):
        mes = data[:7]  # Extrai o mês da data no formato "YYYY-MM"
        temperaturas_mensais[mes].append(temp_max)

    # Calcula a temperatura média de cada mês e armazena para visualização
    medias_mensais = {mes: sum(temps) / len(temps) for mes, temps in temperaturas_mensais.items()}

    # Exibe as temperaturas médias mensais
    st.write("Temperaturas médias mensais (em °C):")
    for mes, temp_media in medias_mensais.items():
        st.write(f"{mes}: {temp_media:.2f}°C")

    # Criando o gráfico
    meses = list(medias_mensais.keys())
    temperaturas = list(medias_mensais.values())

    plt.figure(figsize=(10, 6))
    plt.plot(meses, temperaturas, marker='o', color='blue')
    plt.xlabel('Mês')
    plt.ylabel('Temperatura Média (°C)')
    plt.title('Temperatura Média Mensal no Rio de Janeiro (2024)')
    plt.grid(True)

    # Exibe o gráfico no Streamlit
    st.pyplot(plt)

else:
    st.error(f"Erro ao acessar a API: {resposta.status_code}")
##############################################################

# Título da aplicação
st.title("Pergunta 5")

# Coordenadas do Rio de Janeiro
latitude = -22.9064
longitude = -43.1822

# URL da API Open-Meteo
url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2024-01-01&end_date=2024-08-01&daily=weathercode&timezone=America/Sao_Paulo"

# Tabela de códigos WMO
wmo_codes = {
    0: "Céu limpo",
    1: "Céu limpo com poucas nuvens",
    2: "Parcialmente nublado",
    3: "Nublado",
    4: "Nublado com chuvas leves",
    5: "Chuva moderada",
    6: "Chuva forte",
    7: "Chuva intensa com trovoadas",
    8: "Neve leve",
    9: "Neve moderada",
    10: "Neve forte",
    11: "Neblina",
    12: "Nevoeiro",
    13: "Tempestade de areia",
    14: "Tempestade de granizo",
    15: "Chuvas fortes com granizo",
    51: "Chuva leve",
    53: "Chuva moderada",
    55: "Chuva forte",
    61: "Chuva leve com trovoadas",
    63: "Chuva moderada com trovoadas",
    65: "Chuva forte com trovoadas",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    81: "Chuva leve com granizo",
    82: "Chuva moderada com granizo",
    83: "Chuva forte com granizo",
    # Adicione mais códigos conforme necessário
}

# Função para obter os dados da API e determinar o tempo predominante
def obter_tempo_predominante():
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()

        # Dicionário para armazenar os códigos de tempo por mês
        weather_codes_mensais = defaultdict(list)

        # Itera sobre as datas e códigos de tempo diários
        for i in range(len(dados['daily']['time'])):
            data = dados['daily']['time'][i]
            weather_code = dados['daily']['weathercode'][i]

            # Extrai o mês da data
            mes = dt.strptime(data, "%Y-%m-%d").strftime("%Y-%m")

            # Adiciona o código de tempo à lista correspondente ao mês
            weather_codes_mensais[mes].append(weather_code)

        # Determina o tempo predominante em cada mês
        resultados = {}
        for mes, codes in weather_codes_mensais.items():
            # Conta a frequência de cada código de tempo no mês
            frequencia = Counter(codes)
            # Encontra o código de tempo mais comum
            tempo_predominante = frequencia.most_common(1)[0][0]
            # Converte o código de tempo para a descrição correspondente
            descricao_tempo = wmo_codes.get(tempo_predominante, "Código desconhecido")
            resultados[mes] = descricao_tempo

        return resultados
    else:
        st.error(f"Erro ao acessar a API: {resposta.status_code}")
        return {}

# Configura o título do aplicativo
st.title("Análise do Tempo Predominante em cada mês no Rio de Janeiro")

# Executa a função para obter o tempo predominante
resultados = obter_tempo_predominante()

# Exibe os resultados na interface do Streamlit
if resultados:
    st.write("Tempo predominante em cada mês:")

    # Dados para o gráfico
    meses = list(resultados.keys())
    descricoes = list(resultados.values())

    # Exibe a tabela dos resultados
    for mes, descricao in resultados.items():
        st.write(f"{mes}: {descricao}")

    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(meses, descricoes, color='skyblue')
    ax.set_xlabel('Meses')
    ax.set_ylabel('Descrição do Tempo Predominante')
    ax.set_title('Tempo Predominante no Rio de Janeiro (Jan 2024 - Ago 2024)')
    ax.tick_params(axis='x', rotation=45)

    st.pyplot(fig)
else:
    st.write("Nenhum dado disponível.")
    
########################################################################
    
# Função para fazer requisições GET
def get(url):
    resposta = requests.get(url)
    return resposta

# Coordenadas do Rio de Janeiro
latitude = -22.9064
longitude = -43.1822

# URL da API Open-Meteo
weather_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2024-01-01&end_date=2024-08-01&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America/Sao_Paulo"

# URL da API de Feriados
holidays_url = "https://date.nager.at/api/v3/publicholidays/2024/BR"

# Tabela de códigos WMO
wmo_codes = {
    0: "Céu limpo",
    1: "Céu limpo com poucas nuvens",
    2: "Parcialmente nublado",
    3: "Nublado",
    4: "Nublado com chuvas leves",
    5: "Chuva moderada",
    6: "Chuva forte",
    7: "Chuva intensa com trovoadas",
    8: "Neve leve",
    9: "Neve moderada",
    10: "Neve forte",
    11: "Neblina",
    12: "Nevoeiro",
    13: "Tempestade de areia",
    14: "Tempestade de granizo",
    15: "Chuvas fortes com granizo",
    51: "Chuva leve",
    53: "Chuva moderada",
    55: "Chuva forte",
    61: "Chuva leve com trovoadas",
    63: "Chuva moderada com trovoadas",
    65: "Chuva forte com trovoadas",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    81: "Chuva leve com granizo",
    82: "Chuva moderada com granizo",
    83: "Chuva forte com granizo",
}

# Obtém os dados dos feriados
feriados_resposta = get(holidays_url)
feriados = feriados_resposta.json()

# Obtém os dados meteorológicos
weather_resposta = get(weather_url)
weather_dados = weather_resposta.json()

# Dicionário para armazenar as temperaturas e o tempo por data
dados_feriados = {}

# Preenche o dicionário com os feriados e suas datas
for feriado in feriados:
    data_feriado = feriado['date']
    dados_feriados[data_feriado] = {'temperaturas': [], 'weathercodes': []}

# Preenche o dicionário com as temperaturas e os códigos de tempo diários
for i in range(len(weather_dados['daily']['time'])):
    data = weather_dados['daily']['time'][i]
    temp_max = weather_dados['daily']['temperature_2m_max'][i]
    temp_min = weather_dados['daily']['temperature_2m_min'][i]
    weather_code = weather_dados['daily']['weathercode'][i]

    if data in dados_feriados:
        dados_feriados[data]['temperaturas'].append((temp_max + temp_min) / 2)
        dados_feriados[data]['weathercodes'].append(weather_code)

# Calcula a temperatura média e o tempo para cada feriado
feriados_resultados = []
for data_feriado, info in dados_feriados.items():
    if info['temperaturas']:
        temperatura_media = sum(info['temperaturas']) / len(info['temperaturas'])
        tempo_predominante = Counter(info['weathercodes']).most_common(1)[0][0]
        descricao_tempo = wmo_codes.get(tempo_predominante, "Código desconhecido")
        feriados_resultados.append({
            "Data": data_feriado,
            "Temperatura Média (°C)": f"{temperatura_media:.2f}",
            "Tempo Predominante": descricao_tempo
        })
    else:
        feriados_resultados.append({
            "Data": data_feriado,
            "Temperatura Média (°C)": "Dados não disponíveis",
            "Tempo Predominante": "Dados não disponíveis"
        })

# Converte os resultados para um DataFrame
df_feriados = pd.DataFrame(feriados_resultados)

# Configura o título do aplicativo
st.title("Resposta 6")
st.title("Condições Meteorológicas em Feriados")

# Exibe a tabela dos resultados
st.write("Temperatura média e tempo predominante em cada feriado entre 01/01/2024 e 01/08/2024:")
st.dataframe(df_feriados)

# Converte a coluna "Temperatura Média (°C)" para float, tratando os erros
df_feriados["Temperatura Média (°C)"] = pd.to_numeric(df_feriados["Temperatura Média (°C)"], errors='coerce')


st.pyplot(fig)

########################################################
import streamlit as st
import requests
import pandas as pd
from collections import Counter

# Função para fazer requisições GET
def get(url):
    resposta = requests.get(url)
    return resposta

# Coordenadas do Rio de Janeiro
latitude = -22.9064
longitude = -43.1822

# URL da API Open-Meteo
weather_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2024-01-01&end_date=2024-08-01&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America/Sao_Paulo"

# URL da API de Feriados
holidays_url = "https://date.nager.at/api/v3/publicholidays/2024/BR"

# Tabela de códigos WMO
wmo_codes = {
    0: "☀️ Céu limpo",
    1: "🌤️ Céu limpo com poucas nuvens",
    2: "⛅ Parcialmente nublado",
    3: "☁️ Nublado",
    4: "🌦️ Nublado com chuvas leves",
    5: "🌧️ Chuva moderada",
    6: "🌧️ Chuva forte",
    7: "⛈️ Chuva intensa com trovoadas",
}

# Obtém os dados dos feriados
feriados_resposta = get(holidays_url)
feriados = feriados_resposta.json()

# Obtém os dados meteorológicos
weather_resposta = get(weather_url)
weather_dados = weather_resposta.json()

# Dicionário para armazenar as temperaturas e o tempo por data
dados_feriados = {}

# Preenche o dicionário com os feriados e suas datas
for feriado in feriados:
    data_feriado = feriado['date']
    dados_feriados[data_feriado] = {'temperaturas': [], 'weathercodes': []}

# Preenche o dicionário com as temperaturas e os códigos de tempo diários
for i in range(len(weather_dados['daily']['time'])):
    data = weather_dados['daily']['time'][i]
    temp_max = weather_dados['daily']['temperature_2m_max'][i]
    temp_min = weather_dados['daily']['temperature_2m_min'][i]
    weather_code = weather_dados['daily']['weathercode'][i]

    if data in dados_feriados:
        dados_feriados[data]['temperaturas'].append((temp_max + temp_min) / 2)
        dados_feriados[data]['weathercodes'].append(weather_code)

# Função para identificar feriados não aproveitáveis
def non_enjoyable_holidays(holiday_weather_info):
    non_enjoyable = []
    for date, info in holiday_weather_info.items():
        if info['temperaturas']:
            temperatura_media = sum(info['temperaturas']) / len(info['temperaturas'])
            tempo_predominante = Counter(info['weathercodes']).most_common(1)[0][0]
            if temperatura_media < 20 or tempo_predominante not in [0, 1, 2, 3]:
                non_enjoyable.append({
                    "data": date,
                    "temperatura_média": temperatura_media,
                    "tempo_predominante": wmo_codes.get(tempo_predominante, "Código desconhecido")
                })
    return non_enjoyable

# Obtém os feriados não aproveitáveis
feriados_nao_aproveitaveis = non_enjoyable_holidays(dados_feriados)

# Configura o título do aplicativo no Streamlit
# Configura o título do aplicativo no Streamlit
st.title("Resposta 8")
st.title("Análise de Feriados Não Aproveitáveis em 2024")

# Verifica se há feriados não aproveitáveis
if feriados_nao_aproveitaveis:
    # Converte os resultados para um DataFrame
    df_feriados_nao_aproveitaveis = pd.DataFrame(feriados_nao_aproveitaveis)
    
    # Exibe a tabela dos feriados não aproveitáveis
    st.write("Feriados não aproveitáveis em 2024:")
    st.dataframe(df_feriados_nao_aproveitaveis)
    
    # Gráfico de barras para visualização simples
    st.write("### Visualização Gráfica")
    st.bar_chart(df_feriados_nao_aproveitaveis.set_index('data')['temperatura_média'])
    
#################################
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# Função para fazer requisições GET
def get(url):
    resposta = requests.get(url)
    return resposta.json()

# Coordenadas do Rio de Janeiro
latitude = -22.9064
longitude = -43.1822

# URL da API Open-Meteo
weather_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2024-01-01&end_date=2024-08-01&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America/Sao_Paulo"

# URL da API de Feriados
holidays_url = "https://date.nager.at/api/v3/publicholidays/2024/BR"

# Tabela de códigos WMO
wmo_codes = {
    0: "Céu limpo",
    1: "Céu limpo com poucas nuvens",
    2: "Parcialmente nublado",
    3: "Nublado",
    4: "Nublado com chuvas leves",
    5: "Chuva moderada",
    6: "Chuva forte",
    7: "Chuva intensa com trovoadas",
    8: "Neve leve",
    9: "Neve moderada",
    10: "Neve forte",
    11: "Neblina",
    12: "Nevoeiro",
    13: "Tempestade de areia",
    14: "Tempestade de granizo",
    15: "Chuvas fortes com granizo",
    51: "Chuva leve",
    53: "Chuva moderada",
    55: "Chuva forte",
    61: "Chuva leve com trovoadas",
    63: "Chuva moderada com trovoadas",
    65: "Chuva forte com trovoadas",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    81: "Chuva leve com granizo",
    82: "Chuva moderada com granizo",
    83: "Chuva forte com granizo",
}

# Obtém os dados dos feriados
feriados = get(holidays_url)

# Obtém os dados meteorológicos
weather_dados = get(weather_url)

# Dicionário para armazenar as temperaturas e o tempo por data
dados_feriados = {}

# Preenche o dicionário com os feriados e suas datas
for feriado in feriados:
    data_feriado = feriado['date']
    dados_feriados[data_feriado] = {'temperaturas': [], 'weathercodes': []}

# Preenche o dicionário com as temperaturas e os códigos de tempo diários
for i in range(len(weather_dados['daily']['time'])):
    data = weather_dados['daily']['time'][i]
    temp_max = weather_dados['daily']['temperature_2m_max'][i]
    temp_min = weather_dados['daily']['temperature_2m_min'][i]
    weather_code = weather_dados['daily']['weathercode'][i]

    if data in dados_feriados:
        dados_feriados[data]['temperaturas'].append((temp_max + temp_min) / 2)
        dados_feriados[data]['weathercodes'].append(weather_code)

# Função para identificar o feriado mais aproveitável
def best_holiday(holiday_weather_info):
    melhor_feriado = None
    melhor_criterio = -float('inf')  # Critério para maximizar

    for date, info in holiday_weather_info.items():
        if info['temperaturas']:
            temperatura_media = sum(info['temperaturas']) / len(info['temperaturas'])
            tempo_predominante = Counter(info['weathercodes']).most_common(1)[0][0]

            # Critério para avaliar o feriado
            if temperatura_media >= 20 and tempo_predominante in [0, 1, 2, 3]:
                criterio = temperatura_media  # Aqui, usamos a temperatura como critério principal

                if criterio > melhor_criterio:
                    melhor_criterio = criterio
                    melhor_feriado = {
                        "data": date,
                        "temperatura_média": temperatura_media,
                        "tempo_predominante": wmo_codes.get(tempo_predominante, "Código desconhecido")
                    }

    return melhor_feriado

# Obtém o feriado mais aproveitável
feriado_mais_aproveitavel = best_holiday(dados_feriados)

# Visualização com Streamlit
st.title("Análise dos Feriados e Previsão do Tempo em 2024")

# Converte os dados para um DataFrame
data = {
    'Data': [],
    'Temperatura Média (°C)': [],
    'Tempo Predominante': []
}

for date, info in dados_feriados.items():
    if info['temperaturas']:
        temperatura_media = sum(info['temperaturas']) / len(info['temperaturas'])
        tempo_predominante = Counter(info['weathercodes']).most_common(1)[0][0]
        data['Data'].append(date)
        data['Temperatura Média (°C)'].append(temperatura_media)
        data['Tempo Predominante'].append(wmo_codes.get(tempo_predominante, "Código desconhecido"))

df_dados = pd.DataFrame(data)

# Exibe a tabela dos feriados
st.write("### Dados dos Feriados com Temperatura Média e Tempo Predominante")
st.dataframe(df_dados)

# Gráfico de Temperatura Média
st.write("### Gráfico de Temperatura Média dos Feriados")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_dados['Data'], df_dados['Temperatura Média (°C)'], marker='o', linestyle='-', color='b')
ax.set_xlabel('Data')
ax.set_ylabel('Temperatura Média (°C)')
ax.set_title('Temperatura Média dos Feriados em 2024')
plt.xticks(rotation=45)
st.pyplot(fig)

# Gráfico de Distribuição dos Códigos de Tempo
st.write("### Distribuição dos Códigos de Tempo")
tempo_predominante_counts = df_dados['Tempo Predominante'].value_counts()
fig, ax = plt.subplots(figsize=(12, 6))
tempo_predominante_counts.plot(kind='bar', ax=ax, color='c')
ax.set_xlabel('Tempo Predominante')
ax.set_ylabel('Número de Feriados')
ax.set_title('Distribuição dos Códigos de Tempo para os Feriados em 2024')
st.pyplot(fig)

# Exibe o feriado mais aproveitável
if feriado_mais_aproveitavel:
    st.write("### Feriado Mais Aproveitável")
    st.write(f"**Data:** {feriado_mais_aproveitavel['data']}")
    st.write(f"**Temperatura Média:** {feriado_mais_aproveitavel['temperatura_média']:.2f}°C")
    st.write(f"**Tempo Predominante:** {feriado_mais_aproveitavel['tempo_predominante']}")
else:
    st.write("Não houve feriado aproveitável em 2024.")

    
   
    
    