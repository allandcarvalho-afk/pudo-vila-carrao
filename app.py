import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="PUDO Vila Carrão — Plano de Negócio",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .sebrae-header {
        background: linear-gradient(90deg, #003f88, #0066cc);
        color: white; padding: 14px 20px; border-radius: 8px;
        font-size: 18px; font-weight: bold; margin-bottom: 12px;
    }
    .sebrae-section {
        background: #f7f9fc; border-left: 4px solid #0066cc;
        padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 10px;
    }
    .sebrae-section-pesca {
        background: #f0f7f0; border-left: 4px solid #2e7d32;
        padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 10px;
    }
    .sebrae-section-beleza {
        background: #fdf0f7; border-left: 4px solid #ad1457;
        padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 10px;
    }
    .kpi-box {
        background: white; border: 1px solid #e0e0e0;
        border-radius: 10px; padding: 16px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    .kpi-value { font-size: 24px; font-weight: bold; }
    .kpi-label { font-size: 12px; color: #666; margin-top: 4px; }
    .tag {
        display: inline-block; padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: bold; margin: 2px;
    }
    .tag-green { background: #e8f5e9; color: #2e7d32; }
    .tag-pink  { background: #fce4ec; color: #ad1457; }
    .tag-blue  { background: #e3f2fd; color: #1565c0; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR — Custos Compartilhados ─────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Parâmetros Gerais")
    st.caption("Custos fixos e PUDO — compartilhados entre os dois segmentos")

    st.subheader("🏠 Ponto Fixo")
    aluguel        = st.number_input("Aluguel (R$)", 0, 30000, 3500, 100)
    condominio     = st.number_input("Condomínio + IPTU (R$)", 0, 5000, 300, 50)
    energia        = st.number_input("Energia elétrica (R$)", 0, 5000, 400, 50)
    internet       = st.number_input("Internet (R$)", 0, 1000, 180, 10)
    pessoal        = st.number_input("Pessoal — salários brutos (R$)", 0, 20000, 2200, 100)
    encargos_pct   = st.slider("Encargos trabalhistas (%)", 0, 100, 70)
    contador       = st.number_input("Contador (R$)", 0, 3000, 450, 50)
    sistema        = st.number_input("Sistema ERP/PDV (R$)", 0, 2000, 200, 10)
    embalagens     = st.number_input("Embalagens e suprimentos (R$)", 0, 5000, 400, 50)
    marketing_fixo = st.number_input("Marketing / ADS (R$)", 0, 10000, 500, 50)
    seguros        = st.number_input("Seguros (R$)", 0, 2000, 200, 50)
    taxas_banco    = st.number_input("Taxas bancárias (R$)", 0, 2000, 200, 50)

    st.subheader("📦 PUDO + Logística Reversa")
    pudo_vol       = st.number_input("Pacotes PUDO/mês", 0, 5000, 400, 10)
    pudo_ticket    = st.number_input("Comissão/pacote (R$)", 0.0, 20.0, 3.5, 0.5)
    reversa_vol    = st.number_input("Devoluções/mês", 0, 2000, 80, 10)
    reversa_ticket = st.number_input("Comissão/devolução (R$)", 0.0, 30.0, 8.0, 0.5)
    full_vol       = st.number_input("Pedidos fulfilment/mês", 0, 2000, 50, 5)
    full_ticket    = st.number_input("Receita/pedido fulfilment (R$)", 0.0, 50.0, 12.0, 1.0)
    aliquota       = st.slider("Alíquota Simples Nacional (%)", 0.0, 20.0, 6.0, 0.5)

# ── Cálculos Base ────────────────────────────────────────────────────────────
encargos_val   = pessoal * encargos_pct / 100
opex_fixo_base = (aluguel + condominio + energia + internet + pessoal +
                  encargos_val + contador + sistema + embalagens +
                  marketing_fixo + seguros + taxas_banco)
rec_pudo       = pudo_vol * pudo_ticket
rec_reversa    = reversa_vol * reversa_ticket
rec_full       = full_vol * full_ticket
rec_logistica  = rec_pudo + rec_reversa + rec_full

def projecao_12m(rec_produto_m6, cmv_pct, crescimento, opex_fixo, aliquota):
    receitas, custos, resultados, saldos = [], [], [], []
    saldo = 0.0
    for m in range(1, 13):
        fator = max((1 + crescimento / 100) ** (m - 6), 0.05) if m < 6 else 1.0
        rec_m    = rec_produto_m6 * fator + rec_logistica
        gmv_m    = (rec_produto_m6 * fator) / (1 - cmv_pct / 100) if cmv_pct < 100 else 0
        cmv_m    = gmv_m * cmv_pct / 100
        imp_m    = rec_m * aliquota / 100
        custo_m  = opex_fixo + cmv_m + imp_m
        res_m    = rec_m - custo_m
        saldo   += res_m
        receitas.append(rec_m)
        custos.append(custo_m)
        resultados.append(res_m)
        saldos.append(saldo)
    return pd.DataFrame({
        "Mês": [f"M{i}" for i in range(1, 13)],
        "Receita": receitas, "Custo": custos,
        "Resultado": resultados, "Saldo Acumulado": saldos,
    })

def grafico_fc(df, cor):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df["Mês"], y=df["Receita"], name="Receita",
                         marker_color=cor, opacity=0.75), secondary_y=False)
    fig.add_trace(go.Bar(x=df["Mês"], y=df["Custo"], name="Custo",
                         marker_color="#ef5350", opacity=0.75), secondary_y=False)
    fig.add_trace(go.Scatter(x=df["Mês"], y=df["Saldo Acumulado"],
                             name="Saldo Acumulado", mode="lines+markers",
                             line=dict(color="#43a047", width=3)), secondary_y=True)
    fig.add_hline(y=0, line_dash="dot", line_color="gray", secondary_y=True)
    fig.update_layout(barmode="group", height=340,
                      legend=dict(orientation="h", y=-0.25),
                      margin=dict(l=0, r=0, t=10, b=0))
    fig.update_yaxes(title_text="R$/mês", secondary_y=False)
    fig.update_yaxes(title_text="Saldo acumulado (R$)", secondary_y=True)
    return fig

def tabela_fc(df):
    d = df.copy()
    for c in ["Receita", "Custo", "Resultado", "Saldo Acumulado"]:
        d[c] = d[c].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))

    def cor(val):
        try:
            v = float(val.replace("R$ ", "").replace(".", "").replace(",", "."))
            return "color: #2e7d32; font-weight:bold" if v >= 0 else "color: #c62828; font-weight:bold"
        except Exception:
            return ""

    return d.style.map(cor, subset=["Resultado", "Saldo Acumulado"])

# ── ABAS PRINCIPAIS ──────────────────────────────────────────────────────────
tab_geral, tab_pesca, tab_beleza = st.tabs([
    "📦  Visão Geral PUDO",
    "🐟  Segmento Pesca",
    "💄  Segmento Beleza",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ════════════════════════════════════════════════════════════════════════════
with tab_geral:
    st.markdown('<div class="sebrae-header">📦 PUDO Vila Carrão — Simulador Integrado</div>',
                unsafe_allow_html=True)

    with st.expander("💰 Investimento Inicial (CAPEX) — configure aqui", expanded=False):
        c1, c2, c3 = st.columns(3)
        capex_reforma   = c1.number_input("Reforma (R$)", 0, 200000, 10000, 500, key="cx_r")
        capex_moveis    = c1.number_input("Móveis/Prateleiras (R$)", 0, 50000, 4000, 500, key="cx_m")
        capex_ti        = c2.number_input("Equipamentos TI (R$)", 0, 30000, 5000, 500, key="cx_ti")
        capex_segur     = c2.number_input("Câmeras + Alarme (R$)", 0, 20000, 2500, 500, key="cx_s")
        capex_arc       = c2.number_input("Ar-condicionado (R$)", 0, 15000, 3500, 500, key="cx_ac")
        capex_ep        = c3.number_input("Estoque Pesca (R$)", 0, 100000, 8000, 500, key="cx_ep")
        capex_eb        = c3.number_input("Estoque Beleza (R$)", 0, 100000, 5000, 500, key="cx_eb")
        capex_ab        = c3.number_input("Abertura empresa (R$)", 0, 10000, 1500, 100, key="cx_ab")
        capex_mk        = c3.number_input("Marketing inicial (R$)", 0, 20000, 2000, 500, key="cx_mk")
        meses_cg        = c1.slider("Meses capital de giro", 1, 6, 3, key="cx_cg")

    capex_total = (capex_reforma + capex_moveis + capex_ti + capex_segur + capex_arc +
                   capex_ep + capex_eb + capex_ab + capex_mk + opex_fixo_base * meses_cg)

    st.subheader("📊 KPIs Consolidados")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Investimento Total", f"R$ {capex_total:,.0f}".replace(",", "."))
    k2.metric("OPEX Fixo/mês", f"R$ {opex_fixo_base:,.0f}".replace(",", "."))
    k3.metric("Receita PUDO/mês", f"R$ {rec_logistica:,.0f}".replace(",", "."))
    ponto_eq = opex_fixo_base / (1 - aliquota / 100) if aliquota < 100 else 0
    k4.metric("Ponto de Equilíbrio/mês", f"R$ {ponto_eq:,.0f}".replace(",", "."))
    gap = rec_logistica - ponto_eq
    k5.metric("Gap p/ break-even (só PUDO)", f"R$ {gap:,.0f}".replace(",", "."),
              delta=f"R$ {gap:,.0f}".replace(",", "."))

    st.divider()
    st.subheader("🔗 Links de Credenciamento PUDO")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**Transportadoras**")
        st.markdown("[Correios Agente](https://www.correios.com.br/solucoes-empresariais/agentes-correios)")
        st.markdown("[Jadlog Pickup](https://www.jadlog.com.br/jadlog/pickup)")
        st.markdown("[Pegaki](https://www.pegaki.com.br/seja-um-ponto)")
    with c2:
        st.markdown("**Marketplaces**")
        st.markdown("[Shopee Drops](https://shopee.com.br/m/shopee-drops)")
        st.markdown("[Mercado Envios](https://www.mercadolivre.com.br/agencias)")
        st.markdown("[Total Express](https://www.totalexpress.com.br/seja-parceiro)")
    with c3:
        st.markdown("**Regulação SP**")
        st.markdown("[Portal Empreendedor](https://www.gov.br/empresas-e-negocios/pt-br/empreendedor)")
        st.markdown("[JUCESP](https://www.jucesp.sp.gov.br)")
        st.markdown("[Alvará SP](https://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos)")
    with c4:
        st.markdown("**Dados de Mercado**")
        st.markdown("[ABComm](https://www.abcomm.org.br)")
        st.markdown("[IBGE SP](https://cidades.ibge.gov.br/brasil/sp/sao-paulo/panorama)")
        st.markdown("[GeoSampa](https://geosampa.prefeitura.sp.gov.br)")

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — PESCA
# ════════════════════════════════════════════════════════════════════════════
with tab_pesca:
    st.markdown('<div class="sebrae-header" style="background:linear-gradient(90deg,#1b5e20,#2e7d32)">🐟 Segmento Pesca — Plano de Negócio + Projeção Financeira</div>',
                unsafe_allow_html=True)

    plano_p, financ_p = st.tabs(["📋 Plano de Negócio (SEBRAE)", "💰 Projeção Financeira"])

    # ── Plano SEBRAE Pesca ──────────────────────────────────────────────────
    with plano_p:

        # 1. SUMÁRIO EXECUTIVO
        with st.expander("1. SUMÁRIO EXECUTIVO", expanded=True):
            st.markdown('<div class="sebrae-section-pesca">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.text_input("Nome do Negócio / Marca", "PUDO Pesca Vila Carrão", key="p_nome")
            c1.text_input("Localização", "Vila Carrão — Zona Leste SP", key="p_local")
            c2.text_input("Sócio(s)", "", key="p_socio")
            c2.text_input("CNPJ / Regime", "MEI / Simples Nacional", key="p_cnpj")
            st.text_area("Proposta de Valor (1 parágrafo)",
                "Somos o único ponto especializado em produtos de pesca na Vila Carrão, "
                "combinando atendimento consultivo presencial com conveniência de retirada "
                "de pedidos online (PUDO) e devolução de marketplace — tudo em um único endereço.",
                height=80, key="p_valor")
            st.markdown('</div>', unsafe_allow_html=True)

        # 2. DESCRIÇÃO DO NEGÓCIO
        with st.expander("2. DESCRIÇÃO DO NEGÓCIO"):
            st.markdown('<div class="sebrae-section-pesca">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.text_area("Missão",
                "Oferecer ao pescador da Zona Leste acesso a produtos de qualidade "
                "com atendimento especializado e preço justo.", height=80, key="p_missao")
            col1.text_area("Visão",
                "Ser referência em pesca esportiva na Zona Leste de São Paulo "
                "até 2027, com presença física e online consolidadas.", height=80, key="p_visao")
            col2.text_area("Valores",
                "• Paixão pelo esporte\n• Honestidade no atendimento\n"
                "• Qualidade dos produtos\n• Comprometimento com o cliente", height=80, key="p_valores")
            col2.text_area("Diferencial Competitivo",
                "• Consultoria gratuita para escolha de equipamentos\n"
                "• Ponto PUDO integrado (retirada de pedidos de qualquer loja)\n"
                "• Kits para iniciantes com orientação\n"
                "• Localização com fácil acesso e estacionamento", height=80, key="p_dif")
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. PRODUTOS E SERVIÇOS
        with st.expander("3. PRODUTOS E SERVIÇOS"):
            st.markdown('<div class="sebrae-section-pesca">', unsafe_allow_html=True)
            st.markdown("""
| Categoria | Exemplos de Produtos | Ticket Médio | Margem Estimada |
|---|---|---|---|
| Varas e molinetes | Varas 1,20m–2,40m, molinetes spinning/baitcasting | R$ 150–500 | 45–55% |
| Linhas e anzóis | Linhas monofilamento, fluorocarbono, multifilamento | R$ 20–80 | 60–70% |
| Iscas artificiais | Iscas soft, hard bait, jigs, flies | R$ 15–120 | 50–65% |
| Acessórios | Caixas de pesca, suportes, alicates, roupas UV | R$ 30–200 | 50–60% |
| Kit iniciante | Combo vara + molinete + linha + isca + caixa | R$ 120–280 | 40–50% |
| Serviços PUDO | Retirada e devolução de encomendas | R$ 3–15/pacote | 100% |
""")
            st.text_area("Produtos que pretende adicionar (preencha)",
                         "", height=60, key="p_prod_add")
            st.markdown('</div>', unsafe_allow_html=True)

        # 4. ANÁLISE DE MERCADO
        with st.expander("4. ANÁLISE DE MERCADO"):
            st.markdown('<div class="sebrae-section-pesca">', unsafe_allow_html=True)

            st.markdown("##### 4.1 Clientes-Alvo")
            st.markdown("""
| Perfil | Detalhe |
|---|---|
| **Gênero predominante** | Masculino (85%) |
| **Faixa etária** | 25–55 anos |
| **Classe social** | B2 e C1 (renda R$ 3.000–8.000/mês) |
| **Comportamento** | Compra recorrente; fiel à marca quando bem atendido |
| **Canal preferido** | Loja física para consultoria + online para reposição |
| **Frequência** | Mensal a trimestral |
| **Motivação** | Pesca esportiva / lazer nos finais de semana |
""")
            st.text_area("Observações sobre os seus clientes da região",
                         "", height=60, key="p_clientes")

            st.markdown("##### 4.2 Concorrentes")
            st.markdown("""
| Concorrente | Tipo | Distância | Ponto Fraco |
|---|---|---|---|
| Lojas de pesca Zona Leste (genéricas) | Física | 2–5 km | Pouca variedade / sem consultoria |
| Mercado Livre / Shopee | Online | — | Sem atendimento pós-venda presencial |
| Decathlon | Física | > 8 km | Foco esportes gerais, não especialista |
| Ponto de Pesca / Pesca e Cia | Online | — | Frete alto para zona leste |
""")
            st.text_area("Concorrentes identificados na sua região (preencha)",
                         "", height=60, key="p_concorrentes")

            st.markdown("##### 4.3 Fornecedores Recomendados")
            st.markdown("""
| Fornecedor | Produtos | Contato |
|---|---|---|
| **Marine Sports** | Varas, molinetes, linhas | [marinesports.com.br](https://www.marinesports.com.br) |
| **Albatroz Fishing** | Iscas, varas, acessórios | [albatrozfishing.com.br](https://www.albatrozfishing.com.br) |
| **Maruri** | Varas, molinetes | [maruri.com.br](https://www.maruri.com.br) |
| **Sufix / Rapala** | Linhas premium, iscas | Distribuidores SP |
| **Atacado pesca Brás** | Variedade geral | Pesquisar: Feira do Brás SP |
""")
            st.markdown('</div>', unsafe_allow_html=True)

        # 5. PLANO DE MARKETING — 4Ps
        with st.expander("5. PLANO DE MARKETING — 4Ps"):
            st.markdown('<div class="sebrae-section-pesca">', unsafe_allow_html=True)
            p1, p2 = st.columns(2)
            p1.markdown("**🎣 PRODUTO**")
            p1.text_area("Linha de produtos e diferenciais",
                "• Variedade focada em pesca em represa e rio (perfil SP interior)\n"
                "• Kit iniciante exclusivo com guia de uso\n"
                "• Produtos de marca + opção econômica\n"
                "• Consultoria gratuita na compra", height=120, key="p_produto")
            p1.markdown("**💰 PREÇO**")
            p1.text_area("Estratégia de preço",
                "• Preço competitivo com marketplace (até 10% abaixo)\n"
                "• Desconto para compra de kits\n"
                "• Parcelamento em até 6x sem juros (cartão)\n"
                "• Fidelidade: 5ª compra com 10% de desconto", height=120, key="p_preco")
            p2.markdown("**📍 PRAÇA (Distribuição)**")
            p2.text_area("Canais de venda",
                "• Loja física — Vila Carrão\n"
                "• Mercado Livre (anúncios prata/ouro)\n"
                "• Shopee (frete subsidiado)\n"
                "• WhatsApp Business (atendimento e pedidos)\n"
                "• Instagram Shopping", height=120, key="p_praca")
            p2.markdown("**📣 PROMOÇÃO**")
            p2.text_area("Ações de marketing",
                "• Instagram: dicas de pesca + produtos novos (3x/semana)\n"
                "• Grupos WhatsApp pescadores zona leste\n"
                "• YouTube: reviews de produtos (mensal)\n"
                "• Parcerias com clubes de pesca da região\n"
                "• Google Meu Negócio otimizado", height=120, key="p_promo")
            st.markdown('</div>', unsafe_allow_html=True)

        # 6. PLANO OPERACIONAL
        with st.expander("6. PLANO OPERACIONAL"):
            st.markdown('<div class="sebrae-section-pesca">', unsafe_allow_html=True)
            st.markdown("""
**Layout sugerido (60 m²):**
- Balcão de atendimento + caixa: 8 m²
- Exposição de produtos (prateleiras): 20 m²
- Área de estoque PUDO (encomendas): 15 m²
- Estoque de produtos: 12 m²
- Circulação: 5 m²

**Horário de funcionamento:**
- Seg–Sex: 08h00 às 19h00 | Sáb: 08h00 às 14h00

**Processos críticos:**
1. Recebimento de mercadoria → conferência → estoque → precificação
2. Venda → separação → embalagem → entrega (balcão/motoboy/PUDO)
3. Recebimento de encomendas PUDO → registro → notificação → entrega
""")
            st.text_area("Anotações operacionais (preencha)", "", height=60, key="p_op")
            st.markdown("**Links operacionais:**")
            st.markdown("[Bling ERP](https://www.bling.com.br) · [Melhor Envio](https://www.melhorenvio.com.br) · [ANVISA](https://www.gov.br/anvisa) · [MAPA Pesca](https://www.gov.br/agricultura/pt-br/assuntos/aquicultura-e-pesca)")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Projeção Financeira Pesca ────────────────────────────────────────────
    with financ_p:
        st.markdown('<div class="sebrae-section-pesca"><b>Configure os parâmetros do segmento Pesca</b></div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        p_itens   = c1.number_input("Itens pesca vendidos/mês (meta M6)", 0, 2000, 70, 5, key="pf_itens")
        p_ticket  = c1.number_input("Ticket médio pesca (R$)", 0.0, 1000.0, 180.0, 10.0, key="pf_tick")
        p_margem  = c1.slider("Margem bruta (%)", 0, 100, 50, key="pf_marg")
        p_cresc   = c2.slider("Crescimento mensal meses 1→6 (%)", 0, 60, 25, key="pf_cresc")
        p_capex_e = c2.number_input("Estoque inicial Pesca (R$)", 0, 100000, 8000, 500, key="pf_capex")
        p_capex_o = c2.number_input("Outros CAPEX Pesca (R$)", 0, 50000, 5000, 500, key="pf_capo")
        p_meses_cg = c3.slider("Meses de capital de giro", 1, 6, 3, key="pf_cg")

        rec_pesca_m6 = p_itens * p_ticket * (p_margem / 100)
        capex_pesca  = p_capex_e + p_capex_o + opex_fixo_base * p_meses_cg
        df_p = projecao_12m(rec_pesca_m6, 100 - p_margem, p_cresc, opex_fixo_base, aliquota)
        be_p = next((i + 1 for i, s in enumerate(df_p["Saldo Acumulado"]) if s >= 0), None)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("CAPEX Pesca", f"R$ {capex_pesca:,.0f}".replace(",", "."))
        k2.metric("Receita (margem) Mês 6", f"R$ {rec_pesca_m6 + rec_logistica:,.0f}".replace(",", "."))
        res6 = df_p["Resultado"].iloc[5]
        k3.metric("Resultado Mês 6", f"R$ {res6:,.0f}".replace(",", "."))
        k4.metric("Break-even (mês)", f"Mês {be_p}" if be_p else "Após 12m")

        st.plotly_chart(grafico_fc(df_p, "#2e7d32"), use_container_width=True)
        st.dataframe(tabela_fc(df_p), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("📦 Mix de Estoque Sugerido — Pesca")
        dados_mix_p = {
            "Categoria": ["Varas e molinetes", "Linhas e anzóis", "Iscas artificiais",
                          "Acessórios", "Kit iniciante"],
            "% do Estoque": [30, 15, 25, 15, 15],
            "Valor Sugerido (R$)": [
                round(p_capex_e * 0.30), round(p_capex_e * 0.15),
                round(p_capex_e * 0.25), round(p_capex_e * 0.15),
                round(p_capex_e * 0.15)
            ]
        }
        st.dataframe(pd.DataFrame(dados_mix_p), use_container_width=True, hide_index=True)
        st.markdown("**Fornecedores:** [Marine Sports](https://www.marinesports.com.br) · [Albatroz](https://www.albatrozfishing.com.br) · [Maruri](https://www.maruri.com.br)")
        st.markdown("**Venda online:** [Mercado Livre Seller](https://www.mercadolivre.com.br/vendedor) · [Shopee Seller](https://seller.shopee.com.br) · [MPA Regulação Pesca](https://www.gov.br/agricultura/pt-br/assuntos/aquicultura-e-pesca)")

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — BELEZA
# ════════════════════════════════════════════════════════════════════════════
with tab_beleza:
    st.markdown('<div class="sebrae-header" style="background:linear-gradient(90deg,#880e4f,#ad1457)">💄 Segmento Beleza — Plano de Negócio + Projeção Financeira</div>',
                unsafe_allow_html=True)

    plano_b, financ_b = st.tabs(["📋 Plano de Negócio (SEBRAE)", "💰 Projeção Financeira"])

    # ── Plano SEBRAE Beleza ─────────────────────────────────────────────────
    with plano_b:

        with st.expander("1. SUMÁRIO EXECUTIVO", expanded=True):
            st.markdown('<div class="sebrae-section-beleza">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.text_input("Nome do Negócio / Marca", "PUDO Beleza Vila Carrão", key="b_nome")
            c1.text_input("Localização", "Vila Carrão — Zona Leste SP", key="b_local")
            c2.text_input("Sócio(s)", "", key="b_socio")
            c2.text_input("CNPJ / Regime", "MEI / Simples Nacional", key="b_cnpj")
            st.text_area("Proposta de Valor",
                "Levamos a conveniência de produtos de beleza profissional e de consumo "
                "até a porta do cliente da Zona Leste, com atendimento personalizado, "
                "preços de atacado e ponto de retirada de compras online — tudo no mesmo lugar.",
                height=80, key="b_valor")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("2. DESCRIÇÃO DO NEGÓCIO"):
            st.markdown('<div class="sebrae-section-beleza">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.text_area("Missão",
                "Empoderar a mulher da Zona Leste com acesso a produtos de beleza "
                "de qualidade a preços acessíveis e atendimento que respeite seu tempo.",
                height=80, key="b_missao")
            col1.text_area("Visão",
                "Ser a loja de beleza de referência na Vila Carrão até 2027, "
                "reconhecida pela variedade, confiança e preço justo.",
                height=80, key="b_visao")
            col2.text_area("Valores",
                "• Inclusão e diversidade\n• Transparência nos ingredientes\n"
                "• Sustentabilidade (produtos veganos e cruelty-free)\n"
                "• Atendimento humanizado", height=80, key="b_valores")
            col2.text_area("Diferencial Competitivo",
                "• Mix amplo: cabelos + maquiagem + skincare + perfumaria\n"
                "• Produtos para todos os tipos de cabelo (incluindo afro)\n"
                "• Ponto PUDO integrado (retirada de qualquer e-commerce)\n"
                "• Consultoria de skincare e colorimetria gratuita", height=80, key="b_dif")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("3. PRODUTOS E SERVIÇOS"):
            st.markdown('<div class="sebrae-section-beleza">', unsafe_allow_html=True)
            st.markdown("""
| Categoria | Exemplos | Ticket Médio | Margem Estimada |
|---|---|---|---|
| Cabelos — coloração | Tinturas, descolorantes, alisantes, progressivas | R$ 40–180 | 55–70% |
| Cabelos — tratamento | Shampoo, condicionador, máscaras, leave-in | R$ 25–120 | 50–65% |
| Maquiagem | Base, batom, rímel, paleta de sombras, primer | R$ 20–150 | 55–70% |
| Skincare | Hidratante, sérum, protetor solar, tônico | R$ 30–200 | 55–70% |
| Perfumaria | Águas de colônia, body splash, desodorantes | R$ 25–150 | 50–65% |
| Unhas | Esmaltes, removedor, acessórios nail art | R$ 10–60 | 60–75% |
| Serviços PUDO | Retirada e devolução de encomendas | R$ 3–15/pacote | 100% |
""")
            st.text_area("Produtos que pretende adicionar (preencha)", "", height=60, key="b_prod_add")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("4. ANÁLISE DE MERCADO"):
            st.markdown('<div class="sebrae-section-beleza">', unsafe_allow_html=True)
            st.markdown("##### 4.1 Clientes-Alvo")
            st.markdown("""
| Perfil | Detalhe |
|---|---|
| **Gênero predominante** | Feminino (80%) |
| **Faixa etária** | 18–50 anos |
| **Classe social** | C1 e C2 (renda R$ 1.500–5.000/mês) |
| **Comportamento** | Alta recorrência; sensível a promoções e tendências |
| **Canal preferido** | Físico para experimentar + online para recompra |
| **Frequência** | Quinzenal a mensal |
| **Motivação** | Autoestima, cuidado pessoal, beleza profissional em casa |
""")
            st.text_area("Observações sobre clientes da sua região", "", height=60, key="b_clientes")

            st.markdown("##### 4.2 Concorrentes")
            st.markdown("""
| Concorrente | Tipo | Ponto Fraco |
|---|---|---|
| Farmácias (Drogasil, Pague Menos) | Física | Variedade limitada, preço alto |
| Salões de beleza | Serviço | Não vendem produto retail |
| Beleza na Web / Sephora online | E-commerce | Frete alto, sem consultoria |
| Camelô / feiras | Físico | Procedência duvidosa |
""")
            st.text_area("Concorrentes identificados na sua região (preencha)", "", height=60, key="b_concorrentes")

            st.markdown("##### 4.3 Fornecedores Recomendados")
            st.markdown("""
| Fornecedor | Produtos | Link |
|---|---|---|
| **Wella / Coty** | Coloração profissional | [wella.com/pt-br](https://www.wella.com/pt-br) |
| **L'Oréal Professionnel** | Cabelos e skincare | Distribuidores autorizados SP |
| **Amend / Griffus** | Cabelos afro e gerais | Atacado SP |
| **Eudora / O Boticário Atacado** | Maquiagem e perfumaria | Via revendedor |
| **Atacado Brás / Bom Retiro** | Mix geral beleza | Pesquisa presencial |
""")
            st.markdown("**Regulação ANVISA cosméticos:** [gov.br/anvisa/cosmeticos](https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/cosmeticos)")
            st.markdown("**Dados do setor:** [ABIHPEC](https://www.abihpec.org.br/publicacao/panorama-do-setor/)")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("5. PLANO DE MARKETING — 4Ps"):
            st.markdown('<div class="sebrae-section-beleza">', unsafe_allow_html=True)
            p1, p2 = st.columns(2)
            p1.markdown("**💄 PRODUTO**")
            p1.text_area("Linha de produtos e diferenciais",
                "• Mix completo: cabelos (todos tipos), maquiagem, skincare, perfumaria\n"
                "• Produtos veganos e cruelty-free em destaque\n"
                "• Linha específica para cabelos afro e crespos\n"
                "• Kits presente (natal, dia das mães, aniversário)", height=120, key="b_produto")
            p1.markdown("**💰 PREÇO**")
            p1.text_area("Estratégia de preço",
                "• Preços 10–20% abaixo de farmácias\n"
                "• Programa fidelidade: carimbo (10ª compra = 1 produto grátis)\n"
                "• Combos temáticos com desconto\n"
                "• Parcelamento em até 3x sem juros", height=120, key="b_preco")
            p2.markdown("**📍 PRAÇA**")
            p2.text_area("Canais de venda",
                "• Loja física — Vila Carrão\n"
                "• WhatsApp Business (catálogo + pedidos)\n"
                "• Instagram Shopping\n"
                "• Mercado Livre e Shopee (produtos top sellers)\n"
                "• Delivery via motoboy (raio 5 km)", height=120, key="b_praca")
            p2.markdown("**📣 PROMOÇÃO**")
            p2.text_area("Ações de marketing",
                "• TikTok e Instagram: tutoriais de maquiagem/cabelo (diário)\n"
                "• Micro-influenciadoras locais da Zona Leste (permuta)\n"
                "• Stories com promoções relâmpago\n"
                "• Google Meu Negócio com fotos atualizadas\n"
                "• Cartão fidelidade físico", height=120, key="b_promo")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("6. PLANO OPERACIONAL"):
            st.markdown('<div class="sebrae-section-beleza">', unsafe_allow_html=True)
            st.markdown("""
**Layout sugerido (60 m²):**
- Balcão de atendimento + caixa: 8 m²
- Exposição beleza (gôndolas, display): 22 m²
- Área de estoque PUDO (encomendas): 12 m²
- Estoque de produtos (cosméticos): 13 m²
- Provador de maquiagem / espelho: 5 m²

**Atenção regulatória:**
- Cosméticos grau 1 (shampoo, batom): apenas notificação ANVISA no fornecedor
- Cosméticos grau 2 (alisantes, tinturas): exige registro ANVISA — comprar só de distribuidores com nota fiscal

**Horário de funcionamento:**
- Seg–Sex: 08h00 às 19h30 | Sáb: 08h00 às 16h00
""")
            st.text_area("Anotações operacionais (preencha)", "", height=60, key="b_op")
            st.markdown("**Links:** [ANVISA cosméticos](https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/cosmeticos) · [Bling ERP](https://www.bling.com.br) · [Beauty Fair SP](https://www.beautyfair.com.br)")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Projeção Financeira Beleza ───────────────────────────────────────────
    with financ_b:
        st.markdown('<div class="sebrae-section-beleza"><b>Configure os parâmetros do segmento Beleza</b></div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        b_itens    = c1.number_input("Itens beleza vendidos/mês (meta M6)", 0, 3000, 100, 5, key="bf_itens")
        b_ticket   = c1.number_input("Ticket médio beleza (R$)", 0.0, 500.0, 90.0, 5.0, key="bf_tick")
        b_margem   = c1.slider("Margem bruta (%)", 0, 100, 58, key="bf_marg")
        b_cresc    = c2.slider("Crescimento mensal meses 1→6 (%)", 0, 60, 20, key="bf_cresc")
        b_capex_e  = c2.number_input("Estoque inicial Beleza (R$)", 0, 100000, 6000, 500, key="bf_capex")
        b_capex_o  = c2.number_input("Outros CAPEX Beleza (R$)", 0, 50000, 4000, 500, key="bf_capo")
        b_meses_cg = c3.slider("Meses de capital de giro", 1, 6, 3, key="bf_cg")

        rec_beleza_m6 = b_itens * b_ticket * (b_margem / 100)
        capex_beleza  = b_capex_e + b_capex_o + opex_fixo_base * b_meses_cg
        df_b = projecao_12m(rec_beleza_m6, 100 - b_margem, b_cresc, opex_fixo_base, aliquota)
        be_b = next((i + 1 for i, s in enumerate(df_b["Saldo Acumulado"]) if s >= 0), None)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("CAPEX Beleza", f"R$ {capex_beleza:,.0f}".replace(",", "."))
        k2.metric("Receita (margem) Mês 6", f"R$ {rec_beleza_m6 + rec_logistica:,.0f}".replace(",", "."))
        res6b = df_b["Resultado"].iloc[5]
        k3.metric("Resultado Mês 6", f"R$ {res6b:,.0f}".replace(",", "."))
        k4.metric("Break-even (mês)", f"Mês {be_b}" if be_b else "Após 12m")

        st.plotly_chart(grafico_fc(df_b, "#ad1457"), use_container_width=True)
        st.dataframe(tabela_fc(df_b), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("📦 Mix de Estoque Sugerido — Beleza")
        dados_mix_b = {
            "Categoria": ["Coloração / cabelos", "Tratamento capilar", "Maquiagem",
                          "Skincare", "Perfumaria / unhas"],
            "% do Estoque": [25, 25, 20, 15, 15],
            "Valor Sugerido (R$)": [
                round(b_capex_e * 0.25), round(b_capex_e * 0.25),
                round(b_capex_e * 0.20), round(b_capex_e * 0.15),
                round(b_capex_e * 0.15)
            ]
        }
        st.dataframe(pd.DataFrame(dados_mix_b), use_container_width=True, hide_index=True)
        st.markdown("**Regulação:** [ANVISA cosméticos](https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/cosmeticos)")
        st.markdown("**Dados do setor:** [ABIHPEC](https://www.abihpec.org.br/publicacao/panorama-do-setor/) · [Beauty Fair](https://www.beautyfair.com.br)")
        st.markdown("**Venda online:** [Mercado Livre Seller](https://www.mercadolivre.com.br/vendedor) · [Shopee Seller](https://seller.shopee.com.br)")

st.divider()
st.caption("📦 PUDO Vila Carrão — Plano de Negócio v2.0 | Modelo SEBRAE integrado | Dados estimados para fins de planejamento.")
