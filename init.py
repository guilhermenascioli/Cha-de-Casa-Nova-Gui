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
    scopes=scope
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

if "presence" not in st.session_state:
    st.session_state.presence = None

if "selected_gift" not in st.session_state:
    st.session_state.selected_gift = None

if "show_pix_form" not in st.session_state:
    st.session_state.show_pix_form = False

# ============================================================================

if st.session_state.page == "home":

    st.title("Bem-vindo ao meu Chá de Casa Nova!")

    st.markdown("""
E aí! Tô muito feliz e animado por estar começando essa nova fase morando sozinho, montando meu cantinho do jeito que sempre sonhei.

É um momento que significa muito pra mim, e por isso quis dividir com quem de alguma forma fez parte dessa caminhada. Se esse convite chegou até você é porque, de alguma forma, você fez parte da minha trajetória até aqui. Obrigado por isso. ❤️

Seja você alguém que tá sempre por perto ou alguém que cruzou meu caminho e deixou uma marca importante, sua presença aqui seria muito especial. Você importa pra mim, e ter você celebrando junto deixaria o dia ainda mais legal.

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

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Confirmar presença e ver lista de presentes"):
            if name.strip():
                st.session_state.name = name.strip()
                st.session_state.companions = companions
                st.session_state.presence = "Vai"
                st.session_state.page = "gifts"
                st.rerun()
            else:
                st.error("Digite seu nome.")

    with col2:
        if st.button("Não conseguirei ir mas quero presentear"):
            if name.strip():
                st.session_state.name = name.strip()
                st.session_state.companions = companions
                st.session_state.presence = "Não vai"
                st.session_state.page = "gifts"
                st.rerun()
            else:
                st.error("Digite seu nome.")

    with col3:
        if st.button("Não poderei ir"):
            if name.strip():
                save_confirmation(name.strip(), companions, "Não vai (sem presente)", "")
                st.success("Obrigado por avisar ❤️")
            else:
                st.error("Digite seu nome.")

    # 🔐 ÁREA PRIVADA
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
            st.dataframe(df[["Nome", "Acompanhantes", "Presença", "Presente Reservado", "Data"]])
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
    ("Cooktop de Indução 2 Bocas", 489.90, "https://www.mercadolivre.com.br/cooktop-de-induco-2-bocas-preto-com-trava-de-seguranca-painel-touch-screen/p/MLB41647393"),
    ("Air Fryer", 404.00, "https://www.mercadolivre.com.br/fritadeira-e-forno-style-oven-fry-10-litros-elgin-3-em1-cor-preto/p/MLB51323242"),
    ("Cama Box - Baú", 399.00, "https://www.mercadolivre.com.br/cama-box-bau-casal-44x138x188cm-couro-branco/p/MLB26186586"),
    ("Jogo de Cama", 287.90, "https://www.zelo.com.br/jogo-de-cama-zelo-hotel-casal-percal-400-fios-liso-p1000244"),
    ("Jogo De panelas", 277.40, "https://www.mercadolivre.com.br/jogo-de-panelas-mimo-style-fundo-triplo-induco-5-pecas-cor-bege/p/MLB35490890?pdp_filters=item_id:MLB5219507672&matt_tool=68281196&matt_internal_campaign_id=355305595&matt_word=&matt_source=google&matt_campaign_id=23048606145&matt_ad_group_id=189911819966&matt_match_type=&matt_network=g&matt_device=c&matt_creative=791291032969&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=5649602495&matt_product_id=MLB5219507672&matt_product_partition_id=2458687813826&matt_target_id=aud-1966490908987:pla-2458687813826&cq_src=google_ads&cq_cmp=23048606145&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=1&gad_campaignid=23048606145&gbraid=0AAAAAD93qcDtzoZTNRrooZ35lTqRptVgb&gclid=CjwKCAiAqprNBhB6EiwAMe3yhkWLyZn1nhieQiV0jD0iatMDeT4UQUGN8S-_ap2XdU_b1hWrUDGfBxoCdJkQAvD_BwE"),
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
    ("Kit Abridor de Vinho", 45.99, "https://www.amazon.com.br/ABRIDOR-EL%C3%89TRICO-ACESS%C3%93RIOS-ROLHAS-DECANTER/dp/B0BQH4KC3N/ref=sr_1_6?crid=SN1DV6WPE99R&dib=eyJ2IjoiMSJ9.1Fgvr5sIZ9GxWnjVHp1uH5Q4uo7htStUoV5olLhzLq5tI8l3RjVgRGnYdu3R-vASAi6k14PNL55PDhFTQ51sTvhfbr0RSTNzoCjgfzW5YvxPem8xmF-tpVbk812-Pn0SZiKjdGmqJIb6xHlTBWIfJy2K_xSWBE775Dsffp_SG7MoGLDw4uvq_p2VLEYxjeOPmfberZeSqyYUgikdrrMEk2iaoGcKAwjt9TLdxvzRxrk.iKI_rLQgrTXmQwmCJDrE_xvFbdDJa9HY_0_IsvDriIA&dib_tag=se&keywords=abridor+de+vinho&qid=1772545766&s=kitchen&sprefix=abridor+de+%2Ckitchen%2C185&sr=1-6&ufe=app_do%3Aamzn1.fos.6d798eae-cadf-45de-946a-f477d47705b9"),
    ("Kit Caipirinha", 39.90, "https://www.amazon.com.br/Caipirinha-Drinks-Coqueteleira-Dosador-Socador/dp/B09C6MZ2N8/ref=sr_1_6?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=RY3FFS5HTJUP&dib=eyJ2IjoiMSJ9.Rp5RRNASBKPgA9oPgpXBRQFSWmK6hJa-5F4FjAXymlK8cV1CYj-nGvgmSwGSOYJ82P07kzTi-0ylf_uJSHpA4wUos-qVF0WJm8u4JCo6CVOGepBwCSRJKusvEn174Cwfww9Elg4aw2rdeX7rL46XH0hUQz27l-2Wp0771ml9LnApBOo6Rfk8LUitjoJ48VjUePzZKzKNN_dL6nppF-zdkeBaUW1LnKWgKrCoj5qNe7s.owD_Juvo93Dx1mGBtkdY-zQGyowdodL9c0Ku9osUocI&dib_tag=se&keywords=kit+caipirinha&qid=1772545677&s=kitchen&sprefix=kit+caipirin%2Ckitchen%2C179&sr=1-6"),
    ("Kit Utensílios de Silicone", 39.70, "https://www.amazon.com.br/Kit-Premium-Utens%C3%ADlios-Cozinha-Silicone/dp/B0F6YT4VHP?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A3EYS3YI88WD0A"),
    ("Suporte Papel Higiênico", 37.97, "https://www.amazon.com.br/Higi%C3%AAnico-Prateleira-Inoxid%C3%A1vel-Instala%C3%A7%C3%A3o-Banheiro/dp/B0F5C5M1LW/ref=sr_1_9?dib=eyJ2IjoiMSJ9.tXVx9JpmX_BHf-ORsXogtpW0Ke3CwOqBTI4zYHVPT6gs5AH--OCxZv5KHbqnH8GI0ckbRSgjk4rPOEYYFY3z0lc0JR6DQN7VQDuWqY-i599VAHgHgcy8QPzsFBKUEjKqmAc4F9Omnkb7hAUf0r4WxvoNwUq1b7sT2mI9oqegS-KBr_EYfJdtn2nKvHh6fPUkiF2sWMc8eyUWFTH8PDHrbZ71BhAOM0dAjZJZlmVzljEa6ZfRuXAg3BiJvcQbSXIJYjoE7SQ16bKemU8LudAv_r5DOrDhC_FtZSvS29YkFiE.2ZNyS2QMiJwhvHrQFk8iKHTXtgoi01_tr-LGEwdQ1tI&dib_tag=se&keywords=suporte+papel+higienico&qid=1772545595&sr=8-9"),
    ("Kit Pano de Prato", 37.90, "https://www.amazon.com.br/Panos-Listrado-Felpudo-Cozinha-Algod%C3%A3o/dp/B0CH3QXD8V?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A2AWA4J8IWDR3I"),
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
            st.caption("Alguém já escolheu esse item.")
        else:

            if title == "💰 Pix":
                if st.button("Quero contribuir via Pix", key=f"pix_btn"):
                    st.session_state.show_pix_form = True
                    st.rerun()

                if st.session_state.show_pix_form:
                    pix_value = st.number_input(
                        "Valor (R$)",
                        min_value=0.00,
                        value=0.00,
                        step=50.00,
                        format="%.2f",
                    )

                    if st.button("Confirmar contribuição"):
                        save_confirmation(
                            st.session_state.name,
                            st.session_state.companions,
                            st.session_state.presence,
                            f"Pix - R$ {pix_value:,.2f}"
                        )
                        st.session_state.page = "pix_thanks"
                        st.rerun()

            else:
                if st.button("Quero reservar esse presente", key=f"want_{title}"):
                    save_confirmation(
                        st.session_state.name,
                        st.session_state.companions,
                        st.session_state.presence,
                        title
                    )
                    st.session_state.page = "thanks"
                    st.rerun()

        st.markdown("---")

# ============================================================================

elif st.session_state.page == "thanks":

    st.title("Muito obrigado mesmo! 🚀")

    st.markdown("""
Valeu demais por confirmar a presença e fazer parte dessa nova etapa da minha vida!
Fico muito feliz de te receber e comemorar junto.
Tô contando os dias! 🫂
""")

    st.subheader("Endereço para entrega")
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
        st.rerun()
