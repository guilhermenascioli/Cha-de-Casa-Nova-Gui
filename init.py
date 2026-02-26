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
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1


def load_data():
    data = sheet.get_all_records()
    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame(columns=["Nome", "Acompanhantes", "Presente Reservado", "Data"])


def add_confirmation(nome, acompanhantes):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    sheet.append_row([nome, acompanhantes, "", data])


def update_gift(nome, presente):
    records = sheet.get_all_records()
    for i, row in enumerate(records):
        if row["Nome"] == nome:
            sheet.update_cell(i + 2, 3, presente)
            break


# ================= SESSION =================

if "page" not in st.session_state:
    st.session_state.page = "home"
if "name" not in st.session_state:
    st.session_state.name = None
if "selected_gift" not in st.session_state:
    st.session_state.selected_gift = None
if "show_pix_form" not in st.session_state:
    st.session_state.show_pix_form = False

# ============================================================================

if st.session_state.page == "home":
    st.title("Bem-vindo ao meu Chá de Casa Nova!")

    name = st.text_input("Seu Nome completo")
    companions = st.number_input("Quantos acompanhantes virão com você?", min_value=0, value=0, step=1)

    if st.button("Confirmar Presença"):
        name_clean = name.strip()
        if name_clean:
            df = load_data()
            if name_clean in df["Nome"].values:
                st.error("Este nome já foi cadastrado.")
            else:
                add_confirmation(name_clean, companions)
                st.session_state.name = name_clean
                st.session_state.page = "gifts"
                st.rerun()
        else:
            st.error("Por favor, digite seu nome.")

    df = load_data()
    if not df.empty:
        st.subheader("Área do anfitrião")

        senha_input = st.text_input("Digite a senha", type="password")

        if senha_input == SENHA_TABELA:
            st.success("Acesso liberado!")
            st.dataframe(df[["Nome", "Acompanhantes", "Presente Reservado", "Data"]])
        elif senha_input:
            st.error("Senha incorreta.")

# ============================================================================

