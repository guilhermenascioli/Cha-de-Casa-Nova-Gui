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

    st.markdown("""
    E aí! Tô muito feliz e animado por estar começando essa nova fase morando sozinho,
    montando meu cantinho do jeito que sempre sonhei.

    É um momento que significa muito pra mim, e por isso quis dividir com quem de alguma
    forma fez parte dessa caminhada.

    Se esse convite chegou até você é porque, de alguma forma, você fez parte da minha trajetória até aqui.
    Obrigado por isso. ❤️

    Seja você alguém que tá sempre por perto ou alguém que cruzou meu caminho e deixou
    uma marca importante, sua presença aqui seria muito especial.

    Você importa pra mim, e ter você celebrando junto deixaria o dia ainda mais legal.

    Se der pra vir, vai ser incrível. Se não rolar, saiba que só de você existir na minha história já me deixa grato.

    Obrigado de coração por fazer parte disso.
    """)

    name = st.text_input("Seu Nome completo")

    companions = st.number_input(
        "Quantos acompanhantes virão com você?",
        min_value=0,
        value=0,
        step=1,
    )

    if st.button("Confirmar Presença"):
        name_clean = name.strip()
        if name_clean:
            df = load_data()
            if name_clean in df["Nome"].values:
                st.error("Este nome já foi cadastrado. Use um nome diferente ou me chama no zap.")
            else:
                add_confirmation(name_clean, companions)
                st.session_state.name = name_clean
                st.session_state.page = "gifts"
                st.rerun()
        else:
            st.error("Por favor, digite seu nome.")

    df = load_data()
    if not df.empty:
        st.subheader("Quem já confirmou (área privada)")
        senha_input = st.text_input(
            "Digite a senha para ver a lista completa",
            type="password",
            key="senha_tabela_home",
        )

        if senha_input == SENHA_TABELA:
            st.success("Acesso liberado!")
            st.dataframe(df[["Nome", "Acompanhantes", "Presente Reservado", "Data"]])
        elif senha_input:
            st.error("Senha incorreta.")
        else:
            st.info("Apenas o anfitrião pode ver a lista de confirmações.")


