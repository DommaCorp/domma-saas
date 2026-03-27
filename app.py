import streamlit as st
import pandas as pd

st.set_page_config(page_title="DOMMA SaaS", layout="wide")

st.title("🧠 DOMMA SaaS - Inteligência de Ads")

# =========================
# INPUT MÉTRICAS POR PERÍODO
# =========================
st.subheader("📊 Métricas (30 / 15 / 7 dias)")

col1, col2, col3 = st.columns(3)

def bloco_input(titulo):
    st.markdown(f"### {titulo}")
    imp = st.number_input(f"Impressões {titulo}", 0.0)
    clk = st.number_input(f"Cliques {titulo}", 0.0)
    ven = st.number_input(f"Vendas {titulo}", 0.0)
    cus = st.number_input(f"Custo {titulo}", 0.0)
    fat = st.number_input(f"Faturamento {titulo}", 0.0)
    return imp, clk, ven, cus, fat

with col1:
    imp30, clk30, ven30, cus30, fat30 = bloco_input("30 dias")

with col2:
    imp15, clk15, ven15, cus15, fat15 = bloco_input("15 dias")

with col3:
    imp7, clk7, ven7, cus7, fat7 = bloco_input("7 dias")

# =========================
# FUNÇÃO DE MÉTRICAS
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
# ANÁLISE DE TENDÊNCIA
# =========================
st.subheader("📈 Leitura Inteligente")

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
# DIAGNÓSTICO INTELIGENTE
# =========================
st.subheader("🧠 Diagnóstico DOMMA")

diagnostico = []

if ctr7 < ctr15:
    diagnostico.append("Queda de CTR → problema de imagem ou título")

if clk7 > 10 and ven7 == 0:
    diagnostico.append("Cliques sem venda → problema de conversão")

if roas7 < roas15:
    diagnostico.append("ROAS caiu → tráfego menos qualificado ou oferta ruim")

if acos7 > 0.08:
    diagnostico.append("ACOS alto → você está pagando caro para vender")

if cus7 > cus15:
    diagnostico.append("Investimento aumentou → avaliar retorno")

for d in diagnostico:
    st.warning(d)

# =========================
# STATUS GERAL
# =========================
st.subheader("🚨 Status da Operação")

if roas7 > 6:
    st.success("Escala saudável")
elif roas7 < 3:
    st.error("Operação em risco")
else:
    st.warning("Operação em ajuste")

# =========================
# CAMPANHAS
# =========================
st.subheader("📂 Análise de Campanhas")

file = st.file_uploader("Upload campanhas (CSV)", type=["csv"])

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

    st.subheader("🎯 Campanhas que precisam atenção")

    ajuste = df[df["AÇÃO"] != "ESCALAR"]

    st.dataframe(ajuste)

# =========================
# PLANO DE AÇÃO INTELIGENTE
# =========================
st.subheader("🚀 Plano de Ação DOMMA")

if st.button("Gerar Plano Estratégico"):

    plano = []

    if ctr7 < ctr15:
        plano.append("Melhorar imagem principal e título")

    if ven7 == 0 and clk7 > 10:
        plano.append("Revisar oferta, preço e prova social")

    if roas7 < 3:
        plano.append("Pausar campanhas ruins e reestruturar")

    if roas7 > 6:
        plano.append("Escalar orçamento gradualmente")

    if acos7 > 0.08:
        plano.append("Reduzir investimento ou melhorar conversão")

    if cus7 > cus15:
        plano.append("Avaliar aumento de investimento vs retorno")

    if not plano:
        plano.append("Manter estratégia atual")

    for p in plano:
        st.write("✅", p)
