import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

st.set_page_config(page_title="DOMMA SaaS", layout="wide")

st.title("🧠 DOMMA SaaS - Inteligência de Ads")

# =========================
# FUNÇÃO OCR (SEGURA NA NUVEM)
# =========================
def extrair_texto(imagem):
    try:
        import pytesseract
        return pytesseract.image_to_string(imagem)
    except:
        return "OCR não disponível na nuvem"

# =========================
# 📸 UPLOAD DE PRINTS (ESTRUTURA PROFISSIONAL)
# =========================
st.subheader("📸 Upload de Prints - Análise Completa")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Métricas")
    metrica_30 = st.file_uploader("Métricas 30 dias", type=["png","jpg"], key="m30")
    metrica_15 = st.file_uploader("Métricas 15 dias", type=["png","jpg"], key="m15")
    metrica_7 = st.file_uploader("Métricas 7 dias", type=["png","jpg"], key="m7")

with col2:
    st.markdown("### 📈 Painel Ads")
    painel_30 = st.file_uploader("Painel Ads 30 dias", type=["png","jpg"], key="p30")
    painel_15 = st.file_uploader("Painel Ads 15 dias", type=["png","jpg"], key="p15")
    painel_7 = st.file_uploader("Painel Ads 7 dias", type=["png","jpg"], key="p7")

with col3:
    st.markdown("### 🧩 Campanhas")
    campanhas_img = st.file_uploader("Imagem geral das campanhas", type=["png","jpg"], key="camp")

st.divider()

# =========================
# 🖼️ VISUALIZAÇÃO
# =========================
st.subheader("🖼️ Visualização dos Prints")

colA, colB, colC = st.columns(3)

with colA:
    if metrica_30:
        st.image(metrica_30, caption="Métricas 30 dias", use_container_width=True)
    if metrica_15:
        st.image(metrica_15, caption="Métricas 15 dias", use_container_width=True)
    if metrica_7:
        st.image(metrica_7, caption="Métricas 7 dias", use_container_width=True)

with colB:
    if painel_30:
        st.image(painel_30, caption="Painel 30 dias", use_container_width=True)
    if painel_15:
        st.image(painel_15, caption="Painel 15 dias", use_container_width=True)
    if painel_7:
        st.image(painel_7, caption="Painel 7 dias", use_container_width=True)

with colC:
    if campanhas_img:
        st.image(campanhas_img, caption="Campanhas", use_container_width=True)

# =========================
# 🧠 OCR (LEITURA DO PRINT 7 DIAS)
# =========================
st.subheader("🧠 Leitura Inteligente (OCR)")

if metrica_7:
    imagem = Image.open(metrica_7)
    texto = extrair_texto(imagem)
    st.code(texto)

# =========================
# 📊 INPUT MANUAL (CASO NÃO USE OCR)
# =========================
st.sidebar.header("📊 Métricas da Campanha")

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
# 🚨 ALERTA
# =========================
st.subheader("🚨 Status da Campanha")

if cus > 50 and ven == 0:
    st.error("🚨 Campanha queimando dinheiro!")
elif tacos > 0.08:
    st.warning("⚠️ TACOS alto — atenção")
else:
    st.success("✅ Campanha saudável")

# =========================
# 📊 CLASSIFICAÇÃO DOMMA
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
# 🧠 DIAGNÓSTICO
# =========================
def diagnostico():
    if imp > 0 and clk == 0:
        return "Problema de atração (imagem/título)"
    elif clk > 10 and ven == 0:
        return "Problema de conversão"
    elif roas > 6:
        return "Anúncio pronto para escalar"
    else:
        return "Em otimização"

st.subheader("🧠 Diagnóstico")
st.write(diagnostico())

# =========================
# 📈 GRÁFICO
# =========================
df = pd.DataFrame({
    "Métrica": ["CTR", "ROAS", "TACOS"],
    "Valor": [ctr, roas, tacos]
})

fig = px.bar(df, x="Métrica", y="Valor")
st.plotly_chart(fig, use_container_width=True)

# =========================
# 🚀 PLANO DE AÇÃO
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