# ============================================================================
elif st.session_state.page == "gifts":

    st.title("Sugestões de Presentes")

    st.markdown(
        "Se quiser ajudar a montar a casa, pode escolher algum item da lista abaixo "
        "(para evitar repetidos). Ou contribua via Pix, se preferir."
    )

    gifts = [
        ("💰 Pix", None, None),
        ("Cooktop de Indução 2 Bocas Preto com Trava de Segurança Painel Touch Screen", 489.90, "https://www.mercadolivre.com.br/cooktop-de-induco-2-bocas-preto-com-trava-de-seguranca-painel-touch-screen/p/MLB41647393"),
        ("Air Fryer", 404.00, "https://www.mercadolivre.com.br/fritadeira-e-forno-style-oven-fry-10-litros-elgin-3-em1-cor-preto/p/MLB51323242"),
        ("Cama Box - Baú", 399.00, "https://www.mercadolivre.com.br/cama-box-bau-casal-44x138x188cm-couro-branco/p/MLB26186586?pdp_filters=item_id%3AMLB5333956296&from=gshop&matt_tool=68817901&matt_internal_campaign_id=&matt_word=&matt_source=google&matt_campaign_id=22090354478&matt_ad_group_id=173090608476&matt_match_type=&matt_network=g&matt_device=c&matt_creative=727882732953&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=735098639&matt_product_id=MLB26186586-product&matt_product_partition_id=2392713115661&matt_target_id=aud-1966009190540:pla-2392713115661&cq_src=google_ads&cq_cmp=22090354478&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=1&gad_campaignid=22090354478&gbraid=0AAAAAD93qcBrIEmxNa_tJjVCrTeAu2x8B&gclid=CjwKCAiA2PrMBhA4EiwAwpHyC4ITJoEOJN5ojKBdu_17iLURUlkF6bH3NBPwpEpAY9j6avTQyBMpohoCzUUQAvD_BwE#reviews"),
        ("Jogo de Cama", 287.90, "https://www.zelo.com.br/jogo-de-cama-zelo-hotel-casal-percal-400-fios-liso-p1000244"),
        ("Jogo De panelas", 251.99, "https://www.casasbahia.com.br/jogo-de-panela-de-inducao-7-pecas-fundo-triplo-e-revestimento-ceramico-mimo-style-marmol/p/1579632603"),
        ("Jogo Toalha", 199.00, "https://www.casadatoalha.com.br/products/jogo-de-toalha-essence-5-pecas-cor-off-grafite-gramatura-500g-m-100-algodao-confort-soft"),
        ("Panela de Pressão", 189.91, "https://m.magazineluiza.com.br/panela-de-pressao-brinox-42l-bege-vanilla/p/237084500/ud/udpp/"),
        ("Jogo Travessa", 179.00, "https://www.westwing.com.br/jogo-de-travessa-maniglia-verde-retangular-328953.html"),
        ("Kit Churrasco", 132.99, "https://www.amazon.com.br/Pe%C3%A7as-Churrasco-Incluindo-Afiador-Armazenamento/dp/B0FLV5F9ZW"),
        ("Liquidificador", 113.05, "https://www.casasbahia.com.br/liquidificador-philco-ph900-preto-1200w-com-12-velocidades/p/5082530"),
        ("Jogo de Lençol Cinza", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891?pp=/44.2679/"),
        ("Jogo de Lençol Linho", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891?pp=/44.2875/"),
        ("Panela de Arroz", 107.91, "https://www.magazineluiza.com.br/panela-de-arroz-britania-bpa5bi-5-xicaras/p/kc02ddghb7/ep/pael/"),
        ("Potes Organizadores", 99.90, "https://www.mercadolivre.com.br/kit-9-potes-hermeticos-vidro-tampa-bambu-p-cozinha-mm-house/up/MLBU3262864032"),
        ("Jogo de Taça", 99.90, "https://www.amazon.com.br/Cristal-Premium-Elegante-Transparente-Resist%C3%AAnte/dp/B0G1CSC4QM"),
        ("Sanduicheira", 99.00, "https://www.casasbahia.com.br/sanduicheira-grill-philco-pgr25a-antiaderente-750w-luz-indicadora-preto/p/55071723"),
        ("Escorredor de Louça", 83.35, "amazon.com.br/Escorredor-Loucas-Flat-Coza-Light/dp/B07NGJM9K5/ref=asc_df_B07NGJM9K5?mcid=35ca01e1f54e357e9dac1a7102b34af3&tag=googleshopp00-20&linkCode=df0&hvadid=709864975911&hvpos=&hvnetw=g&hvrand=4191857591987175496&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9197118&hvtargid=pla-883314005477&psc=1&language=pt_BR&gad_source=1"),        
        ("Mixer", 69.90, "https://www.amazon.com.br/Mixer-Brit%C3%A2nia-BMX350P-Preto-127V/dp/B097KP1641"),
        ("Kit 3 Escorredor de Macarrão", 59.90, "https://www.amazon.com.br/Escorredor-Macarr%C3%A3o-Alimentos-Vegetais-Multiuso/dp/B0DCPDZH2N"),
        ("Kit Pote Tempero", 56.99, "https://www.amazon.com.br/Kit-Herm%C3%A9ticos-200ml-Diversos-Armazenamentos/dp/B0B29JDBWL"),
        ("Nicho de Parede Sobrepor", 54.00, "https://www.amazon.com.br/Sobrepor-28cmx40cm-Arquitech-Lavanderia-Instala%C3%A7%C3%A3o/dp/B0FX19V4WN"),
        ("Kit Utensílios Inox de Cozinha", 49.98, "https://www.amazon.com.br/Kit-Utens%C3%ADlios-Inox-Cozinha-Gourmet/dp/B0FTT2JSP5"),
        ("Jarra de vidro", 49.92, "https://www.amazon.com.br/Diamond-Jarra-Sodo-C%C3%A1lcico-Transparente-Dourado/dp/B08X1NZPYH"),
        ("Kit Abridor de Vinho", 48.90, "https://www.amazon.com.br/ABRIDOR-EL%C3%89TRICO-ACESS%C3%93RIOS-ROLHAS-DECANTER/dp/B0BQH4KC3N"),
        ("Kit Caipirinha", 44.90, "https://www.amazon.com.br/Caipirinha-Drinks-Coqueteleira-Dosador-Socador/dp/B09C6MZ2N8"),
        ("Kit Utensílios de Silicone", 39.70, "https://www.amazon.com.br/Kit-Premium-Utens%C3%ADlios-Cozinha-Silicone/dp/B0F6YT4VHP"),
        ("Suporte Papel Higiênico", 36.97, "https://www.amazon.com.br/Higi%C3%AAnico-Prateleira-Inoxid%C3%A1vel-Instala%C3%A7%C3%A3o-Banheiro/dp/B0F5C5M1LW/ref=asc_df_B0F5C5M1LW?mcid=93652418062336ddbd5d76dade158c7b&tag=googleshopp00-20&linkCode=df0&hvadid=715067048070&hvpos=&hvnetw=g&hvrand=1004044875430345428&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9197118&hvtargid=pla-2421703334158&psc=1&language=pt_BR&gad_source=1"),
        ("Kit Pano de Prato", 37.90, "https://www.amazon.com.br/Panos-Listrado-Felpudo-Cozinha-Algod%C3%A3o/dp/B0CH3QXD8V"),
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

        # resto da sua lógica permanece IGUAL ↓↓↓

        if title != "💰 Pix" and title in reserved:
            st.markdown("**🎁 Já reservado** 🔒")
            st.caption("Alguém já escolheu esse item.")
        else:
            if title == "💰 Pix":
                if st.button("Quero contribuir via Pix", key=f"pix_btn"):
                    st.session_state.show_pix_form = True
                    st.rerun()

                if st.session_state.show_pix_form:
                    st.info("Ótimo! Qual valor você pretende enviar via Pix?")
                    pix_value = st.number_input(
                        "Valor (R$)",
                        min_value=0.00,
                        value=0.00,
                        step=50.00,
                        format="%.2f",
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Confirmar contribuição", type="primary"):
                            update_gift(st.session_state.name, f"Pix - R$ {pix_value:,.2f}")
                            st.session_state.show_pix_form = False
                            st.session_state.page = "pix_thanks"
                            st.rerun()
                    with col2:
                        if st.button("Cancelar"):
                            st.session_state.show_pix_form = False
                            st.rerun()
            else:
                if st.button("Quero reservar esse presente", key=f"want_{title}"):
                    st.session_state.selected_gift = title
                    st.rerun()

                if (
                    st.session_state.get("selected_gift") == title
                ):
                    st.info(f"Você selecionou: **{title}**")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Confirmar reserva", type="primary", key=f"conf_{title}"):
                            update_gift(st.session_state.name, title)
                            st.session_state.page = "thanks"
                            st.session_state.selected_gift = None
                            st.rerun()
                    with col2:
                        if st.button("Cancelar", key=f"cancel_{title}"):
                            st.session_state.selected_gift = None
                            st.rerun()

        st.markdown("---")

    if st.button("→ Continuar sem reservar presente", type="secondary"):
        st.session_state.page = "thanks"
        st.session_state.selected_gift = None
        st.session_state.show_pix_form = False
        st.rerun()


# ============================================================================
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
        st.session_state.selected_gift = None
        st.session_state.show_pix_form = False
        st.rerun()

# ============================================================================
elif st.session_state.page == "pix_thanks":

    st.title("Muito obrigado pela contribuição! 🙌")

    st.markdown("""
    Agradeço de coração pela ajuda via Pix.
    Vai fazer muita diferença na montagem da casa nova. ❤️
    """)

    st.subheader("Chave Pix")
    st.code("444.858.688-00", language=None)
    st.caption("CPF – Guilherme")

    st.markdown("[Falar comigo no WhatsApp →](https://w.app/4qrasc)")

    st.balloons()

    if st.button("Voltar ao início"):
        st.session_state.page = "home"
        st.session_state.selected_gift = None
        st.session_state.show_pix_form = False
        st.rerun()
