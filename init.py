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
        ("Cooktop de Indução 2 Bocas", 489.90, "..."),
        # 👇 mantém o restante da sua lista exatamente igual
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
