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
    </style>
    """, unsafe_allow_html=True)

# 2. INIZIALIZZAZIONE DATI (Session State per non perdere i nuovi inserimenti durante la sessione)
if 'clienti_df' not in st.session_state:
    st.session_state.clienti_df = pd.DataFrame([
        {'Ragione Sociale': 'Rossi Tessuti', 'P.IVA': '01234567890', 'Indirizzo': 'Via Roma 10, Prato', 'Telefono': '0574123456', 'Stato': '✅ ATTIVO'},
        {'Ragione Sociale': 'Moda Prato', 'P.IVA': '09876543210', 'Indirizzo': 'Via Pratese 5, Montemurlo', 'Telefono': '0574654321', 'Stato': '🆘 RECUPERARE'},
        {'Ragione Sociale': 'Filati snc', 'P.IVA': '11223344556', 'Indirizzo': 'Via Prato 20, Prato', 'Telefono': '0574998877', 'Stato': '✅ ATTIVO'},
        {'Ragione Sociale': 'Tessitura Toscana', 'P.IVA': '66554433221', 'Indirizzo': 'Via Campi 1, Campi Bisenzio', 'Telefono': '055123456', 'Stato': '🆘 RECUPERARE'}
    ])

if 'prodotti_df' not in st.session_state:
    st.session_state.prodotti_df = pd.DataFrame({
        'Articolo': ['Lana Verginel', 'Seta Lucida', 'Lino Grezzo', 'Cotone Bio'],
        'Prezzo (€/mt)': [25.50, 45.00, 18.00, 12.50],
        'Disponibilità': [1200, 450, 2100, 3000],
        'Immagine': ['🧶', '✨', '🌾', '🌱']
    })

# 3. FUNZIONE DI LOGIN
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

# 4. ESECUZIONE APP
if check_password():
    
    # --- SIDEBAR DI NAVIGAZIONE ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=80)
        st.title("Gofgi.io")
        menu = st.radio("MENU PRINCIPALE", 
                        ["📊 Dashboard", "👥 Anagrafica Clienti", "📦 Magazzino Prodotti", "📝 Crea Preventivo", "🛒 Ordini Ricevuti"])
        st.divider()
        if st.button("🚪 Esci"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- LOGICA DELLE PAGINE ---
    
    if menu == "📊 Dashboard":
        st.title("Pannello di Controllo")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("FATTURATO MESE", "105.000 €", "+12%")
        c2.metric("CLIENTI TOTALI", len(st.session_state.clienti_df), "+3")
        c3.metric("ORDINI OGGI", "12", "+2")
        c4.metric("DA RECUPERARE", len(st.session_state.clienti_df[st.session_state.clienti_df['Stato'] == '🆘 RECUPERARE']), "🆘")
        
        st.divider()
        col_graf, col_sos = st.columns([2, 1])
        with col_graf:
            st.subheader("Andamento Vendite per Cliente")
            fig = px.bar(st.session_state.clienti_df, x='Ragione Sociale', y=[10, 4, 8, 2][:len(st.session_state.clienti_df)], template="plotly_dark", color_discrete_sequence=['#3b82f6'])
            st.plotly_chart(fig, use_container_width=True)
        with col_sos:
            st.subheader("🆘 SOS Recupero")
            st.table(st.session_state.clienti_df[st.session_state.clienti_df['Stato'] == '🆘 RECUPERARE'][['Ragione Sociale', 'Telefono']])

    elif menu == "👥 Anagrafica Clienti":
        st.title("Anagrafica Clienti")
        
        # Aggiunta Nuovo Cliente
        with st.expander("➕ Aggiungi Nuovo Cliente"):
            with st.form("nuovo_cliente_form", clear_on_submit=True):
                rs = st.text_input("Ragione Sociale")
                piva = st.text_input("CF / P.IVA")
                col1, col2 = st.columns([3, 1])
                via = col1.text_input("Via e N° Civico")
                comune = col2.text_input("Comune")
                col3, col4, col5 = st.columns([2, 1, 1])
                prov = col3.text_input("Provincia")
                cap = col4.text_input("CAP")
                tel = col5.text_input("Telefono")
                if st.form_submit_button("Salva Nuovo Cliente"):
                    nuovo_c = {'Ragione Sociale': rs, 'P.IVA': piva, 'Indirizzo': f"{via}, {comune} ({prov}), {cap}", 'Telefono': tel, 'Stato': '✅ ATTIVO'}
                    st.session_state.clienti_df = pd.concat([st.session_state.clienti_df, pd.DataFrame([nuovo_c])], ignore_index=True)
                    st.success("Cliente aggiunto!")
                    st.rerun()

        st.divider()
        search = st.text_input("Cerca cliente per nome...")
        
        # Lista e Modifica Clienti
        for index, row in st.session_state.clienti_df.iterrows():
            if search.lower() in row['Ragione Sociale'].lower():
                with st.expander(f"🏢 {row['Ragione Sociale']} - {row['Stato']}"):
                    with st.form(f"edit_{index}"):
                        u_rs = st.text_input("Ragione Sociale", row['Ragione Sociale'])
                        u_tel = st.text_input("Telefono", row['Telefono'])
                        u_stato = st.selectbox("Stato", ["✅ ATTIVO", "🆘 RECUPERARE"], index=0 if row['Stato'] == "✅ ATTIVO" else 1)
                        if st.form_submit_button("Aggiorna"):
                            st.session_state.clienti_df.at[index, 'Ragione Sociale'] = u_rs
                            st.session_state.clienti_df.at[index, 'Telefono'] = u_tel
                            st.session_state.clienti_df.at[index, 'Stato'] = u_stato
                            st.rerun()

    elif menu == "📦 Magazzino Prodotti":
        st.title("Magazzino Prodotti")
        for i, row in st.session_state.prodotti_df.iterrows():
            with st.expander(f"{row['Immagine']} {row['Articolo']} - {row['Prezzo (€/mt)']}€/mt"):
                st.write(f"**Disponibilità:** {row['Disponibilità']} metri")
                st.button("Vedi scheda tecnica", key=f"prd_{i}")

    elif menu == "📝 Crea Preventivo":
        st.title("Generatore Preventivi WhatsApp")
        c1, c2 = st.columns(2)
        with c1:
            cl = st.selectbox("Seleziona Cliente", st.session_state.clienti_df['Ragione Sociale'])
            pr = st.selectbox("Seleziona Prodotto", st.session_state.prodotti_df['Articolo'])
        with c2:
            qt = st.number_input("Metri richiesti", min_value=1)
            px_u = st.session_state.prodotti_df[st.session_state.prodotti_df['Articolo'] == pr]['Prezzo (€/mt)'].values[0]
            totale = px_u * qt
            st.write(f"### Totale: {totale:.2f} €")
        
        if st.button("🚀 GENERA LINK WHATSAPP"):
            tel_c = st.session_state.clienti_df[st.session_state.clienti_df['Ragione Sociale'] == cl]['Telefono'].values[0]
            messaggio = f"Ciao {cl}, ti propongo {qt}mt di {pr}. Totale: {totale}€. Ti interessa?"
            st.link_button("Invia ora su WhatsApp", f"https://wa.me/{tel_c}?text={messaggio}")

    elif menu == "🛒 Ordini Ricevuti":
        st.title("Storico Ordini")
        st.table(pd.DataFrame({'Data': ['12/05/2024'], 'Cliente': ['Rossi Tessuti'], 'Totale': ['1.200€'], 'Stato': ['In Lavorazione']}))
