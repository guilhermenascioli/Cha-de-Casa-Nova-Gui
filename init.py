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
    st.secrets["gcp_service_account"], scopes=scope
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1


def load_data():
    data = sheet.get_all_records()
    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame(columns=["Nome", "Acompanhantes", "Presença", "Presente Reservado", "Data"])


def save_confirmation(nome, acompanhantes, presenca, presente):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    sheet.append_row([nome, acompanhantes, presenca, presente, data])


# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "name" not in st.session_state:
    st.session_state.name = None

if "companions" not in st.session_state:
    st.session_state.companions = 0

if "presence_status" not in st.session_state:
    st.session_state.presence_status = None

if "selected_gift" not in st.session_state:
    st.session_state.selected_gift = None

if "show_pix_form" not in st.session_state:
    st.session_state.show_pix_form = False


# ============================================================================
# HOME
# ============================================================================
if st.session_state.page == "home":

    st.title("Bem-vindo ao meu Chá de Casa Nova!")

    name = st.text_input("Seu Nome completo")
    companions = st.number_input(
        "Quantos acompanhantes virão com você?",
        min_value=0,
        value=0,
        step=1,
    )

    st.markdown("### O que você deseja fazer?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Confirmar presença e ver lista"):
            if name.strip():
                st.session_state.name = name.strip()
                st.session_state.companions = companions
                st.session_state.presence_status = "Vai"
                st.session_state.page = "gifts"
                st.rerun()
            else:
                st.error("Digite seu nome.")

    with col2:
        if st.button("🎁 Não conseguirei ir mas quero presentear"):
            if name.strip():
                st.session_state.name = name.strip()
                st.session_state.companions = 0
                st.session_state.presence_status = "Não vai"
                st.session_state.page = "gifts"
                st.rerun()
            else:
                st.error("Digite seu nome.")

    with col3:
        if st.button("❌ Não poderei ir"):
            if name.strip():
                save_confirmation(name.strip(), 0, "Não vai", "")
                st.success("Obrigado por avisar ❤️")
            else:
                st.error("Digite seu nome.")


