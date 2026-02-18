import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Gofgi.io - Gestione Tessile", layout="wide")

# STILE DARK PROFESSIONALE
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1f2937; border-right: 1px solid #3b82f6; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    h1, h2, h3 { color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Accesso Gofgi.io")
        password = st.text_input("Password Aziendale", type="password")
        if st.button("Entra"):
            if password == "Prato2024":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Password errata")
    return False

if check_password():
    
    # --- DATI MANUALI (PULITI) ---
    # Questi sono i dati che potremo cambiare uno ad uno
    clienti_data = pd.DataFrame({
        'Cliente': ['Rossi Tessuti', 'Moda Prato', 'Filati snc'],
        'Stato': ['✅ ATTIVO', '🆘 RECUPERARE', '✅ ATTIVO'],
        'Città': ['Prato', 'Montemurlo', 'Prato']
    })

    # --- MENU LATERALE ---
    with st.sidebar:
        st.title("Gofgi.io")
        menu = st.radio("Scegli sezione:", ["Dashboard", "Clienti", "Prodotti"])
        st.divider()
        if st.button("Esci"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- LOGICA PAGINE ---
    if menu == "Dashboard":
        st.title("📊 Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("FATTURATO", "105.000 €")
        c2.metric("CLIENTI", "450")
        c3.metric("ALERT", "1")
        
        st.divider()
        st.subheader("Grafico Vendite")
        fig = px.bar(clienti_data, x='Cliente', y=[50, 20, 35], template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Clienti":
        st.title("👥 Anagrafica Clienti")
        st.dataframe(clienti_data, use_container_width=True)

    elif menu == "Prodotti":
        st.title("📦 Magazzino")
        st.write("Sezione prodotti in fase di creazione...")
