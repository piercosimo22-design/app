import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA E STILE
st.set_page_config(page_title="Gofgi.io - Gestione Tessile", layout="wide")

# CSS per rendere l'app Dark e professionale come la tua foto
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1f2937; border-right: 1px solid #3b82f6; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    h1, h2, h3 { color: #3b82f6; }
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

# 3. ESECUZIONE APP (Solo se loggato)
if check_password():
    
    # --- DATABASE TEMPORANEO (Lo collegheremo a Excel dopo) ---
    clienti_df = pd.DataFrame({
        'Cliente': ['Rossi Tessuti', 'Moda Prato', 'Filati snc', 'Tessitura Toscana'],
        'Stato': ['✅ ATTIVO', '🆘 RECUPERARE', '✅ ATTIVO', '🆘 RECUPERARE'],
        'Località': ['Prato', 'Montemurlo', 'Prato', 'Campi Bisenzio'],
        'Ultimo Ordine': ['2024-05-10', '2023-11-20', '2024-05-12', '2024-01-15']
    })

    prodotti_df = pd.DataFrame({
        'Articolo': ['Lana Verginel', 'Seta Lucida', 'Lino Grezzo', 'Cotone Bio'],
        'Prezzo (€/mt)': [25.50, 45.00, 18.00, 12.50],
        'Disponibilità': [1200, 450, 2100, 3000],
        'Immagine': ['🧶', '✨', '🌾', '🌱']
    })

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
        c2.metric("CLIENTI ATTIVI", "450", "+3")
        c3.metric("ORDINI OGGI", "12", "+2")
        c4.metric("DA RECUPERARE", "2", "🆘")
        
        st.divider()
        col_graf, col_sos = st.columns([2, 1])
        with col_graf:
            st.subheader("Andamento Vendite per Cliente")
            fig = px.bar(clienti_df, x='Cliente', y=[10, 4, 8, 2], template="plotly_dark", color_discrete_sequence=['#3b82f6'])
            st.plotly_chart(fig, use_container_width=True)
        with col_sos:
            st.subheader("🆘 SOS Recupero")
            st.table(clienti_df[clienti_df['Stato'] == '🆘 RECUPERARE'][['Cliente', 'Ultimo Ordine']])

    elif menu == "👥 Anagrafica Clienti":
        st.title("Anagrafica Clienti")
        search = st.text_input("Cerca cliente per nome...")
        filtered_df = clienti_df[clienti_df['Cliente'].str.contains(search, case=False)]
        st.dataframe(filtered_df, use_container_width=True)

    elif menu == "📦 Magazzino Prodotti":
        st.title("Magazzino Prodotti")
        for i, row in prodotti_df.iterrows():
            with st.expander(f"{row['Immagine']} {row['Articolo']} - {row['Prezzo (€/mt)']}€/mt"):
                st.write(f"**Disponibilità:** {row['Disponibilità']} metri")
                st.write(f"**Codice Interno:** PRD-00{i}")
                st.button("Vedi scheda tecnica", key=f"btn_{i}")

    elif menu == "📝 Crea Preventivo":
        st.title("Generatore Preventivi WhatsApp")
        c1, c2 = st.columns(2)
        with c1:
            cl = st.selectbox("Seleziona Cliente", clienti_df['Cliente'])
            pr = st.selectbox("Seleziona Prodotto", prodotti_df['Articolo'])
        with c2:
            qt = st.number_input("Metri richiesti", min_value=1)
            prezzo_finale = prodotti_df[prodotti_df['Articolo'] == pr]['Prezzo (€/mt)'].values[0] * qt
            st.write(f"### Totale: {prezzo_finale:.2f} €")
        
        if st.button("🚀 GENERA LINK WHATSAPP"):
            messaggio = f"Ciao {cl}, ti propongo {qt}mt di {pr}. Totale: {prezzo_finale}€. Ti interessa?"
            st.success("Link pronto!")
            st.link_button("Invia ora al cliente", f"https://wa.me/393330000000?text={messaggio}")

    elif menu == "🛒 Ordini Ricevuti":
        st.title("Storico Ordini")
        st.info("Qui verranno visualizzati gli ordini confermati dai clienti.")
        # Esempio tabella ordini
        st.table(pd.DataFrame({'Data': ['12/05/2024'], 'Cliente': ['Rossi Tessuti'], 'Totale': ['1.200€'], 'Stato': ['In Lavorazione']}))