# ============================================================================
# LISTA DE PRESENTES (SUA LISTA INTACTA)
# ============================================================================
elif st.session_state.page == "gifts":

    st.title("Sugestões de Presentes")

    st.info(f"Olá, {st.session_state.name}!")

    st.markdown(
        "Se quiser ajudar a montar a casa, pode escolher algum item da lista abaixo "
        "(para evitar repetidos). Ou contribua via Pix, se preferir."
    )

    # 👇 SUA LISTA COMPLETA PERMANECE EXATAMENTE IGUAL
    gifts = [
        ("💰 Pix", None, None),
        ("Cooktop de Indução 2 Bocas", 489.90, "https://www.mercadolivre.com.br/cooktop-de-induco-2-bocas-preto-com-trava-de-seguranca-painel-touch-screen/p/MLB41647393"),
        ("Air Fryer", 404.00, "https://www.mercadolivre.com.br/fritadeira-e-forno-style-oven-fry-10-litros-elgin-3-em1-cor-preto/p/MLB51323242"),
        ("Cama Box - Baú", 399.00, "https://www.mercadolivre.com.br/cama-box-bau-casal-44x138x188cm-couro-branco/p/MLB26186586?pdp_filters=item_id%3AMLB5333956296"),
        ("Jogo de Cama", 287.90, "https://www.zelo.com.br/jogo-de-cama-zelo-hotel-casal-percal-400-fios-liso-p1000244"),
        ("Jogo De panelas", 251.99, "https://www.casasbahia.com.br/jogo-de-panela-de-inducao-7-pecas-fundo-triplo-e-revestimento-ceramico-mimo-style-marmol/p/1579632603"),
        ("Jogo Toalha", 199.00, "https://www.casadatoalha.com.br/products/jogo-de-toalha-essence-5-pecas"),
        ("Colcha Casal", 191.90, "https://www.zelo.com.br/colcha-chamonix-casal-com-2-porta-travesseiros-beca-decor-p1011005"),
        ("Panela de Pressão", 189.91, "https://m.magazineluiza.com.br/panela-de-pressao-brinox-42l-bege-vanilla/p/237084500/ud/udpp/"),
        ("Jogo Travessa", 179.00, "https://www.westwing.com.br/jogo-de-travessa-maniglia-verde-retangular-328953.html"),
        ("Kit Churrasco", 132.99, "https://www.amazon.com.br/Pe%C3%A7as-Churrasco-Incluindo-Afiador-Armazenamento/dp/B0FLV5F9ZW"),
        ("Liquidificador", 113.05, "https://www.casasbahia.com.br/liquidificador-philco-ph900-preto-1200w-com-12-velocidades/p/5082530"),
        ("Jogo de Lençol Cinza", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891"),
        ("Jogo de Lençol Linho", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891"),
        ("Panela de Arroz", 107.91, "https://www.magazineluiza.com.br/panela-de-arroz-britania-bpa5bi-5-xicaras/p/kc02ddghb7/ep/pael/"),
        ("Potes Organizadores", 99.90, "https://www.mercadolivre.com.br/kit-9-potes-hermeticos"),
        ("Jogo de Taça", 99.90, "https://www.amazon.com.br/Cristal-Premium-Elegante"),
        ("Sanduicheira", 99.00, "https://www.casasbahia.com.br/sanduicheira-grill-philco-pgr25a"),
        ("Escorredor de Louça", 83.35, "https://www.amazon.com.br/Escorredor-Loucas-Flat-Coza-Light"),
        ("Cobertor", 82.10, "https://shopee.com.br/product/1572699366"),
        ("Mixer", 69.90, "https://www.amazon.com.br/Mixer-Brit%C3%A2nia-BMX350P-Preto-127V/dp/B097KP1641"),
        ("Kit 3 Escorredor de Macarrão", 59.90, "https://www.amazon.com.br/Escorredor-Macarr%C3%A3o-Alimentos-Vegetais-Multiuso"),
        ("Kit Pote Tempero", 56.99, "https://www.amazon.com.br/Kit-Herm%C3%A9ticos-200ml-Diversos-Armazenamentos"),
        ("Nicho de Parede Sobrepor", 54.00, "https://www.amazon.com.br/Sobrepor-28cmx40cm-Arquitech-Lavanderia"),
        ("Kit Utensílios Inox de Cozinha", 49.98, "https://www.amazon.com.br/Kit-Utens%C3%ADlios-Inox-Cozinha-Gourmet"),
        ("Jarra de vidro", 49.92, "https://www.amazon.com.br/Diamond-Jarra-Sodo-C%C3%A1lcico-Transparente"),
        ("Kit Abridor de Vinho", 48.90, "https://www.amazon.com.br/ABRIDOR-EL%C3%89TRICO-ACESS%C3%93RIOS"),
        ("Kit Caipirinha", 44.90, "https://www.amazon.com.br/Caipirinha-Drinks-Coqueteleira-Dosador-Socador"),
        ("Kit Utensílios de Silicone", 39.70, "https://www.amazon.com.br/Kit-Premium-Utens%C3%ADlios-Cozinha-Silicone"),
        ("Suporte Papel Higiênico", 36.97, "https://www.amazon.com.br/Higi%C3%AAnico-Prateleira-Inoxid%C3%A1vel"),
        ("Kit Pano de Prato", 37.90, "https://www.amazon.com.br/Panos-Listrado-Felpudo-Cozinha-Algod%C3%A3o"),
    ]

    df = load_data()
    df["Presente Reservado"] = df["Presente Reservado"].fillna("").astype(str).str.strip()
    reserved = set(df["Presente Reservado"][df["Presente Reservado"] != ""])

    contador = 1

    for title, price, url in gifts:

        if title != "💰 Pix":
            st.markdown(f"### {contador}. {title}")
            contador += 1
        else:
            st.markdown(f"### {title}")

        if price is not None:
            st.markdown(f"**Preço: R$ {price:,.2f}**")

        if url:
            st.markdown(f"[Ver produto →]({url})")
        else:
            st.markdown("(Contribuição via Pix)")

        if title != "💰 Pix" and title in reserved:
            st.markdown("**🎁 Já reservado** 🔒")
        else:

            if title == "💰 Pix":
                if st.button("Quero contribuir via Pix", key="pix"):
                    st.session_state.show_pix_form = True

                if st.session_state.show_pix_form:
                    pix_value = st.number_input("Valor (R$)", min_value=0.0, step=50.0)

                    if st.button("Confirmar contribuição"):
                        save_confirmation(
                            st.session_state.name,
                            st.session_state.companions,
                            st.session_state.presence_status,
                            f"Pix - R$ {pix_value:,.2f}",
                        )
                        st.session_state.page = "pix_thanks"
                        st.rerun()

            else:
                if st.button("Quero reservar esse presente", key=title):
                    save_confirmation(
                        st.session_state.name,
                        st.session_state.companions,
                        st.session_state.presence_status,
                        title,
                    )
                    st.session_state.page = "thanks"
                    st.rerun()

        st.markdown("---")


# ============================================================================
elif st.session_state.page == "thanks":

    st.title("Muito obrigado mesmo! 🚀")
    st.balloons()

    if st.button("Voltar ao início"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================================================
elif st.session_state.page == "pix_thanks":

    st.title("Muito obrigado pela contribuição! 🙌")
    st.balloons()

    if st.button("Voltar ao início"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
