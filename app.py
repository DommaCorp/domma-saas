import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import pytesseract
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
texto = pytesseract.image_to_string(gray)

st.set_page_config(page_title="DOMMA SaaS", layout="wide")

st.title("🧠 DOMMA SaaS - Inteligência de Ads")

# =========================
# OCR (LEITURA DE PRINT)
# =========================
def extrair_texto(imagem):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gray)
    return texto

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📸 Upload de Prints")

img_7 = st.sidebar.file_uploader("Print 7 dias", type=["png","jpg"])

ocr_data = {}

if img_7:
    imagem = Image.open(img_7)
    st.image(imagem, caption="Print carregado", use_container_width=True)

    texto = extrair_texto(imagem)

    st.subheader("🔍 Texto identificado (OCR)")
    st.code(texto)

# =========================
# INPUT MANUAL (fallback)
# =========================
st.sidebar.header("📊 Métricas")

imp = st.sidebar.number_input("Impressões", 0.0)
clk = st.sidebar.number_input("Cliques", 0.0)
ven = st.sidebar.number_input("Vendas", 0.0)
cus = st.sidebar.number_input("Custo", 0.0)
fat = st.sidebar.number_input("Faturamento", 0.0)

# =========================
# CÁLCULOS
# =========================
def calc():
    ctr = clk / imp if imp > 0 else 0
    roas = fat / cus if cus > 0 else 0
    tacos = cus / fat if fat > 0 else 0
    return ctr, roas, tacos

ctr, roas, tacos = calc()

# =========================
# ALERTA
# =========================
st.subheader("🚨 Status da Campanha")

if cus > 50 and ven == 0:
    st.error("🚨 Campanha queimando dinheiro!")
elif tacos > 0.08:
    st.warning("⚠️ TACOS alto — atenção")
else:
    st.success("✅ Campanha saudável")

# =========================
# CLASSIFICAÇÃO DOMMA
# =========================
def classificar():
    if roas > 6 and tacos < 0.03:
        return "ESCALAR"
    elif roas < 3 or tacos > 0.08:
        return "PAUSAR"
    else:
        return "OTIMIZAR"

status = classificar()

st.subheader("📊 Classificação DOMMA")
st.info(status)

# =========================
# DIAGNÓSTICO
# =========================
def diagnostico():
    if imp > 0 and clk == 0:
        return "Problema de imagem (baixa atração)"
    elif clk > 10 and ven == 0:
        return "Problema de conversão"
    elif roas > 6:
        return "Anúncio pronto para escalar"
    else:
        return "Em otimização"

st.subheader("🧠 Diagnóstico")
st.write(diagnostico())

# =========================
# GRÁFICO SIMPLES
# =========================
df = pd.DataFrame({
    "Métrica": ["CTR", "ROAS", "TACOS"],
    "Valor": [ctr, roas, tacos]
})

fig = px.bar(df, x="Métrica", y="Valor")
st.plotly_chart(fig, use_container_width=True)

# =========================
# CAMPANHAS (CSV)
# =========================
st.subheader("📂 Campanhas (7 dias)")

camp_file = st.file_uploader("Upload campanhas", type=["csv"])

if camp_file:
    df_camp = pd.read_csv(camp_file)

    def classificar_linha(row):
        roas = row["faturamento"] / row["custo"] if row["custo"] > 0 else 0
        tacos = row["custo"] / row["faturamento"] if row["faturamento"] > 0 else 0

        if roas > 6:
            return "ESCALAR"
        elif roas < 3:
            return "PAUSAR"
        else:
            return "OTIMIZAR"

    df_camp["STATUS"] = df_camp.apply(classificar_linha, axis=1)

    st.dataframe(df_camp, use_container_width=True)

# =========================
# PLANO DE AÇÃO
# =========================
st.subheader("🚀 Plano de Ação")

if st.button("Gerar Plano de Ação"):

    plano = []

    if clk == 0:
        plano.append("Melhorar imagem e título")
    if clk > 10 and ven == 0:
        plano.append("Revisar oferta e preço")
    if roas > 6:
        plano.append("Aumentar orçamento")
    if tacos > 0.08:
        plano.append("Reduzir investimento ou otimizar")

    if not plano:
        plano.append("Manter estratégia atual")

    for p in plano:
        st.write("✅", p)
