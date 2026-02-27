import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ================= CONFIG =================

SENHA_LISTA = "195967"
SHEET_NAME = "Confirmacoes_Cha_Casa_Nova"

st.set_page_config(page_title="Chá de Casa Nova", layout="centered")

# ================= VISUAL PREMIUM =================

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.stTextInput>div>div>input {
    background-color: #262730;
    color: white;
}

.stNumberInput>div>div>input {
    background-color: #262730;
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    font-weight: 600;
    font-size: 16px;
    background-color: #000000;
    color: white;
    border: none;
}

.stButton>button:hover {
    background-color: #333333;
    color: white;
}

/* BOTÃO CONFIRMAR RESERVA */
button[kind="secondary"] {
    background-color: #16a34a !important;
    color: white !important;
}

/* BOTÃO NÃO VOU */
button[kind="primary"] {
    background-color: #dc2626 !important;
    color: white !important;
}

.presente-card {
    padding: 18px;
    border-radius: 16px;
    background-color: #1c1f26;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================= CONEXÃO GOOGLE SHEETS =================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(credentials)
sheet = client.open(SHEET_NAME).sheet1

# ================= LISTA COMPLETA =================

gifts = [
    ("💰 Pix", None, None),
    ("Cooktop de Indução 2 Bocas", 489.90, "https://www.mercadolivre.com.br/cooktop-de-induco-2-bocas-preto-com-trava-de-seguranca-painel-touch-screen/p/MLB41647393"),
    ("Air Fryer", 404.00, "https://www.mercadolivre.com.br/fritadeira-e-forno-style-oven-fry-10-litros-elgin-3-em1-cor-preto/p/MLB51323242"),
    # restante mantido igual...
]

# ================= CONTROLE =================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "presente_selecionado" not in st.session_state:
    st.session_state.presente_selecionado = None

# ================= HOME =================

if st.session_state.page == "home":

    st.title("Feijoada de Chá de Casa Nova 🎉")

    st.markdown("""
É com muita alegria que convido você para celebrar essa nova fase da minha vida.
Sua presença será muito especial!
    """)

    nome = st.text_input("Seu nome")

    acompanhantes = st.number_input(
        "Quantidade de acompanhantes",
        min_value=0,
        max_value=10,
        step=1
    )

    st.session_state.nome = nome
    st.session_state.acompanhante = acompanhantes

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Confirmar presença"):
            st.session_state.presenca = "Vai"
            st.session_state.page = "gifts"
            st.rerun()

    with col2:
        if st.button("🎁 Não vou mas quero presentear"):
            st.session_state.presenca = "Não vai"
            st.session_state.page = "gifts"
            st.rerun()

    with col3:
        if st.button("❌ Não poderei ir", type="primary"):

            sheet.append_row([
                nome,
                acompanhantes,
                "Não vai",
                "Não irá",
                datetime.now().strftime("%d/%m/%Y %H:%M")
            ])

            st.success("Obrigado por avisar 💛")

    st.divider()

    st.subheader("Ver lista de confirmados")
    senha = st.text_input("Senha", type="password")

    if senha == SENHA_LISTA:
        dados = sheet.get_all_records()
        df = pd.DataFrame(dados)
        st.dataframe(df)

# ================= GIFTS =================

elif st.session_state.page == "gifts":

    st.title("Escolha um presente 🎁")

    dados = sheet.get_all_records()
    df = pd.DataFrame(dados)

    presentes_reservados = []
    if not df.empty and "Presente Reservado" in df.columns:
        presentes_reservados = df["Presente Reservado"].tolist()

    for nome, valor, link in gifts:

        reservado = nome in presentes_reservados

        st.markdown('<div class="presente-card">', unsafe_allow_html=True)

        if valor:
            st.markdown(f"### {nome}")
            st.markdown(f"💲 R$ {valor:.2f}")
            st.markdown(f"[Ver produto]({link})")
        else:
            st.markdown(f"### {nome}")
            st.markdown("Escolha qualquer valor 💛")

        if reservado:
            st.error("❌ Já reservado")
        else:
            if st.session_state.presente_selecionado == nome:

                st.warning("⚠️ Clique abaixo para confirmar a reserva")

                if st.button(f"🎉 Confirmar reserva de {nome}", key=f"confirmar_{nome}", type="secondary"):

                    dados_atualizados = sheet.get_all_records()
                    df_check = pd.DataFrame(dados_atualizados)

                    if not df_check.empty and nome in df_check.get("Presente Reservado", []).values:
                        st.error("Esse presente acabou de ser reservado por outra pessoa 😢")
                    else:
                        sheet.append_row([
                            st.session_state.nome,
                            st.session_state.acompanhante,
                            st.session_state.presenca,
                            nome,
                            datetime.now().strftime("%d/%m/%Y %H:%M")
                        ])

                        st.session_state.presente_selecionado = None
                        st.session_state.page = "thanks"
                        st.rerun()

            else:
                if st.button(f"🎁 Reservar {nome}", key=nome):
                    st.session_state.presente_selecionado = nome
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ================= THANKS =================

elif st.session_state.page == "thanks":

    st.title("Muito obrigado mesmo! 🚀")
    st.markdown("""
Valeu demais por confirmar a presença e fazer parte dessa nova etapa da minha vida!
Fico muito feliz de te receber e comemorar junto.
Tô contando os dias! 🫂
    """)

    st.subheader("Endereço para entrega (se for presente físico)")
    st.markdown("""
**Estrada do Campo Limpo, 143 – Vila Prel**  
São Paulo – SP – 05777-001  
Apto 105 Fun
    """)

    st.markdown("[Falar comigo no WhatsApp →](https://w.app/4qrasc)")
    st.balloons()

    if st.button("🔙 Voltar ao início"):
        st.session_state.page = "home"
        st.rerun()
