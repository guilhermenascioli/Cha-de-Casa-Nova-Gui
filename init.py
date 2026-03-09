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
    ("Jogo Toalha", 199.00, "https://www.casadatoalha.com.br/products/jogo-de-toalha-essence-5-pecas-cor-off-grafite-gramatura-500g-m-100-algodao-confort-soft?variant=53765080187252&country=BR&currency=BRL&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gad_source=1&gad_campaignid=23346720634&gbraid=0AAAAACw6cAdZ56t_qqme5kT3qWG1_8Ini&gclid=CjwKCAiAqprNBhB6EiwAMe3yhgIxK3G1h3USiYEcG62obpNirV5RRcb99LhF-qAffbM_ZtKgiCE6TBoCC8YQAvD_BwE"),
    ("Colcha Casal", 191.90, "https://www.zelo.com.br/colcha-chamonix-casal-com-2-porta-travesseiros-beca-decor-p1011005?pp=/44.2609/"),
    ("Panela de Pressão", 189.91, "https://www.mercadolivre.com.br/panela-de-presso-max-chef-wood-42l-para-induco-design-wood-verde-acizentado/p/MLB63327834?pdp_filters=item_id%3AMLB6203311988&from=gshop&matt_tool=86217123&matt_word=&matt_source=google&matt_campaign_id=23351282321&matt_ad_group_id=191545524922&matt_match_type=&matt_network=g&matt_device=c&matt_creative=787871604137&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=735128761&matt_product_id=MLB63327834-product&matt_product_partition_id=2388009209946&matt_target_id=aud-1966490908987:pla-2388009209946&cq_src=google_ads&cq_cmp=23351282321&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=1&gad_campaignid=23351282321&gbraid=0AAAAAD93qcA5trhbxKKKhvCENucE4smbI&gclid=CjwKCAiAqprNBhB6EiwAMe3yhgc-2GxcVat0cN3Zrb_hpRiSkbzK_vCavYr1gMVu45mO73ZXQPmE_BoCS7MQAvD_BwE"),
    ("Kit Churrasco", 139.99, "https://www.amazon.com.br/Churrasco-Tradicional-Pe%C3%A7as-Tabua-T%C3%A1bua/dp/B0FP19W6GP/ref=sr_1_59_sspa?dib=eyJ2IjoiMSJ9.Bp44b9rXSyRiN7rlkglqiKsSUqUgztMRpbCOuDONoXVZTepIhLACQqg0gxHn1q7dAVQlFFVHPBQWh9i_s0Ck5da5kOn6z352NM7l61aRB7pbGUPAqjqwdjgaGgEIFS1POIz8a_oYRfCp4cSvvAcHXfne0a8_2apF4L6p8I3e5m9w12VSFglznJmMhRjqXl7BGHaa8ZRElkc7b6-bVxzblQHUoYF28XbrBMo9Z6HSfveCvfra79cMgc_YHnt18slpsD1M8NNGy2LfJXolynF0VILXYUT0bkOQTWNbgemWF4Q.agpIbZE_APGBdigw8FOBRLDX3UoHoyTKeFIEDOq6yKA&dib_tag=se&keywords=kit+churrasco&qid=1772547033&sr=8-59-spons&ufe=app_do%3Aamzn1.fos.a492fd4a-f54d-4e8d-8c31-35e0a04ce61e&sp_csd=d2lkZ2V0TmFtZT1zcF9idGY&psc=1"),
    ("Cobertor", 127.21, "https://shopee.com.br/Cobertor-Manta-Ultrasoft-Willow-Aveludada-Alto-Relevo-Coberta-Queen-2-40m-X-2-20m-i.1572699366.22194263666?extraParams=%7B%22display_model_id%22%3A228788054532%2C%22model_selection_logic%22%3A3%7D&sp_atk=daeee00e-d5a0-4c6d-ac8f-5ca77747474e&xptdk=daeee00e-d5a0-4c6d-ac8f-5ca77747474e"),
    ("Churrasqueira Elétrica", 123.90,"https://www.amazon.com.br/Churrasqueira-Elétrica-Grand-Mondial-CH-05/dp/B07CNVHCVX/ref=asc_df_B07CNVHCVX?mcid=bee223b88e9b3585b63539f97c6cb407&tag=googleshopp06-20&linkCode=df0&hvadid=709884383920&hvpos=&hvnetw=g&hvrand=8871538218815698153&hvpone=&hvptwo=&hvqmt=&hvdev=m&hvdvcmdl=&hvlocint=&hvlocphy=9100079&hvtargid=pla-812647248478&psc=1&language=pt_BR&gad_source=1"),
    ("Liquidificador", 113.05, "https://www.casasbahia.com.br/liquidificador-philco-ph900-preto"),
    ("Jogo de Lençol Cinza", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891?pp=/44.2679/&tsid=17&utm_source=pmax&utm_medium=cpc&gad_source=1&gad_campaignid=17335599522&gbraid=0AAAAADp43MZfKjJW8cUBRit48QCP7Bwv0&gclid=CjwKCAiAqprNBhB6EiwAMe3yhjIf2QhY83v7nX47m18x--_imaNPgAC1gL4S8dHRN6lt1ptIQZhw-RoC1X4QAvD_BwE"),
    ("Jogo de Lençol Linho", 115.10, "https://www.zelo.com.br/jogo-de-cama-microfibra-casal-beca-decor-p1009891?pp=/44.2875/&tsid=17&utm_source=pmax&utm_medium=cpc&gad_source=1&gad_campaignid=17335599522&gbraid=0AAAAADp43MZfKjJW8cUBRit48QCP7Bwv0&gclid=CjwKCAiAqprNBhB6EiwAMe3yhjIf2QhY83v7nX47m18x--_imaNPgAC1gL4S8dHRN6lt1ptIQZhw-RoC1X4QAvD_BwE"),
    ("Panela de Arroz", 107.91, "https://www.magazineluiza.com.br/panela-de-arroz-britania-bpa5bi-5-xicaras/p/kc02ddghb7/ep/pael/?&seller_id=britaniaoficial&utm_source=google&utm_medium=cpc&utm_term=84396&utm_campaign=google_eco_per_ven_pla_arp_apo_3p_ep-0326&utm_content=&partner_id=84396&gclsrc=aw.ds&gad_source=1&gad_campaignid=23594804622&gbraid=0AAAAAD4zZmSNcVRT6157mhiixYgA-KrrS&gclid=CjwKCAiAqprNBhB6EiwAMe3yhjncAy0kAVrqpriN6sbaP80TIM_DqWAAL7LTQm4CCpwh_WN8LJQIzhoCzzAQAvD_BwE"),
    ("Jogo de Taça", 99.90, "https://www.amazon.com.br/Cristal-Conjunto-Unidades-Brancos-Millilitros/dp/B0GK9RDPJM/ref=sr_1_1_sspa?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3AXJF8OI91WUL&dib=eyJ2IjoiMSJ9.G68zz1c6-KPQ5oPPgKYjsR9ssLwlXjaSb6OeoZw67gA8hkcvFq9Ot7X7kyS6b7jrvLEuDm0la_jCKVcI0tukcu8LPnNJoWrmplevXJ_1EYjSmvzyO1_PMGwGRl5iX0sYAPnaMyU4Ae40SMmg9L_Hpr-iIeL1uFjflIKspCl6QnMU6jRblUNPnjf5dUCP0D29I-OQZFkUvzOwlftk0zTmW219vjQojHj-DsrFA6Fl2SbX18Aoff7NgR2jo_FioksJQRf3ofhESvApaIahZCbk_ItnJYOgdGrCMLvmQGBoOeE.Ivuz4rlEoe2fgPAr2nEwwxpqM_Kghh7Fng2aKSDwgpk&dib_tag=se&keywords=ta%C3%A7a%2Bcristal&qid=1772553229&sprefix=ta%C3%A7a%2Bcrista%2Caps%2C204&sr=8-1-spons&ufe=app_do%3Aamzn1.fos.6d798eae-cadf-45de-946a-f477d47705b9&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"),
    ("Sanduicheira", 99.00, "https://www.casasbahia.com.br/sanduicheira-grill-philco-pgr25a-antiaderente-750w-luz-indicadora-preto/p/55071723?utm_source=GP_PLA&utm_medium=Cpc&utm_campaign=cb_mkp_gg_shopping_sellers_acima16"),
    ("Escorredor de Louça", 83.35, "https://www.amazon.com.br/Escorredor-Loucas-Flat-Coza-Light/dp/B07NMML18T/ref=asc_df_B07NGJM9K5?mcid=35ca01e1f54e357e9dac1a7102b34af3&tag=googleshopp00-20&linkCode=df0&hvadid=709864975911&hvpos=&hvnetw=g&hvrand=6979147431379274457&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9222019&hvtargid=pla-883314005477&language=pt_BR&gad_source=1&th=1"),
    ("Mixer", 84.90, "https://www.amazon.com.br/Mixer-Brit%C3%A2nia-BMX350P-Preto-127V/dp/B097KP1641/ref=sr_1_6?dib=eyJ2IjoiMSJ9.1yTmxoHvZC9-Phj3dnNmjy1rEdACoA7Wn7Dd2Ip6Z4Pmj1b1G_j3pb57adRISFPqF_AtHiJpqY6fa44husEbRG2HsN7ioQ7R-0IjbSHK8KXwve9TeOyxqcksZczX76cRL6t8DLfnDljQ1yzLaRSUXWQ_RhGm-bHagF6xWdOOK9gYasvpFG_mukh5g-maYZ-ugRMUkewsQhYZ0oOtKnAshGbNL38_HC_HXTAupWCG9twtS6Pxu6GsQV2EduNQ68PzFWVJLr4Qdet22aORKfDvuTX1EbjAfi4YXK5Da1DM99k.THzZwy-M2fTC3O01He3huCEQPIp2hkkaNZ6gpG0Xx0U&dib_tag=se&keywords=mixer+britania&qid=1772553904&sr=8-6"),
    ("Potes Organizadores", 65.33, "https://www.amazon.com.br/Potes-Herm%C3%A9ticos-Mantimentos-Transparente-Unidades/dp/B0DMMFHYPM/ref=asc_df_B0DMMFHYPM?mcid=038483f8864636da8d69d3c0b7197c09&tag=googleshopp00-20&linkCode=df0&hvadid=709989056369&hvpos=&hvnetw=g&hvrand=943135354086922394&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9222019&hvtargid=pla-2385322973416&language=pt_BR&gad_source=1&th=1"),
    ("Kit 3 Escorredor de Macarrão", 59.90, "https://www.amazon.com.br/Escorredor-Macarr%C3%A3o-Alimentos-Vegetais-Multiuso/dp/B0DCPDZH2N/ref=asc_df_B0DCPDZH2N?mcid=7b31720451f83389b2a6e761d9008265&tag=googleshopp00-20&linkCode=df0&hvadid=709876289439&hvpos=&hvnetw=g&hvrand=706584530222083164&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9197118&hvtargid=pla-2364536886640&psc=1&language=pt_BR&gad_source=1"),
    ("Kit Pote Tempero", 49.00, "https://www.amazon.com.br/Oikos-Potes-Vidro-Herm%C3%A9ticos-Redondos/dp/B0BFC5HJY8/ref=sr_1_3?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=18K0F2GA0HPPT&dib=eyJ2IjoiMSJ9.-rI4o4mlzj2i4JMLSyaHBAwFjorIV0pjncE8TFvW4pnmR4UC7IPYQgLemIgxFhPh6nmIgVEzBJxXU_ar_IYxuO7j44tUiQiHnWPlextrNUTer9A_CL5sSAn1ESq2I-RDzmqLuWp4dwWgEXoC2-enX3hgEE4GjJjVm8I_lK39ILFlaKm_WMZxDCk6eOuUWBY4CEtF_VztvoEIAvBQ8sCsLTnAYEjHxOZq49UXwV812y0.aVpj-YR1aM3hvGZJUcIFknaIXnGE-HZBrWwQjyvYqec&dib_tag=se&keywords=kit%2Bherm%C3%A9tico%2B200%2Bml&qid=1772554017&s=kitchen&sprefix=kit%2Bh%2Bermeticos%2B200%2Bml%2Ckitchen%2C269&sr=1-3&th=1"),
    ("Jogo Travessa", 56.00, "https://produto.mercadolivre.com.br/MLB-4361321319-kit-3-travessa-vidro-retangular-com-alca-opaline-branco-1l-_JM?matt_tool=48995110&matt_internal_campaign_id=&matt_word=&matt_source=google&matt_campaign_id=22603531562&matt_ad_group_id=181244933895&matt_match_type=&matt_network=g&matt_device=c&matt_creative=758138322200&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=562635765&matt_product_id=MLB4361321319&matt_product_partition_id=2424443211326&matt_target_id=aud-1966490908987:pla-2424443211326&cq_src=google_ads&cq_cmp=22603531562&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=4&gad_campaignid=22603531562&gbraid=0AAAAAD93qcBQ9Rv0bi0tBs42YI50REDDZ&gclid=CjwKCAiAqprNBhB6EiwAMe3yhnepP23Mn7id7xgN_1JI9SuVvU1Iud2mLNns5T33DWMJJevaEGZmNxoCMPAQAvD_BwE"),        
    ("Nicho de Parede Sobrepor", 54.00, "https://www.amazon.com.br/Sobrepor-28cmx40cm-Arquitech-Lavanderia-Instala%C3%A7%C3%A3o/dp/B0FX19V4WN/ref=sr_1_6?dib=eyJ2IjoiMSJ9.AJ_uRYcLPh4wzxbW3sLF-6HWDrjnaYJ2g0WwVbaqAarP2aLgouOF59cRSeNRrRCITZuZozJpxaQrfV-jpYEb2p4B3xwNANxEJjh6USdwRKK1LNXlJOVz0-1an1BYlw1x8TpeEGZdDn6NmJP5-YpESYYqWm0x6Xq-oyXegjil0i4D6owKBGA1_qgBzS0uRFql9pz5WFfajNhF1Gchvzgq1gipGwu0SYVemkRV6mSBPlZm_D0B5-sAERgnpn3Hum2V7HJF9EidBA6BCHvS7ihMgiVhBtqagoPbYeJ3nvF23MU.H75iG4hoNqKS9pROsZ5xSmpPnaviIMNdH0iiQelrEYw&dib_tag=se&keywords=nicho+parede&qid=1772554066&sr=8-6&ufe=app_do%3Aamzn1.fos.6d798eae-cadf-45de-946a-f477d47705b9"),
    ("Kit Utensílios Inox de Cozinha", 64.50, "https://www.mercadolivre.com.br/7-utensilios-inox-amassador-ralador-descascador-peneira/up/MLBU3211590549?pdp_filters=item_id%3AMLB5413764608&from=gshop&matt_tool=48995110&matt_internal_campaign_id=&matt_word=&matt_source=google&matt_campaign_id=22603531562&matt_ad_group_id=181244933895&matt_match_type=&matt_network=g&matt_device=c&matt_creative=758138322200&matt_keyword=&matt_ad_position=&matt_ad_type=pla&matt_merchant_id=5584773650&matt_product_id=MLBU3211590549&matt_product_partition_id=2424443219726&matt_target_id=aud-1966490908987:pla-2424443219726&cq_src=google_ads&cq_cmp=22603531562&cq_net=g&cq_plt=gp&cq_med=pla&gad_source=1&gad_campaignid=22603531562&gbraid=0AAAAAD93qcC_PXRMjPxHv0UkN6BEjHNAe&gclid=CjwKCAiAqprNBhB6EiwAMe3yhs2zlCiSX_XPeaDYzLWb3IpjNU29IkaFuvB_R16wKeio2WE0nZqxhRoCp68QAvD_BwE"),
    ("Jarra de vidro", 49.92, "https://www.amazon.com.br/Diamond-Jarra-Sodo-C%C3%A1lcico-Transparente-Dourado/dp/B08X1NZPYH/ref=asc_df_B08X1NZPYH?mcid=0574324181243c7ab9f042a75d4ac50e&tag=googleshopp00-20&linkCode=df0&hvadid=709964506238&hvpos=&hvnetw=g&hvrand=9168573640763778955&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9222019&hvtargid=pla-1596728074940&language=pt_BR&gad_source=1&th=1"),
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
