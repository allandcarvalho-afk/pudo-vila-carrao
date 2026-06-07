import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Plano de Negócio — PUDO Vila Carrão",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .metric-card {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .positive { color: #28a745; font-weight: bold; }
    .negative { color: #dc3545; font-weight: bold; }
    .neutral  { color: #007bff; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Parâmetros do Negócio")

    st.subheader("📍 Localização")
    bairro = st.text_input("Bairro", "Vila Carrão — Zona Leste SP")

    # ── CAPEX
    st.subheader("💰 Investimento Inicial (CAPEX)")
    capex_reforma     = st.number_input("Reforma / adequação (R$)", 0, 200000, 10000, step=500)
    capex_moveis      = st.number_input("Móveis / prateleiras / balcão (R$)", 0, 50000, 4000, step=500)
    capex_ti          = st.number_input("Equipamentos TI (R$)", 0, 30000, 5000, step=500)
    capex_seguranca   = st.number_input("Câmeras + alarme (R$)", 0, 20000, 2500, step=500)
    capex_arcond      = st.number_input("Ar-condicionado (R$)", 0, 15000, 3500, step=500)
    capex_estoque_p   = st.number_input("Estoque inicial — Pesca (R$)", 0, 100000, 8000, step=500)
    capex_estoque_b   = st.number_input("Estoque inicial — Beleza (R$)", 0, 100000, 5000, step=500)
    capex_abertura    = st.number_input("Abertura empresa / contador (R$)", 0, 10000, 1500, step=100)
    capex_marketing   = st.number_input("Marketing inicial (R$)", 0, 20000, 2000, step=500)
    meses_capital_giro = st.slider("Meses de capital de giro reservados", 1, 6, 3)

    # ── OPEX FIXO
    st.subheader("🔄 Custos Fixos Mensais (OPEX)")
    aluguel           = st.number_input("Aluguel (R$)", 0, 30000, 3500, step=100)
    condominio        = st.number_input("Condomínio + IPTU (R$)", 0, 5000, 300, step=50)
    energia           = st.number_input("Energia elétrica (R$)", 0, 5000, 400, step=50)
    internet          = st.number_input("Internet (R$)", 0, 1000, 180, step=10)
    telefone          = st.number_input("Telefone / celular (R$)", 0, 500, 120, step=10)
    pessoal           = st.number_input("Pessoal — salários brutos (R$)", 0, 20000, 2200, step=100)
    encargos_pct      = st.slider("Encargos trabalhistas (%)", 0, 100, 70)
    contador          = st.number_input("Contador (R$)", 0, 3000, 450, step=50)
    sistema           = st.number_input("Sistema ERP / PDV (R$)", 0, 2000, 200, step=10)
    embalagens        = st.number_input("Embalagens e suprimentos (R$)", 0, 5000, 400, step=50)
    marketing_mensal  = st.number_input("Marketing mensal / ADS (R$)", 0, 10000, 500, step=50)
    seguros           = st.number_input("Seguros (R$)", 0, 2000, 200, step=50)
    taxas_banco       = st.number_input("Taxas bancárias / maquininha (R$)", 0, 2000, 200, step=50)

    # ── RECEITAS
    st.subheader("📈 Projeção de Receita")

    st.markdown("**PUDO — Retiradas**")
    pudo_vol_m6       = st.number_input("Pacotes PUDO/mês (mês 6)", 0, 5000, 400, step=10)
    pudo_ticket       = st.number_input("Comissão por pacote (R$)", 0.0, 20.0, 3.5, step=0.5)

    st.markdown("**Logística Reversa**")
    reversa_vol_m6    = st.number_input("Devoluções/mês (mês 6)", 0, 2000, 80, step=10)
    reversa_ticket    = st.number_input("Comissão por devolução (R$)", 0.0, 30.0, 8.0, step=0.5)

    st.markdown("**Venda Pesca**")
    pesca_itens_m6    = st.number_input("Itens pesca/mês (mês 6)", 0, 1000, 60, step=5)
    pesca_ticket_med  = st.number_input("Ticket médio pesca (R$)", 0.0, 1000.0, 180.0, step=10.0)
    pesca_margem      = st.slider("Margem bruta pesca (%)", 0, 100, 50)

    st.markdown("**Venda Beleza**")
    beleza_itens_m6   = st.number_input("Itens beleza/mês (mês 6)", 0, 1000, 80, step=5)
    beleza_ticket_med = st.number_input("Ticket médio beleza (R$)", 0.0, 500.0, 90.0, step=10.0)
    beleza_margem     = st.slider("Margem bruta beleza (%)", 0, 100, 55)

    st.markdown("**Fulfilment (vendedores locais)**")
    full_pedidos_m6   = st.number_input("Pedidos fulfilment/mês (mês 6)", 0, 2000, 50, step=5)
    full_ticket       = st.number_input("Receita por pedido (R$)", 0.0, 50.0, 12.0, step=1.0)

    st.markdown("**Impostos**")
    aliquota_simples  = st.slider("Alíquota Simples Nacional (%)", 0.0, 20.0, 6.0, step=0.5)

    st.markdown("**Crescimento**")
    crescimento_pct   = st.slider("Crescimento mensal (meses 1→6, %)", 0, 50, 20)

# ── CÁLCULOS ────────────────────────────────────────────────────────────────────

encargos_val = pessoal * encargos_pct / 100

opex_fixo = (aluguel + condominio + energia + internet + telefone +
             pessoal + encargos_val + contador + sistema +
             embalagens + marketing_mensal + seguros + taxas_banco)

capex_total = (capex_reforma + capex_moveis + capex_ti + capex_seguranca +
               capex_arcond + capex_estoque_p + capex_estoque_b +
               capex_abertura + capex_marketing +
               opex_fixo * meses_capital_giro)

# Receita base mês 6
receita_pudo_m6     = pudo_vol_m6    * pudo_ticket
receita_reversa_m6  = reversa_vol_m6 * reversa_ticket
receita_pesca_m6    = pesca_itens_m6 * pesca_ticket_med * (pesca_margem / 100)
receita_beleza_m6   = beleza_itens_m6 * beleza_ticket_med * (beleza_margem / 100)
receita_full_m6     = full_pedidos_m6 * full_ticket
receita_total_m6    = (receita_pudo_m6 + receita_reversa_m6 +
                       receita_pesca_m6 + receita_beleza_m6 + receita_full_m6)

# Projeção 12 meses (ramp-up exponencial até mês 6, estável depois)
meses = list(range(1, 13))
receitas, custos_totais, resultados, saldos_acum = [], [], [], []
saldo_acumulado = -capex_total

for m in meses:
    fator = (crescimento_pct / 100 + 1) ** (m - 6) if m < 6 else 1.0
    fator = max(fator, 0.1)

    rec_m = receita_total_m6 * fator
    imposto_m = rec_m * aliquota_simples / 100

    # CMV estimado (custo do produto = 1 - margem) para itens de venda
    gmv_pesca   = pesca_itens_m6   * pesca_ticket_med   * fator
    gmv_beleza  = beleza_itens_m6  * beleza_ticket_med  * fator
    cmv_m = (gmv_pesca * (1 - pesca_margem / 100) +
             gmv_beleza * (1 - beleza_margem / 100))

    custo_m = opex_fixo + imposto_m + cmv_m
    resultado_m = rec_m - custo_m

    receitas.append(rec_m)
    custos_totais.append(custo_m)
    resultados.append(resultado_m)
    saldo_acumulado += resultado_m
    saldos_acum.append(saldo_acumulado)

df = pd.DataFrame({
    "Mês": [f"M{m}" for m in meses],
    "Receita": receitas,
    "Custo Total": custos_totais,
    "Resultado": resultados,
    "Saldo Acumulado": saldos_acum,
})

break_even_mes = next((i + 1 for i, s in enumerate(saldos_acum) if s >= 0), None)
receita_be = opex_fixo / (1 - aliquota_simples / 100) if aliquota_simples < 100 else None

# ── LAYOUT PRINCIPAL ────────────────────────────────────────────────────────────
st.title("📦 Plano de Negócio — PUDO + Logística Reversa + Loja")
st.caption(f"📍 {bairro}")

# ── ROW 1: KPIs topo
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💸 Investimento Total", f"R$ {capex_total:,.0f}".replace(",", "."))
c2.metric("📆 OPEX Fixo/mês", f"R$ {opex_fixo:,.0f}".replace(",", "."))
c3.metric("📈 Receita Mês 6", f"R$ {receita_total_m6:,.0f}".replace(",", "."))
resultado_m6 = receitas[5] - custos_totais[5]
delta_str = f"R$ {resultado_m6:+,.0f}".replace(",", ".")
c4.metric("💰 Resultado Mês 6", delta_str, delta=delta_str)
c5.metric("🎯 Break-even", f"Mês {break_even_mes}" if break_even_mes else "Após 12m")

st.divider()

# ── ROW 2: Gráfico de fluxo de caixa + composição receita
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Fluxo de Caixa — 12 Meses")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df["Mês"], y=df["Receita"], name="Receita",
        marker_color="#2196F3", opacity=0.8
    ), secondary_y=False)
    fig.add_trace(go.Bar(
        x=df["Mês"], y=df["Custo Total"], name="Custo Total",
        marker_color="#F44336", opacity=0.8
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df["Mês"], y=df["Saldo Acumulado"], name="Saldo Acumulado",
        line=dict(color="#4CAF50", width=3), mode="lines+markers"
    ), secondary_y=True)
    fig.add_hline(y=0, line_dash="dot", line_color="gray", secondary_y=True)
    fig.update_layout(
        barmode="group", height=380, legend=dict(orientation="h", y=-0.2),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    fig.update_yaxes(title_text="R$/mês", secondary_y=False)
    fig.update_yaxes(title_text="Saldo acumulado (R$)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🥧 Composição da Receita (Mês 6)")
    labels = ["PUDO", "Log. Reversa", "Pesca", "Beleza", "Fulfilment"]
    values = [receita_pudo_m6, receita_reversa_m6, receita_pesca_m6,
              receita_beleza_m6, receita_full_m6]
    fig2 = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.4,
        marker_colors=["#2196F3", "#9C27B0", "#4CAF50", "#FF9800", "#00BCD4"]
    ))
    fig2.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0),
                       legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── ROW 3: Tabela + CAPEX breakdown
