import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA E STILE
st.set_page_config(page_title="Gofgi.io - Gestione Tessile", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1f2937; border-right: 1px solid #3b82f6; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    h1, h2, h3 { color: #3b82f6; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIONE DATI (Inizializzazione)
if 'clienti_df' not in st.session_state:
    st.session_state.clienti_df = pd.DataFrame([
        {'Ragione Sociale': 'Rossi Tessuti', 'P.IVA': '01234567890', 'Indirizzo': 'Via Roma 10, Prato', 'Telefono': '0574123456', 'Stato': '✅ ATTIVO'},
        {'Ragione Sociale': 'Moda Prato', 'P.IVA': '09876543210', 'Indirizzo': 'Via Pratese 5, Montemurlo', 'Telefono': '0574654321', 'Stato': '🆘 RECUPERARE'}
    ])

# 3. FUNZIONE DI LOGIN
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
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=80)
        st.title("Gofgi.io")
        menu = st.radio("MENU", ["📊 Dashboard", "👥 Anagrafica Clienti", "📦 Magazzino Prodotti"])
        st.divider()
        if st.button("🚪 Esci"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- LOGICA PAGINE ---
    
    if menu == "📊 Dashboard":
        st.title("Pannello di Controllo")
        c1, c2 = st.columns(2)
        c1.metric("TOTALI CLIENTI", len(st.session_state.clienti_df))
        c2.metric("SOS RECUPERO", len(st.session_state.clienti_df[st.session_state.clienti_df['Stato'] == '🆘 RECUPERARE']))

    elif menu == "👥 Anagrafica Clienti":
        st.title("Gestione Clienti")
        
        # --- PARTE 1: AGGIUNTA NUOVO CLIENTE ---
        with st.expander("➕ Aggiungi Nuovo Cliente"):
            with st.form("nuovo_cliente_form", clear_on_submit=True):
                rs = st.text_input("Ragione Sociale")
                piva = st.text_input("CF / P.IVA")
                col_ind1, col_ind2 = st.columns([3, 1])
                via = col_ind1.text_input("Via e N° Civico")
                comune = col_ind2.text_input("Comune")
                col_ind3, col_ind4, col_ind5 = st.columns([2, 1, 1])
                prov = col_ind3.text_input("Provincia")
                cap = col_ind4.text_input("CAP")
                tel = col_ind5.text_input("Telefono")
                
                submitted = st.form_submit_button("Salva Cliente")
                if submitted:
                    indirizzo_full = f"{via}, {comune} ({prov}), {cap}"
                    nuovo_c = {
                        'Ragione Sociale': rs, 'P.IVA': piva, 
                        'Indirizzo': indirizzo_full, 'Telefono': tel, 'Stato': '✅ ATTIVO'
                    }
                    st.session_state.clienti_df = pd.concat([st.session_state.clienti_df, pd.DataFrame([nuovo_c])], ignore_index=True)
                    st.success("Cliente aggiunto!")
                    st.rerun()

        st.divider()

        # --- PARTE 2: VISUALIZZAZIONE E MODIFICA ---
        st.subheader("Lista Clienti (Clicca per modificare)")
        for index, row in st.session_state.clienti_df.iterrows():
            with st.expander(f"🏢 {row['Ragione Sociale']} - {row['Stato']}"):
                with st.form(f"edit_form_{index}"):
                    new_rs = st.text_input("Ragione Sociale", row['Ragione Sociale'])
                    new_piva = st.text_input("P.IVA", row['P.IVA'])
                    new_ind = st.text_input("Indirizzo", row['Indirizzo'])
                    new_tel = st.text_input("Telefono", row['Telefono'])
                    new_stato = st.selectbox("Stato", ["✅ ATTIVO", "🆘 RECUPERARE"], index=0 if row['Stato'] == "✅ ATTIVO" else 1)
                    
                    if st.form_submit_button("Aggiorna Dati"):
                        st.session_state.clienti_df.at[index, 'Ragione Sociale'] = new_rs
                        st.session_state.clienti_df.at[index, 'P.IVA'] = new_piva
                        st.session_state.clienti_df.at[index, 'Indirizzo'] = new_ind
                        st.session_state.clienti_df.at[index, 'Telefono'] = new_tel
                        st.session_state.clienti_df.at[index, 'Stato'] = new_stato
                        st.success("Modifica salvata!")
                        st.rerun()

    elif menu == "📦 Magazzino Prodotti":
        st.title("Magazzino")
        st.info("Questa sezione la personalizzeremo nel prossimo passaggio.")
