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
    .stDataFrame { background-color: #1f2937; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNZIONE DI LOGIN
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Accesso Gofgi.io")
        password = st.text_input("Inserisci la Password Aziendale", type="password")
        if st.button("Entra"):
            if password == "Prato2024":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Password errata")
    return False

# 3. CARICAMENTO DATI DAL TUO GOOGLE SHEET
@st.cache_data(ttl=60) # Aggiorna i dati ogni 60 secondi
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULq1AyqK-pIhgesMkDbbf1yO1rysqtdo5_SS7hrrzn4Qf0gvEgD8LoT98Urw4QIaCIwX4yDz-US0_/pub?output=csv"
    df = pd.read_csv(url)
    return df

# 4. ESECUZIONE APP
if check_password():
    
    # Carichiamo i dati reali dal link che mi hai dato
    try:
        data_all = load_data()
        
        # --- SIDEBAR DI NAVIGAZIONE ---
        with st.sidebar:
            st.title("Gofgi.io")
            menu = st.radio("MENU PRINCIPALE", 
                            ["📊 Dashboard", "👥 Anagrafica Clienti", "📦 Magazzino Prodotti", "📝 Crea Preventivo"])
            st.divider()
            if st.button("🔄 Aggiorna Dati"):
                st.cache_data.clear()
                st.rerun()
            if st.button("🚪 Esci"):
                st.session_state["password_correct"] = False
                st.rerun()

        # --- LOGICA DELLE PAGINE ---

        if menu == "📊 Dashboard":
            st.title("Pannello di Controllo")
            # Metriche basate sui tuoi dati (es. conteggio righe o somme se ci sono colonne numeriche)
            c1, c2, c3 = st.columns(3)
            c1.metric("TOTALE VOCI NEL FOGLIO", len(data_all))
            c2.metric("STATO SISTEMA", "Online")
            c3.metric("DATABASE", "Collegato ✅")
            
            st.divider()
            st.subheader("Anteprima Dati dal Google Sheet")
            st.dataframe(data_all.head(10), use_container_width=True)

        elif menu == "👥 Anagrafica Clienti":
            st.title("Ricerca nel Database")
            # Creiamo una barra di ricerca universale sui tuoi dati
            search = st.text_input("Cerca qualsiasi valore (Nome, Prodotto, Località)...")
            if search:
                # Filtra il database per qualsiasi colonna che contiene il testo cercato
                mask = data_all.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
                filtered_df = data_all[mask]
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.dataframe(data_all, use_container_width=True)

        elif menu == "📦 Magazzino Prodotti":
            st.title("Visualizzazione Catalogo")
            st.write("Ecco i dati estratti dal tuo foglio:")
            st.table(data_all)

        elif menu == "📝 Crea Preventivo":
            st.title("Generatore Messaggio WhatsApp")
            st.write("Seleziona una riga dal tuo database per inviare i dettagli:")
            
            # Selezione riga
            selected_row = st.selectbox("Scegli la voce dal database", data_all.index)
            row_data = data_all.iloc[selected_row]
            
            st.write("### Dettagli selezionati:")
            st.json(row_data.to_dict())
            
            numero_tel = st.text_input("Numero WhatsApp del cliente (es. 39333...)", "39")
            
            if st.button("🚀 GENERA LINK WHATSAPP"):
                # Crea un messaggio automatico con i dati della riga selezionata
                testo_messaggio = "Ciao! Ecco i dettagli richiesti: " + str(row_data.to_dict())
                st.link_button("Invia ora", f"https://wa.me/{numero_tel}?text={testo_messaggio}")

    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {e}")
        st.info("Assicurati che il link di pubblicazione del Google Sheet sia corretto e impostato su CSV.")
