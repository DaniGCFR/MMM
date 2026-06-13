import streamlit as st
import pandas as pd

st.set_page_config(page_title="Climogrames Web", page_icon="🌤️", layout="centered")

st.title("🌤️ Consulta de Dades per Climogrames")
st.write("Selecciona una estació, un mes i un dia per veure els registres històrics.")

# --- CONFIGURACIÓ DE L'ENLLAÇ ---
ID_DEL_MEU_SHEETS = "1IebNZOb6QoGsjTtv5rxkOCrxj_Tl-6dw"
URL_EXCEL = f"https://docs.google.com/spreadsheets/d/{ID_DEL_MEU_SHEETS}/export?format=xlsx"

# --- INTERFICIE WEB ---
# Posa aquí els noms exactes de les teves pestanyes
estacions_disponibles = ["Sa_Pobla"] 
estacio = st.selectbox("1. Tria l'estació:", estacions_disponibles)

# Diccionari per mostrar els mesos en text però filtrar per número
mesos_noms = {
    1: "Gener", 2: "Febrer", 3: "Març", 4: "Abril", 5: "Maig", 6: "Juny",
    7: "Juliol", 8: "Agost", 9: "Setembre", 10: "Octubre", 11: "Novembre", 12: "Desembre"
}

# Creem dues columnes per als desplegables de Mes i Dia
col_mes, col_dia = st.columns(2)

with col_mes:
    mes_triat = st.selectbox("2. Selecciona el Mes:", list(mesos_noms.keys()), format_func=lambda x: mesos_noms[x])

with col_dia:
    dia_triat = st.selectbox("3. Selecciona el Dia:", list(range(1, 32)))

# --- CÀRREGA I FILTRAT DE DADES ---
@st.cache_data
def carregar_i_processar_dades(nom_pestanya):
    dades = pd.read_excel(URL_EXCEL, sheet_name=nom_pestanya)
    
    # Convertim la columna 'Data' a format data de Python
    dades['Data_Neta'] = pd.to_datetime(dades['Data'])
    
    # Extraiem el mes i el dia en columnes noves amagades per poder filtrar fàcilment
    dades['Mes_Num'] = dades['Data_Neta'].dt.month
    dades['Dia_Num'] = dades['Data_Neta'].dt.day
    return dades

try:
    df = carregar_i_processar_dades(estacio)
    
    # Filtrem l'Excel: busquem les files on coincideixin el Mes i el Dia triats
    fila_filtrada = df[(df['Mes_Num'] == mes_triat) & (df['Dia_Num'] == dia_triat)]
    
    if not fila_filtrada.empty:
        st.success(f"Dades trobades per al dia {dia_triat} de {mesos_noms[mes_triat]}:")
        
        # Si tens dades de diversos anys per a aquest mateix dia, es mostraran totes en una taula
        # Ideal per veure l'evolució del mateix dia en diferents anys!
        
        # Netegem la taula abans de mostrar-la perquè no es vegin les columnes quimiques que hem creat
        taula_neta = fila_filtrada.drop(columns=['Data_Neta', 'Mes_Num', 'Dia_Num'])
        st.dataframe(taula_neta)
        
    else:
        st.warning(f"No s'han trobat dades per al {dia_triat} de {mesos_noms[mes_triat]}. (Revisa si el mes té 31 dies).")

except Exception as e:
    st.error("Hi ha hagut un error en carregar les dades.")
    st.info(f"Detall de l'error: {e}")
