import streamlit as st
from PIL import Image
import pytesseract
import re
import pandas as pd

st.set_page_config(page_title="DOMMA SaaS", layout="wide")

st.title("🧠 DOMMA SaaS - Inteligência Completa")

# =========================
# OCR
# =========================
def extrair_texto(imagem):
    try:
        return pytesseract.image_to_string(imagem)
    except:
        return ""

# =========================
# EXTRAIR NÚMEROS
# =========================
def extrair_numero(texto, padrao):
    match = re.search(padrao, texto)
    if match:
        return float(match.group(1).replace(".", "").replace(",", "."))
    return 0

# =========================
# LEITURA DE PRINT
# =========================
def analisar_print(img):
    texto = extrair_texto(img)

    dados = {
        "vendas": extrair_numero(texto, r"R\$ ([\d\.,]+)"),
        "cliques": extrair_numero(texto, r"(\d+)\s+cliques"),
        "visitas": extrair_numero(texto, r"(\d+)\s+visitas"),
    }

    return dados

# =========================
# 📸 PRINTS
# =========================
st.subheader("📸 Upload de Prints")

col1, col2, col3 = st.columns(3)

with col1:
    m30 = st.file_uploader("Métricas 30 dias", type=["png","jpg"])
    m15 = st.file_uploader("Métricas 15 dias", type=["png","jpg"])
    m7 = st.file_uploader("Métricas 7 dias", type=["png","jpg"])

with col2:
    p30 = st.file_uploader("Painel Ads 30 dias", type=["png","jpg"])
    p15 = st.file_uploader("Painel Ads 15 dias", type=["png","jpg"])
    p7 = st.file_uploader("Painel Ads 7 dias", type=["png","jpg"])

with col3:
    camp = st.file_uploader("Campanhas", type=["png","jpg"])

st.divider()

# =========================
# 📊 INPUT MANUAL
# =========================
st.subheader("📊 Dados para análise")

imp = st.number_input("Impressões 7 dias", 0.0)
clk = st.number_input("Cliques 7 dias", 0.0)
ven = st.number_input("Vendas 7 dias", 0.0)
cus = st.number_input("Custo 7 dias", 0.0)
fat = st.number_input("Faturamento 7 dias", 0.0)

# =========================
# CALCULO
# =========================
def calc():
    ctr = clk / imp if imp > 0 else 0
    roas = fat / cus if cus > 0 else 0
    acos = cus / fat if fat > 0 else 0
    return ctr, roas, acos

ctr, roas, acos = calc()

# =========================
# ANALISE DOS PRINTS
# =========================
st.subheader("🧠 Leitura dos Prints")

dados_print = []

if m7:
    dados_print.append(analisar_print(Image.open(m7)))

if p7:
    dados_print.append(analisar_print(Image.open(p7)))

# =========================
# INTERPRETAÇÃO
# =========================
st.subheader("🧠 Diagnóstico DOMMA")

# comportamento
if ctr < 0.01:
    st.warning("CTR baixo → problema de imagem")

if clk > 20 and ven == 0:
    st.error("Clique sem venda → problema de conversão")

if roas < 3:
    st.error("ROAS baixo → operação ruim")

if acos > 0.08:
    st.error("ACOS alto → custo elevado")

if cus > 0 and ven == 0:
    st.error("Campanha queimando dinheiro")

# tendência básica
st.subheader("📈 Leitura Estratégica")

if roas > 6:
    st.success("Escala saudável")
elif roas < 3:
    st.error("Operação em risco")
else:
    st.warning("Operação em ajuste")

# =========================
# CAMPANHAS
# =========================
st.subheader("📂 Campanhas")

file = st.file_uploader("CSV campanhas", type=["csv"])

if file:
    df = pd.read_csv(file)

    def avaliar(row):
        roas = row["faturamento"] / row["custo"] if row["custo"] > 0 else 0

        if roas > 6:
            return "ESCALAR"
        elif roas < 3:
            return "PAUSAR"
        else:
            return "AJUSTAR"

    df["AÇÃO"] = df.apply(avaliar, axis=1)

    st.dataframe(df)

    st.subheader("🎯 Ajustes necessários")
    st.dataframe(df[df["AÇÃO"] != "ESCALAR"])

# =========================
# PLANO DE AÇÃO
# =========================
st.subheader("🚀 Plano DOMMA")

if st.button("Gerar Estratégia"):

    plano = []

    if ctr < 0.01:
        plano.append("Melhorar capa do anúncio")

    if ven == 0 and clk > 20:
        plano.append("Revisar oferta e preço")

    if roas < 3:
        plano.append("Pausar campanhas ruins")

    if roas > 6:
        plano.append("Escalar orçamento")

    if acos > 0.08:
        plano.append("Reduzir custo ou melhorar conversão")

    if not plano:
        plano.append("Manter operação")

    for p in plano:
        st.write("✅", p)
