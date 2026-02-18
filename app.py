import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Gestione Tessile Pro", layout="wide", initial_sidebar_state="expanded")

# --- FUNZIONE DI LOGIN ---
def check_password():
    """Restituisce True se l'utente ha inserito la password corretta."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Visualizzazione schermata di login
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; }
        .login-box { 
            background-color: #1f2937; 
            padding: 2rem; 
            border-radius: 10px; 
            border: 1px solid #3b82f6;
            text-align: center;
        }
        </style>
    """, unsafe_allow_view_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/565/565547.png", width=100) # Icona lucchetto
        st.title("Accesso Aziendale")
        password = st.text_input("Inserisci la Password per accedere al Database", type="password")
        if st.button("Entra"):
            if password == "Prato2024": # <--- CAMBIA QUI LA TUA PASSWORD
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Password errata")
    return False

# ESECUZIONE LOGIN
if check_password():

    # --- DATI E LOGICA (Viene eseguito solo se loggato) ---
    clienti = pd.DataFrame({
        'Cliente': ['Rossi Tessuti', 'Moda Prato', 'Filati snc', 'Lanificio X'],
        'Stato': ['✅ ATTIVO', '🆘 RECUPERARE', '✅ ATTIVO', '🆘 RECUPERARE'],
        'Fatturato': [50000, 12000, 35000, 8000]
    })

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🧶 Gofgi.io")
        st.subheader("Menù Principale")
        st.button("🏠 Dashboard")
        st.button("👥 Anagrafica Clienti")
        st.button("📦 Database Prodotti")
        st.divider()
        if st.button("Esci (Logout)"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- DASHBOARD (Come la tua foto) ---
    st.title("Pannello di Controllo")
    
    # Metriche
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("FATTURATO TOTALE", "105.000 €", "+12%")
    c2.metric("CLIENTI ATTIVI", "450", "+3")
    c3.metric("ORDINI MESE", "38", "-2%")
    c4.metric("SOS RECUPERO", "10", "🆘")

    st.divider()

    # Grafico e Tabella SOS
    col_sx, col_dx = st.columns([2, 1])
    with col_sx:
        st.subheader("📊 Performance Clienti")
        fig = px.bar(clienti, x='Cliente', y='Fatturato', color='Stato', 
                     color_discrete_map={'✅ ATTIVO': '#10b981', '🆘 RECUPERARE': '#ef4444'},
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col_dx:
        st.subheader("🆘 Da Chiamare")
        st.dataframe(clienti[clienti['Stato'] == '🆘 RECUPERARE'][['Cliente']], use_container_width=True)

    # Invio WhatsApp Rapido
    st.divider()
    st.subheader("🚀 Invio Rapido Offerta")
    w1, w2, w3 = st.columns(3)
    with w1:
        sel_cliente = st.selectbox("Seleziona Cliente", clienti['Cliente'])
    with w2:
        prodotto = st.text_input("Prodotto/Tessuto", "Lana Verginel")
    with w3:
        if st.button("Invia su WhatsApp"):
            st.success("Apertura WhatsApp...")
            # Qui andrebbe il link dinamico
