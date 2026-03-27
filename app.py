import streamlit as st
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="DOMMA SaaS", layout="wide")

st.title("🧠 DOMMA SaaS - Inteligência Automática")

# =========================
# OCR
# =========================
def extrair_texto(imagem):
    try:
        return pytesseract.image_to_string(imagem)
    except:
        return ""

# =========================
# EXTRAÇÃO DE DADOS
# =========================
def extrair_numero(texto, padrao):
    match = re.search(padrao, texto)
    if match:
        return float(match.group(1).replace(".", "").replace(",", "."))
    return 0

def analisar_texto(texto):
    dados = {}

    dados["vendas"] = extrair_numero(texto, r"R\$ ([\d\.,]+)")
    dados["cliques"] = extrair_numero(texto, r"(\d+)\s+cliques")
    dados["visitas"] = extrair_numero(texto, r"(\d+)\s+visitas")

    return dados

# =========================
# PRINTS
# =========================
st.subheader("📸 Upload dos Prints")

metrica_7 = st.file_uploader("Métricas 7 dias", type=["png","jpg"])

if metrica_7:
    imagem = Image.open(metrica_7)
    st.image(imagem, caption="Print carregado")

    texto = extrair_texto(imagem)

    # =========================
    # INTERPRETAÇÃO
    # =========================
    dados = analisar_texto(texto)

    st.subheader("🧠 Análise DOMMA Automática")

    # Diagnóstico inteligente
    if dados["cliques"] > 50 and dados["vendas"] == 0:
        st.error("🚨 Muito clique sem venda → problema de conversão")

    if dados["visitas"] > 1000:
        st.warning("⚠️ Muito tráfego → validar qualidade")

    if dados["vendas"] > 100:
        st.success("🔥 Produto validado — potencial de escala")

    # Plano de ação
    st.subheader("🚀 Plano de Ação")

    plano = []

    if dados["cliques"] > 50 and dados["vendas"] == 0:
        plano.append("Revisar preço e oferta")

    if dados["visitas"] > 1000:
        plano.append("Melhorar conversão da página")

    if dados["vendas"] > 100:
        plano.append("Escalar investimento")

    if not plano:
        plano.append("Coletar mais dados")

    for p in plano:
        st.write("✅", p)
