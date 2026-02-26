import streamlit as st
import pandas as pd
import os

DATA_FILE = "confirmations.csv"
SENHA_TABELA = "195967"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["Presente Reservado"] = df["Presente Reservado"].fillna("").astype(str)
            return df
        except Exception:
            st.warning("Arquivo CSV corrompido. Criando novo.")
    df = pd.DataFrame(columns=["Nome", "Acompanhantes", "Presente Reservado"])
    df.to_csv(DATA_FILE, index=False)
    return df

if "page" not in st.session_state:
    st.session_state.page = "home"
if "name" not in st.session_state:
    st.session_state.name = None
if "selected_gift" not in st.session_state:
    st.session_state.selected_gift = None
if "show_pix_form" not in st.session_state:
    st.session_state.show_pix_form = False

# ================= HOME =================
if st.session_state.page == "home":
    st.title("Bem-vindo ao meu Chá de Casa Nova!")

    name = st.text_input("Seu Nome completo")
    companions = st.number_input("Quantos acompanhantes?", min_value=0, value=0)

    if st.button("Confirmar Presença"):
        name_clean = name.strip()
        if name_clean:
            df = load_data()
            if name_clean in df["Nome"].values:
                st.error("Este nome já foi cadastrado.")
            else:
                new_row = {
                    "Nome": name_clean,
                    "Acompanhantes": companions,
                    "Presente Reservado": ""
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)

                st.session_state.name = name_clean
                st.session_state.page = "gifts"
                st.rerun()
        else:
            st.error("Digite seu nome.")

    df = load_data()
    if not df.empty:
        senha_input = st.text_input("Senha para ver lista", type="password")
        if senha_input == SENHA_TABELA:
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Baixar CSV",
                csv,
                "confirmados.csv",
                "text/csv"
            )

# ================= GIFTS =================
elif st.session_state.page == "gifts":

    st.title("Sugestões de Presentes")

    gifts = [
        ("Pix", None),
        ("Air Fryer", 381.00),
        ("Jogo de Cama", 287.90),
        ("Liquidificador", 113.05),
    ]

    df = load_data()
    reserved = set(df["Presente Reservado"].str.replace("Pix - R\\$ .*", "Pix", regex=True))

    for title, price in gifts:

        st.markdown(f"### {title}")

        if price:
            st.markdown(f"R$ {price:,.2f}")

        # ================= PIX =================
        if title == "Pix":

            if st.button("Quero contribuir via Pix"):
                st.session_state.show_pix_form = True

            if st.session_state.show_pix_form:

                pix_value = st.number_input(
                    "Valor do Pix (R$)",
                    min_value=0.01,
                    value=50.00,
                    step=1.00,
                    format="%.2f"
                )

                if st.button("Confirmar Pix", type="primary"):
                    df = load_data()

                    df.loc[
                        df["Nome"] == st.session_state.name,
                        "Presente Reservado"
                    ] = f"Pix - R$ {pix_value:,.2f}"

                    df.to_csv(DATA_FILE, index=False)

                    st.session_state.show_pix_form = False
                    st.session_state.page = "pix_thanks"
                    st.rerun()

        # ================= PRESENTES FÍSICOS =================
        else:
            if title in reserved:
                st.markdown("🎁 Já reservado")
            else:
                if st.button("Reservar", key=title):
                    df = load_data()
                    df.loc[
                        df["Nome"] == st.session_state.name,
                        "Presente Reservado"
                    ] = title

                    df.to_csv(DATA_FILE, index=False)

                    st.session_state.page = "thanks"
                    st.rerun()

        st.markdown("---")

# ================= THANKS =================
elif st.session_state.page == "thanks":
    st.title("Obrigado! 🎉")
    st.balloons()

    if st.button("Voltar"):
        st.session_state.page = "home"
        st.rerun()

# ================= PIX THANKS =================
elif st.session_state.page == "pix_thanks":
    st.title("Obrigado pelo Pix 🙌")

    st.subheader("Chave Pix")
    st.code("444.858.688-00")

    st.balloons()

    if st.button("Voltar"):
        st.session_state.page = "home"
        st.rerun()