elif st.session_state.page == "gifts":
    st.title("Sugestões de Presentes")

    gifts = [
        ("Pix", None, None),

        ("Cooktop de Indução 2 Bocas Preto com Trava de Segurança Painel Touch Screen", 489.90, "https://www.mercadolivre.com.br/cooktop-de-induco-2-bocas-preto-com-trava-de-seguranca-painel-touch-screen/p/MLB41647393"),
        ("Air Fryer", 404.00, "https://www.mercadolivre.com.br/fritadeira-e-forno-style-oven-fry-10-litros-elgin-3-em1-cor-preto/p/MLB51323242"),
        ("Jogo de Cama", 287.90, "https://www.zelo.com.br/jogo-de-cama-zelo-hotel-casal-percal-400-fios-liso-p1000244"),
        ("Jogo De panelas", 251.99, "https://www.casasbahia.com.br/jogo-de-panela-de-inducao-7-pecas-fundo-triplo-e-revestimento-ceramico-mimo-style-marmol/p/1579632603"),
        ("Jogo Toalha", 199.00, "https://www.casadatoalha.com.br/products/jogo-de-toalha-essence-5-pecas-cor-off-grafite-gramatura-500g-m-100-algodao-confort-soft"),
        ("Panela de Pressão", 189.91, "https://m.magazineluiza.com.br/panela-de-pressao-brinox-42l-bege-vanilla/p/237084500/ud/udpp/"),
        ("Jogo Travessa", 179.00, "https://www.westwing.com.br/jogo-de-travessa-maniglia-verde-retangular-328953.html"),
        ("Kit Churrasco", 132.99, "https://www.amazon.com.br/Pe%C3%A7as-Churrasco-Incluindo-Afiador-Armazenamento/dp/B0FLV5F9ZW"),
        ("Jogo de Lençol Cinza", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891?pp=/44.2679/"),
        ("Jogo de Lençol Linho", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891?pp=/44.2875/"),
        ("Liquidificador", 113.05, "https://www.casasbahia.com.br/liquidificador-philco-ph900-preto-1200w-com-12-velocidades/p/5082530"),
        ("Panela de Arroz", 107.91, "https://www.magazineluiza.com.br/panela-de-arroz-britania-bpa5bi-5-xicaras/p/kc02ddghb7/ep/pael/"),
        ("Potes Organizadores", 99.90, "https://www.mercadolivre.com.br/kit-9-potes-hermeticos-vidro-tampa-bambu-p-cozinha-mm-house/up/MLBU3262864032"),
        ("Jogo de Taça", 99.90, "https://www.amazon.com.br/Cristal-Premium-Elegante-Transparente-Resist%C3%AAnte/dp/B0G1CSC4QM"),
        ("Sanduicheira", 99.00, "https://www.casasbahia.com.br/sanduicheira-grill-philco-pgr25a-antiaderente-750w-luz-indicadora-preto/p/55071723"),
        ("Suporte Papel Higiênico", 78.90, "https://www.amazon.com.br/Suporte-Higi%C3%AAnico-Banheiro-Madeira-Rustico/dp/B0G1PQFZL8"),
        ("Mixer", 69.90, "https://www.amazon.com.br/Mixer-Brit%C3%A2nia-BMX350P-Preto-127V/dp/B097KP1641"),
        ("Kit 3 Escorredor de Macarrão", 59.90, "https://www.amazon.com.br/Escorredor-Macarr%C3%A3o-Alimentos-Vegetais-Multiuso/dp/B0DCPDZH2N"),
        ("Kit Pote Tempero", 56.99, "https://www.amazon.com.br/Kit-Herm%C3%A9ticos-200ml-Diversos-Armazenamentos/dp/B0B29JDBWL"),
        ("Nicho de Parede Sobrepor", 54.00, "https://www.amazon.com.br/Sobrepor-28cmx40cm-Arquitech-Lavanderia-Instala%C3%A7%C3%A3o/dp/B0FX19V4WN"),
        ("Kit Utensílios Inox de Cozinha", 49.98, "https://www.amazon.com.br/Kit-Utens%C3%ADlios-Inox-Cozinha-Gourmet/dp/B0FTT2JSP5"),
        ("Jarra de vidro", 49.92, "https://www.amazon.com.br/Diamond-Jarra-Sodo-C%C3%A1lcico-Transparente-Dourado/dp/B08X1NZPYH"),
        ("Kit Abridor de Vinho", 48.90, "https://www.amazon.com.br/ABRIDOR-EL%C3%89TRICO-ACESS%C3%93RIOS-ROLHAS-DECANTER/dp/B0BQH4KC3N"),
        ("Kit Caipirinha", 44.90, "https://www.amazon.com.br/Caipirinha-Drinks-Coqueteleira-Dosador-Socador/dp/B09C6MZ2N8"),
        ("Escorredor de Louça Compacto", 39.70, "https://www.amazon.com.br/Escorredor-Lou%C3%A7as-Compacto-Linha-Trium/dp/B0C5RKCKXM"),
        ("Kit Utensílios de Silicone", 39.70, "https://www.amazon.com.br/Kit-Premium-Utens%C3%ADlios-Cozinha-Silicone/dp/B0F6YT4VHP"),
        ("Kit Pano de Prato", 37.90, "https://www.amazon.com.br/Panos-Listrado-Felpudo-Cozinha-Algod%C3%A3o/dp/B0CH3QXD8V"),
    ]

    df = load_data()
    df["Presente Reservado"] = df["Presente Reservado"].fillna("").astype(str).str.strip()
    reserved = set(df["Presente Reservado"][df["Presente Reservado"] != ""])

    numero = 1

    for title, price, url in gifts:

        if title == "Pix":
            st.markdown("### Pix 💳")
        else:
            st.markdown(f"### {numero}. {title}")
            numero += 1

        if price is not None:
            st.markdown(f"**Preço: R$ {price:,.2f}**")

        if url:
            st.markdown(f"[Ver produto →]({url})")
        else:
            st.markdown("(Contribuição via Pix)")

        if title != "Pix" and title in reserved:
            st.markdown("**🎁 Já reservado** 🔒")
        else:
            if title == "Pix":
                if st.button("Quero contribuir via Pix", key="pix_btn"):
                    st.session_state.page = "pix_thanks"
                    st.rerun()
            else:
                if st.button("Quero reservar esse presente", key=f"btn_{title}"):
                    update_gift(st.session_state.name, title)
                    st.session_state.page = "thanks"
                    st.rerun()

        st.markdown("---")

# ============================================================================

elif st.session_state.page == "thanks":
    st.title("Muito obrigado mesmo! 🚀")
    st.balloons()

    if st.button("Voltar ao início"):
        st.session_state.page = "home"
        st.rerun()

elif st.session_state.page == "pix_thanks":
    st.title("Muito obrigado pela contribuição! 🙌")
    st.code("444.858.688-00")
    st.balloons()

    if st.button("Voltar ao início"):
        st.session_state.page = "home"
        st.rerun()
