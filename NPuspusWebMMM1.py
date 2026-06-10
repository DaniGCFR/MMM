import streamlit as st
import pandas as pd

st.set_page_config(page_title="MMM", page_icon="🌤️", layout="centered")

st.title("🌤️ Consulta d'Estacions Meteorològiques")
st.write("Selecciona una estació i una data per consultar els registres.")

ENLLAÇ_ORIGINAL = "https://docs.google.com/spreadsheets/d/1IebNZOb6QoGsjTtv5rxkOCrxj_Tl-6dw/edit?usp=sharing&ouid=103282406717109577819&rtpof=true&sd=true"

ID_FITXER = ENLLAÇ_ORIGINAL.split("/d/")[1].split("/")[0]
URL_EXCEL = f"https://docs.google.com/spreadsheets/d/1IebNZOb6QoGsjTtv5rxkOCrxj_Tl-6dw/edit?usp=sharing&ouid=103282406717109577819&rtpof=true&sd=true"

estacions_disponibles = ["Sa_Pobla", "Lluc"] 

estacio = st.selectbox("1. Tria l'estació meteorològica:", estacions_disponibles)

@st.cache_data 
def carregar_dades(nom_pestanya):
    dades = pd.read_excel(URL_EXCEL, sheet_name=nom_pestanya)
    dades['Data'] = pd.to_datetime(dades['Data']).dt.date
    return dades

try:
    df = carregar_dades(estacio)
    
    data_triada = st.date_input("2. Selecciona la data a consultar:")
    
    fila_filtrada = df[df['Data'] == data_triada]
    
    if not fila_filtrada.empty:
        st.success(f"Dades trobades per al dia {data_triada}:")
        
        mitjana = fila_filtrada['Mitjana'].values[0]
        minima = fila_filtrada['Mínima'].values[0]
        maxima = fila_filtrada['Màxima'].values[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Temp. Mitjana", value=f"{mitjana} ºC")
        col2.metric(label="Temp. Mínima", value=f"{minima} ºC", delta_color="inverse")
        col3.metric(label="Temp. Màxima", value=f"{maxima} ºC")
        
        st.dataframe(fila_filtrada)
        
    else:
        st.warning("No s'han trobat dades per a la data seleccionada en aquesta estació.")

except Exception as e:
    st.error("Hi ha hagut un error en carregar les dades. Revisa que els noms de les columnes i pestanyes coincideixin.")
    st.info(f"Detall de l'error: {e}")