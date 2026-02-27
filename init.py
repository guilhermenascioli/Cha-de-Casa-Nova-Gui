import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SENHA_TABELA = "195967"
SHEET_NAME = "Confirmacoes_Cha_Casa_Nova"

# ================= CONEXÃO GOOGLE SHEETS =================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

def carregar_dados():
    dados = sheet.get_all_records()
    return pd.DataFrame(dados)

def salvar_dados(nome, acompanhantes, presenca, presente):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    sheet.append_row([nome, acompanhantes, presenca, presente, agora])

# ================= LISTA DE PRESENTES =================

presentes = [
    {"nome": "Air Fryer", "link": "https://www.amazon.com.br/"},
    {"nome": "Jogo de Panelas", "link": "https://www.amazon.com.br/"},
    {"nome": "Liquidificador", "link": "https://www.amazon.com.br/"},
    {"nome": "Kit Toalhas", "link": "https://www.amazon.com.br/"},
    {"nome": "Cafeteira", "link": "https://www.amazon.com.br/"},
]

# ================= CONTROLE DE PÁGINA =================

if "page" not in st.session_state:
    st.session_state.page = "inicio"

if "presenca" not in st.session_state:
    st.session_state.presenca = None

if "nome" not in st.session_state:
    st.session_state.nome = ""

if "acompanhantes" not in st.session_state:
    st.session_state.acompanhantes = ""

# ================= PÁGINA INICIAL =================

if st.session_state.page == "inicio":

    st.title("Feijoada de Chá de Casa Nova 🎉")

    nome = st.text_input("Seu nome")
    acompanhantes = st.text_input("Acompanhantes (opcional)")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Confirmar presença e ver lista de presentes"):
            if nome.strip() != "":
                st.session_state.nome = nome
                st.session_state.acompanhantes = acompanhantes
                st.session_state.presenca = "Vai"
                st.session_state.page = "presentes"
                st.rerun()

    with col2:
        if st.button("Não conseguirei ir mas quero presentear"):
            if nome.strip() != "":
                st.session_state.nome = nome
                st.session_state.acompanhantes = acompanhantes
                st.session_state.presenca = "Não vai"
                st.session_state.page = "presentes"
                st.rerun()

    with col3:
        if st.button("Não poderei ir"):
            if nome.strip() != "":
                salvar_dados(nome, acompanhantes, "Não vai (sem presente)", "")
                st.success("Obrigado por avisar ❤️")

    st.divider()

    st.subheader("🔐 Ver lista de confirmados")

    senha = st.text_input("Digite a senha", type="password")

    if st.button("Ver confirmados"):
        if senha == SENHA_TABELA:
            df = carregar_dados()
            if not df.empty:
                st.dataframe(df)
            else:
                st.info("Ainda não há confirmações.")
        else:
            st.error("Senha incorreta.")

# ================= PÁGINA DE PRESENTES =================

elif st.session_state.page == "presentes":

    st.title("Escolha seu presente 🎁")

    df = carregar_dados()

    for presente in presentes:

        reservado = False
        if not df.empty:
            reservado = df["Presente Reservado"].astype(str).str.contains(
                presente["nome"], na=False
            ).any()

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**{presente['nome']}**")
            st.markdown(f"[Ver produto]({presente['link']})")

        with col2:
            if reservado:
                st.button("Reservado", disabled=True)
            else:
                if st.button(f"Reservar {presente['nome']}"):
                    salvar_dados(
                        st.session_state.nome,
                        st.session_state.acompanhantes,
                        st.session_state.presenca,
                        presente["nome"]
                    )
                    st.success("Presente reservado com sucesso! 🎉")
                    st.session_state.page = "inicio"
                    st.rerun()

    st.divider()

    if st.button("Voltar"):
        st.session_state.page = "inicio"
        st.rerun()
