import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configurazione Pagina
st.set_page_config(page_title="Gestione Tessile Pro", layout="wide")

# --- FUNZIONE DI LOGIN SEMPLIFICATA ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.title("🔐 Accesso Aziendale")
    password = st.text_input("Inserisci la Password", type="password")
    if st.button("Entra"):
        if password == "Prato2024":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Password errata")
    return False

# 2. Esecuzione App
if check_password():
    # DATI DI PROVA
    clienti = pd.DataFrame({
        'Cliente': ['Rossi Tessuti', 'Moda Prato', 'Filati snc'],
        'Stato': ['✅ ATTIVO', '🆘 RECUPERARE', '✅ ATTIVO'],
        'Fatturato': [50000, 12000, 35000]
    })

    # SIDEBAR
    with st.sidebar:
        st.title("🧶 Gofgi.io")
        if st.button("Esci (Logout)"):
            st.session_state["password_correct"] = False
            st.rerun()

    # DASHBOARD
    st.title("📊 Pannello di Controllo")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("FATTURATO", "97.000 €", "+5%")
    c2.metric("CLIENTI", "450", "+3")
    c3.metric("ALERT SOS", "1", "🆘")

    st.divider()

    col_sx, col_dx = st.columns([2, 1])
    with col_sx:
        st.subheader("Performance Vendite")
        fig = px.bar(clienti, x='Cliente', y='Fatturato', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_dx:
        st.subheader("Azioni Rapide")
        st.write("Invia offerta via WhatsApp")
        cliente_scelto = st.selectbox("Seleziona Cliente", clienti['Cliente'])
        if st.button("Genera Messaggio"):
            st.info(f"Messaggio pronto per {cliente_scelto}!")