col_tab, col_capex = st.columns([2, 1])

with col_tab:
    st.subheader("📋 Projeção Mensal Detalhada")
    df_display = df.copy()
    for col in ["Receita", "Custo Total", "Resultado", "Saldo Acumulado"]:
        df_display[col] = df_display[col].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))

    def color_resultado(val):
        try:
            v = float(val.replace("R$ ", "").replace(".", "").replace(",", "."))
            return "color: green" if v >= 0 else "color: red"
        except Exception:
            return ""

    st.dataframe(
        df_display.style.map(color_resultado, subset=["Resultado", "Saldo Acumulado"]),
        use_container_width=True, hide_index=True
    )

with col_capex:
    st.subheader("💡 Breakdown CAPEX")
    capex_items = {
        "Reforma": capex_reforma,
        "Móveis": capex_moveis,
        "TI": capex_ti,
        "Segurança": capex_seguranca,
        "Ar-cond.": capex_arcond,
        "Est. Pesca": capex_estoque_p,
        "Est. Beleza": capex_estoque_b,
        "Empresa": capex_abertura,
        "Marketing": capex_marketing,
        "Capital Giro": opex_fixo * meses_capital_giro,
    }
    capex_items = {k: v for k, v in capex_items.items() if v > 0}
    fig3 = px.bar(
        x=list(capex_items.values()),
        y=list(capex_items.keys()),
        orientation="h",
        color=list(capex_items.values()),
        color_continuous_scale="Blues",
    )
    fig3.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0),
                       showlegend=False, coloraxis_showscale=False)
    fig3.update_xaxes(tickprefix="R$ ")
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── ROW 4: Indicadores de saúde
st.subheader("🩺 Indicadores de Saúde do Negócio")

