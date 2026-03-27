import streamlit as st
import pandas as pd

st.set_page_config(page_title="DOMMA SaaS", layout="wide")

st.title("🧠 DOMMA SaaS - Inteligência de Ads")

# =========================
# 📸 PRINTS (ESTRUTURA VISUAL)
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
# 📊 INPUT DOMMA (CÉREBRO)
# =========================
st.subheader("📊 Inserção de Dados para Análise")

col1, col2, col3 = st.columns(3)

def bloco(nome):
    st.markdown(f"### {nome}")
    imp = st.number_input(f"Impressões {nome}", 0.0)
    clk = st.number_input(f"Cliques {nome}", 0.0)
    ven = st.number_input(f"Vendas {nome}", 0.0)
    cus = st.number_input(f"Custo {nome}", 0.0)
    fat = st.number_input(f"Faturamento {nome}", 0.0)
    return imp, clk, ven, cus, fat

with col1:
    imp30, clk30, ven30, cus30, fat30 = bloco("30 dias")

with col2:
    imp15, clk15, ven15, cus15, fat15 = bloco("15 dias")

with col3:
    imp7, clk7, ven7, cus7, fat7 = bloco("7 dias")

# =========================
# CÁLCULOS
# =========================
def calc(imp, clk, cus, fat):
    ctr = clk / imp if imp > 0 else 0
    roas = fat / cus if cus > 0 else 0
    acos = cus / fat if fat > 0 else 0
    return ctr, roas, acos

ctr30, roas30, acos30 = calc(imp30, clk30, cus30, fat30)
ctr15, roas15, acos15 = calc(imp15, clk15, cus15, fat15)
ctr7, roas7, acos7 = calc(imp7, clk7, cus7, fat7)

# =========================
# 🧠 LEITURA INTELIGENTE
# =========================
st.subheader("🧠 Leitura DOMMA")

def tendencia(nome, v30, v15, v7):
    if v7 > v15 > v30:
        return f"📈 {nome} em crescimento"
    elif v7 < v15 < v30:
        return f"📉 {nome} em queda"
    else:
        return f"⚖️ {nome} estável"

st.write(tendencia("CTR", ctr30, ctr15, ctr7))
st.write(tendencia("ROAS", roas30, roas15, roas7))
st.write(tendencia("ACOS", acos30, acos15, acos7))

# =========================
# 🧠 DIAGNÓSTICO PROFUNDO
# =========================
st.subheader("🧠 Diagnóstico Estratégico")

if ctr7 < ctr15:
    st.warning("Queda de CTR → problema de imagem ou título")

if clk7 > 10 and ven7 == 0:
    st.warning("Cliques sem venda → problema de conversão")

if roas7 < roas15:
    st.warning("ROAS caiu → piora na qualidade do tráfego ou oferta")

if acos7 > 0.08:
    st.error("ACOS alto → você está pagando caro para vender")

if cus7 > cus15:
    st.warning("Investimento aumentou → validar retorno")

# =========================
# 🚨 STATUS
# =========================
st.subheader("🚨 Status da Operação")

if roas7 > 6:
    st.success("Escala saudável")
elif roas7 < 3:
    st.error("Operação em risco")
else:
    st.warning("Operação em ajuste")

# =========================
# 📂 CAMPANHAS
# =========================
st.subheader("📂 Campanhas")

file = st.file_uploader("Upload campanhas CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    def analisar(row):
        roas = row["faturamento"] / row["custo"] if row["custo"] > 0 else 0

        if roas > 6:
            return "ESCALAR"
        elif roas < 3:
            return "PAUSAR"
        else:
            return "AJUSTAR"

    df["AÇÃO"] = df.apply(analisar, axis=1)

    st.dataframe(df)

    st.subheader("🎯 Campanhas que precisam ajuste")
    st.dataframe(df[df["AÇÃO"] != "ESCALAR"])

# =========================
# 🚀 PLANO DE AÇÃO
# =========================
st.subheader("🚀 Plano de Ação DOMMA")

if st.button("Gerar Plano Estratégico"):

    plano = []

    if ctr7 < ctr15:
        plano.append("Melhorar imagem e título")

    if ven7 == 0 and clk7 > 10:
        plano.append("Revisar oferta, preço e prova social")

    if roas7 < 3:
        plano.append("Pausar campanhas ruins")

    if roas7 > 6:
        plano.append("Escalar orçamento gradualmente")

    if acos7 > 0.08:
        plano.append("Reduzir investimento ou melhorar conversão")

    if cus7 > cus15:
        plano.append("Revisar aumento de investimento")

    if not plano:
        plano.append("Manter estratégia atual")

    for p in plano:
        st.write("✅", p)
