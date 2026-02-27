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
    background-color: #f8f6f3;
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

.block-container {
    padding-top: 2rem;
}

.presente-card {
    padding: 18px;
    border-radius: 16px;
    background-color: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
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
    ("Cama Box - Baú", 399.00, "https://www.mercadolivre.com.br/cama-box-bau-casal-44x138x188cm-couro-branco/p/MLB26186586"),
    ("Jogo de Cama", 287.90, "https://www.zelo.com.br/jogo-de-cama-zelo-hotel-casal-percal-400-fios-liso-p1000244"),
    ("Jogo De panelas", 251.99, "https://www.casasbahia.com.br/jogo-de-panela-de-inducao-7-pecas"),
    ("Jogo Toalha", 199.00, "https://www.casadatoalha.com.br/products/jogo-de-toalha-essence-5-pecas-cor-off-grafite"),
    ("Colcha Casal", 191.90, "https://www.zelo.com.br/colcha-chamonix-casal-com-2-porta-travesseiros"),
    ("Panela de Pressão", 189.91, "https://m.magazineluiza.com.br/panela-de-pressao-brinox-42l-bege-vanilla"),
    ("Jogo Travessa", 179.00, "https://www.westwing.com.br/jogo-de-travessa-maniglia-verde-328953.html"),
    ("Kit Churrasco", 132.99, "https://www.amazon.com.br/Pe%C3%A7as-Churrasco-Incluindo-Afiador"),
    ("Liquidificador", 113.05, "https://www.casasbahia.com.br/liquidificador-philco-ph900-preto"),
    ("Jogo de Lençol Cinza", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal"),
    ("Jogo de Lençol Linho", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal"),
    ("Panela de Arroz", 107.91, "https://www.magazineluiza.com.br/panela-de-arroz-britania"),
    ("Potes Organizadores", 99.90, "https://www.mercadolivre.com.br/kit-9-potes-hermeticos"),
    ("Jogo de Taça", 99.90, "https://www.amazon.com.br/Cristal-Premium-Elegante"),
    ("Sanduicheira", 99.00, "https://www.casasbahia.com.br/sanduicheira-grill-philco-pgr25a"),
    ("Escorredor de Louça", 83.35, "https://www.amazon.com.br/Escorredor-Loucas-Flat-Coza"),
    ("Cobertor", 82.10, "https://shopee.com.br/product/1572699366"),
    ("Mixer", 69.90, "https://www.amazon.com.br/Mixer-Brit%C3%A2nia-BMX350P"),
    ("Kit 3 Escorredor de Macarrão", 59.90, "https://www.amazon.com.br/Escorredor-Macarr%C3%A3o-Alimentos"),
    ("Kit Pote Tempero", 56.99, "https://www.amazon.com.br/Kit-Herm%C3%A9ticos-200ml"),
    ("Nicho de Parede Sobrepor", 54.00, "https://www.amazon.com.br/Sobrepor-28cmx40cm-Arquitech"),
    ("Kit Utensílios Inox de Cozinha", 49.98, "https://www.amazon.com.br/Kit-Utens%C3%ADlios-Inox-Cozinha-Gourmet"),
    ("Jarra de vidro", 49.92, "https://www.amazon.com.br/Diamond-Jarra-Sodo-C%C3%A1lcico"),
    ("Kit Abridor de Vinho", 48.90, "https://www.amazon.com.br/ABRIDOR-EL%C3%89TRICO-ACESS%C3%93RIOS"),
    ("Kit Caipirinha", 44.90, "https://www.amazon.com.br/Caipirinha-Drinks-Coqueteleira"),
    ("Kit Utensílios de Silicone", 39.70, "https://www.amazon.com.br/Kit-Premium-Utens%C3%ADlios-Cozinha-Silicone"),
    ("Suporte Papel Higiênico", 36.97, "https://www.amazon.com.br/Higi%C3%AAnico-Prateleira-Inoxid%C3%A1vel"),
    ("Kit Pano de Prato", 37.90, "https://www.amazon.com.br/Panos-Listrado-Felpudo-Cozinha-Algodão"),
]

# ================= CONTROLE DE PÁGINAS =================

if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= HOME =================

if st.session_state.page == "home":

    st.title("Feijoada de Chá de Casa Nova 🎉")

    st.markdown("""
É com muita alegria que convido você para celebrar essa nova fase da minha vida.
Sua presença será muito especial!
    """)

    nome = st.text_input("Seu nome")
    acompanhante = st.text_input("Nome do acompanhante (se houver)")

    st.session_state.nome = nome
    st.session_state.acompanhante = acompanhante

    if st.button("Confirmar presença e ver lista de presentes"):
        st.session_state.presenca = "Vai"
        st.session_state.page = "gifts"
        st.rerun()

    if st.button("Não conseguirei ir mas quero presentear"):
        st.session_state.presenca = "Não vai"
        st.session_state.page = "gifts"
        st.rerun()

    if st.button("Não poderei ir"):
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

    for nome, valor, link in gifts:

        st.markdown('<div class="presente-card">', unsafe_allow_html=True)

        if valor:
            st.markdown(f"### {nome}")
            st.markdown(f"💲 R$ {valor:.2f}")
            st.markdown(f"[Ver produto]({link})")
        else:
            st.markdown(f"### {nome}")
            st.markdown("Escolha qualquer valor 💛")

        if st.button(f"Reservar {nome}", key=nome):

            nova_linha = pd.DataFrame([{
                "Nome": st.session_state.nome,
                "Acompanhantes": st.session_state.acompanhante,
                "Presença": st.session_state.presenca,
                "Presente Reservado": nome,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }])

            sheet.append_rows(nova_linha.values.tolist())

            st.session_state.page = "thanks"
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

    if st.button("Voltar ao início"):
        st.session_state.page = "home"
        st.rerun()