ia, ib, ic, id_ = st.columns(4)

margem_contrib_m6 = ((receitas[5] - custos_totais[5]) / receitas[5] * 100) if receitas[5] > 0 else 0
payback = abs(capex_total) / max(receitas[5] - custos_totais[5], 1)
roi_12 = (sum(resultados) / capex_total * 100) if capex_total > 0 else 0

ia.metric("Margem Contribuição (M6)", f"{margem_contrib_m6:.1f}%")
ib.metric("Payback estimado", f"{payback:.1f} meses")
ic.metric("ROI 12 meses", f"{roi_12:.1f}%")
id_.metric("Break-even mensal (R$)", f"R$ {receita_be:,.0f}".replace(",", ".") if receita_be else "N/A")

st.divider()

# ── ROW 5: Links rápidos
st.subheader("🔗 Links Essenciais por Categoria")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**📦 Credenciamento PUDO**")
    links_pudo = {
        "Correios Agente": "https://www.correios.com.br/solucoes-empresariais/agentes-correios",
        "Jadlog Pickup": "https://www.jadlog.com.br/jadlog/pickup",
        "Pegaki": "https://www.pegaki.com.br/seja-um-ponto",
        "Shopee Drops": "https://shopee.com.br/m/shopee-drops",
        "Total Express": "https://www.totalexpress.com.br/seja-parceiro",
        "Mercado Envios": "https://www.mercadolivre.com.br/agencias",
    }
    for nome, url in links_pudo.items():
        st.markdown(f"[{nome}]({url})")

with col2:
    st.markdown("**🛒 Marketplaces — Seller**")
    links_mkp = {
        "Mercado Livre Seller": "https://www.mercadolivre.com.br/vendedor",
        "Shopee Seller Center": "https://seller.shopee.com.br",
        "Amazon Seller Central": "https://sellercentral.amazon.com.br",
        "Americanas Mkt": "https://marketplace.americanas.com.br",
        "Magalu Mkt": "https://marketplace.magalu.com.br",
        "Melhor Envio": "https://www.melhorenvio.com.br",
    }
    for nome, url in links_mkp.items():
        st.markdown(f"[{nome}]({url})")

with col3:
    st.markdown("**📊 Pesquisa e Dados**")
    links_dados = {
        "IBGE SP": "https://cidades.ibge.gov.br/brasil/sp/sao-paulo/panorama",
        "ABComm": "https://www.abcomm.org.br",
        "ABIHPEC (Beleza)": "https://www.abihpec.org.br/publicacao/panorama-do-setor/",
        "Sebrae SP": "https://www.sp.sebrae.com.br",
        "GeoSampa SP": "https://geosampa.prefeitura.sp.gov.br",
        "Seade SP": "https://www.seade.gov.br",
    }
    for nome, url in links_dados.items():
        st.markdown(f"[{nome}]({url})")

with col4:
    st.markdown("**🏛️ Regulação e Abertura**")
    links_reg = {
        "Portal Empreendedor": "https://www.gov.br/empresas-e-negocios/pt-br/empreendedor",
        "JUCESP": "https://www.jucesp.sp.gov.br",
        "Alvará SP": "https://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos",
        "ANVISA Cosméticos": "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/cosmeticos",
        "Simples Nacional": "https://www8.receita.fazenda.gov.br/SimplesNacional",
        "MPA Pesca": "https://www.gov.br/agricultura/pt-br/assuntos/aquicultura-e-pesca",
    }
    for nome, url in links_reg.items():
        st.markdown(f"[{nome}]({url})")

st.divider()
st.caption("📦 PUDO Vila Carrão — Simulador de Plano de Negócio v1.0 | Dados estimados para fins de planejamento.")
