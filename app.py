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
    [data-testid="stAppViewContainer"] { background: #f4f6f9; }
    [data-testid="stSidebar"] { background: #1a1f2e; }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] .stSlider > label { color: #aaa !important; }
    .block-container { padding-top: 1.5rem; }

    .hero-card {
        background: white; border-radius: 12px; padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07); text-align: center;
        border-top: 4px solid #2563eb;
    }
    .hero-card.green  { border-top-color: #16a34a; }
    .hero-card.red    { border-top-color: #dc2626; }
    .hero-card.purple { border-top-color: #7c3aed; }
    .hero-card.orange { border-top-color: #ea580c; }
    .hero-card.teal   { border-top-color: #0d9488; }
    .hero-val  { font-size: 26px; font-weight: 700; color: #111; margin: 4px 0; }
    .hero-lbl  { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: .5px; }
    .hero-sub  { font-size: 13px; color: #888; margin-top: 2px; }

    .section-title {
        font-size: 13px; font-weight: 700; color: #2563eb;
        text-transform: uppercase; letter-spacing: 1px;
        border-bottom: 2px solid #2563eb; padding-bottom: 6px;
        margin: 20px 0 12px;
    }
    .section-title.green  { color: #16a34a; border-color: #16a34a; }
    .section-title.pink   { color: #be185d; border-color: #be185d; }

    .dre-row  { display:flex; justify-content:space-between; padding: 5px 0; font-size: 14px; border-bottom: 1px solid #f0f0f0; }
    .dre-bold { font-weight: 700; }
    .dre-pos  { color: #16a34a; font-weight: 600; }
    .dre-neg  { color: #dc2626; font-weight: 600; }
    .dre-box  { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }

    .model-badge {
        display: inline-block; padding: 6px 18px; border-radius: 20px;
        font-size: 13px; font-weight: 600; margin-right: 8px;
    }
    .badge-pesca  { background: #dcfce7; color: #15803d; }
    .badge-beleza { background: #fce7f3; color: #9d174d; }
    .badge-pudo   { background: #dbeafe; color: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Parâmetros")

    modelo = st.radio("Modelo de Negócio", ["📦🐟  PUDO + Pesca", "📦💄  PUDO + Beleza"], index=0)
    is_pesca = "Pesca" in modelo
    accent   = "#16a34a" if is_pesca else "#be185d"

    st.markdown("---")
    st.markdown("#### 🏠 Custos Fixos Mensais")
    aluguel      = st.number_input("Aluguel (R$)",             0, 30000,  3500, 100)
    condominio   = st.number_input("Condomínio + IPTU (R$)",   0,  5000,   300,  50)
    energia      = st.number_input("Energia elétrica (R$)",    0,  5000,   400,  50)
    internet     = st.number_input("Internet + Telefone (R$)", 0,  1000,   300,  10)
    salarios     = st.number_input("Salários brutos (R$)",     0, 20000,  2200, 100)
    enc_pct      = st.slider("Encargos trabalhistas (%)", 0, 100, 70)
    contador     = st.number_input("Contador (R$)",            0,  3000,   450,  50)
    sistema_erp  = st.number_input("ERP / PDV (R$)",           0,  2000,   200,  10)
    embalagens   = st.number_input("Embalagens (R$)",          0,  5000,   400,  50)
    mkt_mensal   = st.number_input("Marketing / ADS (R$)",     0, 10000,   500,  50)
    seguros      = st.number_input("Seguros (R$)",             0,  2000,   200,  50)
    taxas_banco  = st.number_input("Taxas bancárias (R$)",     0,  2000,   200,  50)

    st.markdown("---")
    st.markdown("#### 📦 PUDO + Logística")
    pudo_vol     = st.number_input("Pacotes PUDO / mês",         0, 5000,  400, 10)
    pudo_tick    = st.number_input("Comissão / pacote (R$)",  0.0, 20.0,  3.5,  .5)
    rev_vol      = st.number_input("Devoluções / mês",           0, 2000,   80, 10)
    rev_tick     = st.number_input("Comissão / devolução (R$)",0.0, 30.0,  8.0,  .5)
    full_vol     = st.number_input("Fulfilment / mês",           0, 2000,   50,  5)
    full_tick    = st.number_input("Receita / pedido (R$)",    0.0, 50.0, 12.0, 1.0)

    st.markdown("---")
    if is_pesca:
        st.markdown("#### 🐟 Produto — Pesca")
        prod_itens  = st.number_input("Itens / mês (meta M6)",   0, 2000,  70,  5)
        prod_ticket = st.number_input("Ticket médio (R$)",     0.0, 1000., 180., 10.)
        prod_marg   = st.slider("Margem bruta (%)", 0, 100, 50)
        capex_est   = st.number_input("Estoque inicial (R$)",    0, 100000, 8000, 500)
    else:
        st.markdown("#### 💄 Produto — Beleza")
        prod_itens  = st.number_input("Itens / mês (meta M6)",   0, 3000, 100,   5)
        prod_ticket = st.number_input("Ticket médio (R$)",     0.0,  500.,  90.,  5.)
        prod_marg   = st.slider("Margem bruta (%)", 0, 100, 58)
        capex_est   = st.number_input("Estoque inicial (R$)",    0, 100000, 6000, 500)

    st.markdown("---")
    st.markdown("#### 💰 Investimento Inicial")
    capex_obra   = st.number_input("Obra / Reforma (R$)",    0, 200000, 10000, 500)
    capex_equip  = st.number_input("Equip. + TI + Seg. (R$)",0,  50000,  8000, 500)
    capex_mkt_i  = st.number_input("Marketing inicial (R$)", 0,  20000,  2000, 500)
    capex_aber   = st.number_input("Abertura empresa (R$)",  0,  10000,  1500, 100)
    meses_cg     = st.slider("Meses capital de giro", 1, 6, 3)

    st.markdown("---")
    st.markdown("#### 📐 Cenários e Impostos")
    crescimento  = st.slider("Crescimento meses 1→6 (%)", 0, 60, 22)
    aliquota     = st.slider("Simples Nacional (%)", 0.0, 20.0, 6.0, .5)
    depreciacao  = st.number_input("Depreciação mensal estimada (R$)", 0, 5000, 500, 50)

# ══════════════════════════════════════════════════════════════
# CÁLCULOS CENTRAIS
# ══════════════════════════════════════════════════════════════
enc_val      = salarios * enc_pct / 100
opex_fixo    = (aluguel + condominio + energia + internet + salarios +
                enc_val + contador + sistema_erp + embalagens +
                mkt_mensal + seguros + taxas_banco)

capex_total  = (capex_obra + capex_equip + capex_est +
                capex_mkt_i + capex_aber + opex_fixo * meses_cg)

rec_pudo_m   = pudo_vol  * pudo_tick
rec_rev_m    = rev_vol   * rev_tick
rec_full_m   = full_vol  * full_tick
rec_log_base = rec_pudo_m + rec_rev_m + rec_full_m

gmv_prod_m6  = prod_itens * prod_ticket
rec_prod_m6  = gmv_prod_m6 * prod_marg / 100
cmv_prod_m6  = gmv_prod_m6 * (1 - prod_marg / 100)

rec_total_m6 = rec_log_base + rec_prod_m6
imp_m6       = rec_total_m6 * aliquota / 100
custo_total_m6 = opex_fixo + cmv_prod_m6 + imp_m6
ebitda_m6    = rec_total_m6 - custo_total_m6
lucro_m6     = ebitda_m6 - depreciacao
margem_b_m6  = rec_prod_m6 / rec_total_m6 * 100 if rec_total_m6 else 0
margem_l_m6  = lucro_m6 / rec_total_m6 * 100 if rec_total_m6 else 0
payback      = capex_total / max(lucro_m6, 1)
ponto_eq     = (opex_fixo + depreciacao) / (1 - aliquota / 100)

# ── Projeção 12 meses (3 cenários)
def proj(fator_cenario):
    rows = []
    saldo = 0.0
    for m in range(1, 13):
        fat = max((1 + crescimento / 100) ** (m - 6), 0.08) if m < 6 else 1.0
        fat *= fator_cenario
        gmv_m  = gmv_prod_m6 * fat
        rp_m   = rec_log_base * fator_cenario
        rl_m   = gmv_m * prod_marg / 100
        rec_m  = rp_m + rl_m
        cmv_m  = gmv_m * (1 - prod_marg / 100)
        imp_m  = rec_m * aliquota / 100
        custo_m = opex_fixo + cmv_m + imp_m
        ebitda_m = rec_m - custo_m
        lucro_m  = ebitda_m - depreciacao
        saldo   += lucro_m
        rows.append({
            "Mês": f"M{m}", "Receita": rec_m, "CMV": cmv_m,
            "Impostos": imp_m, "Desp Op": opex_fixo,
            "EBITDA": ebitda_m, "Lucro Líquido": lucro_m,
            "Saldo Acum": saldo, "PUDO Base": rp_m, "Prod": rl_m,
        })
    return pd.DataFrame(rows)

df_real = proj(1.0)
df_pess = proj(0.70)
df_otim = proj(1.40)
be_mes   = next((i+1 for i, s in enumerate(df_real["Saldo Acum"]) if s >= 0), None)
roi_12   = df_real["Lucro Líquido"].sum() / capex_total * 100 if capex_total else 0

# ══════════════════════════════════════════════════════════════
# CABEÇALHO
# ══════════════════════════════════════════════════════════════
segmento_label = "🐟 Pesca" if is_pesca else "💄 Beleza"
cor_badge = "badge-pesca" if is_pesca else "badge-beleza"

st.markdown(f"""
<h2 style="margin-bottom:4px;">📦 PUDO Vila Carrão
  <span class="model-badge badge-pudo">PUDO</span>
  <span class="model-badge {cor_badge}">{segmento_label}</span>
</h2>
<p style="color:#666;margin-top:0;">Plano de Negócio Integrado — Zona Leste de São Paulo</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TABS PRINCIPAIS
# ══════════════════════════════════════════════════════════════
t_dash, t_fin, t_cont, t_plano, t_draw = st.tabs([
    "🎯  Dashboard Executivo",
    "💰  Financeiro",
    "📊  Contabilidade (DRE)",
    "📋  Plano de Negócio",
    "✏️  Desenho da Estrutura",
])

# ════════════════════════════════════════════════
# TAB 1 — DASHBOARD EXECUTIVO
# ════════════════════════════════════════════════
with t_dash:
    def kpi(col, label, val, sub="", cls=""):
        col.markdown(f"""
        <div class="hero-card {cls}">
          <div class="hero-lbl">{label}</div>
          <div class="hero-val">{val}</div>
          <div class="hero-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    # Linha 1
    c1, c2, c3 = st.columns(3)
    kpi(c1, "Investimento Total",  f"R$ {capex_total:,.0f}".replace(",","."), "CAPEX total necessário")
    kpi(c2, "OPEX Fixo / Mês",    f"R$ {opex_fixo:,.0f}".replace(",","."),   "custos fixos mensais")
    kpi(c3, "Receita Mês 6",      f"R$ {rec_total_m6:,.0f}".replace(",","."), "cenário realista", "green")
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
    # Linha 2
    c4, c5, c6 = st.columns(3)
    kpi(c4, "EBITDA Mês 6",       f"R$ {ebitda_m6:,.0f}".replace(",","."),
        f"Margem {margem_b_m6:.1f}%", "green" if ebitda_m6 > 0 else "red")
    kpi(c5, "Break-even / Payback", f"Mês {be_mes}" if be_mes else ">12m",
        f"Payback {payback:.1f} meses", "purple")
    kpi(c6, "ROI 12 meses",       f"{roi_12:.1f}%", "retorno sobre CAPEX", "teal")

    st.markdown("<br>", unsafe_allow_html=True)
    col_g1, col_g2 = st.columns([2,1])

    with col_g1:
        st.markdown('<div class="section-title">Projeção de Receita vs Custo — 12 Meses (Realista)</div>',
                    unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_real["Mês"], y=df_real["Receita"],
            name="Receita Total", marker_color="#2563eb", opacity=.8), secondary_y=False)
        fig.add_trace(go.Bar(x=df_real["Mês"], y=df_real["Desp Op"]+df_real["CMV"]+df_real["Impostos"],
            name="Custo Total", marker_color="#dc2626", opacity=.7), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_real["Mês"], y=df_real["Saldo Acum"],
            name="Saldo Acumulado", line=dict(color="#16a34a", width=3),
            mode="lines+markers"), secondary_y=True)
        fig.add_trace(go.Scatter(x=df_real["Mês"], y=df_real["PUDO Base"],
            name="Piso PUDO", line=dict(color="#7c3aed", width=2, dash="dot"),
            mode="lines"), secondary_y=False)
        fig.add_hline(y=0, line_dash="dot", line_color="#999", secondary_y=True)
        fig.update_layout(barmode="group", height=340,
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", y=-0.28, x=0),
            margin=dict(l=0,r=0,t=10,b=0))
        fig.update_yaxes(gridcolor="#f0f0f0", secondary_y=False)
        fig.update_yaxes(gridcolor="#f0f0f0", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.markdown('<div class="section-title">Composição da Receita (Mês 6)</div>',
                    unsafe_allow_html=True)
        labels = ["PUDO Retirada", "Log. Reversa", "Fulfilment",
                  segmento_label.replace("🐟 ","").replace("💄 ","")]
        values = [rec_pudo_m, rec_rev_m, rec_full_m, rec_prod_m6]
        cores  = ["#2563eb","#7c3aed","#0d9488", "#16a34a" if is_pesca else "#be185d"]
        fig2 = go.Figure(go.Pie(labels=labels, values=values, hole=.5,
            marker_colors=cores, textinfo="percent+label", textfont_size=11))
        fig2.update_layout(height=290, showlegend=False,
            paper_bgcolor="white",
            margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:14px;margin-top:8px;box-shadow:0 1px 4px rgba(0,0,0,.06)">
          <div style="font-size:12px;color:#666;margin-bottom:8px;">RECEITA BASE (PUDO)</div>
          <div style="font-size:20px;font-weight:700;color:#2563eb;">R$ {rec_log_base:,.0f}</div>
          <div style="font-size:11px;color:#999;margin-top:4px;">Piso garantido independente das vendas de produto</div>
        </div>""".replace(",","."), unsafe_allow_html=True)

    # Comparativo 3 cenários
    st.markdown('<div class="section-title">Comparativo de Cenários — Lucro Acumulado 12 Meses</div>',
                unsafe_allow_html=True)
    fig3 = go.Figure()
    for df_c, nome, cor, fill in [
        (df_pess,"Pessimista (−30%)","#ef4444","rgba(239,68,68,0.08)"),
        (df_real,"Realista","#2563eb","rgba(37,99,235,0.08)"),
        (df_otim,"Otimista (+40%)","#16a34a","rgba(22,163,74,0.10)"),
    ]:
        fig3.add_trace(go.Scatter(
            x=df_c["Mês"], y=df_c["Saldo Acum"], name=nome,
            line=dict(color=cor, width=2.5),
            fill="tozeroy", fillcolor=fill, mode="lines"))
    fig3.add_hline(y=0, line_dash="dash", line_color="#666",
                   annotation_text="Break-even", annotation_position="right")
    fig3.update_layout(height=260, plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.30),
        margin=dict(l=0,r=0,t=10,b=0))
    fig3.update_yaxes(gridcolor="#f0f0f0")
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════
# TAB 2 — FINANCEIRO
# ════════════════════════════════════════════════
with t_fin:
    st.markdown('<div class="section-title">Fluxo de Caixa Mensal — Cenário Realista</div>',
                unsafe_allow_html=True)

    # Decomposição de resultado Mês 6 (barras horizontais)
    cats_h = ["Rec. PUDO", f"Rec. {segmento_label.split()[-1]}", "Impostos",
              "CMV Produto", "Desp. Operacionais", "Depreciação", "EBITDA", "Lucro Líquido"]
    vals_h = [rec_log_base, rec_prod_m6, -imp_m6, -cmv_prod_m6,
              -opex_fixo, -depreciacao, ebitda_m6, lucro_m6]
    cores_h = ["#2563eb","#2563eb","#ef4444","#ef4444","#ef4444","#f97316","#7c3aed",
               "#16a34a" if lucro_m6 >= 0 else "#dc2626"]

    fig_wf = go.Figure()
    fig_wf.add_trace(go.Bar(
        x=vals_h, y=cats_h, orientation="h",
        marker_color=cores_h,
        text=[f"R$ {abs(v):,.0f}".replace(",", ".") for v in vals_h],
        textposition="outside",
        cliponaxis=False,
    ))
    fig_wf.add_vline(x=0, line_color="#666", line_width=1.5)
    fig_wf.update_layout(
        height=340, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, margin=dict(l=0, r=120, t=10, b=0),
        xaxis=dict(gridcolor="#f0f0f0", zeroline=False),
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown('<div class="section-title">Tabela de Fluxo de Caixa — 12 Meses</div>',
                unsafe_allow_html=True)

    df_fc = df_real[["Mês","PUDO Base","Prod","Receita","CMV","Impostos",
                     "Desp Op","EBITDA","Lucro Líquido","Saldo Acum"]].copy()
    df_fc.columns = ["Mês","Rec PUDO","Rec Produto","Rec Total","CMV",
                     "Impostos","Desp Fixas","EBITDA","Lucro Líq","Saldo Acum"]

    def fmt_fc(df):
        d = df.copy()
        for c in d.columns[1:]:
            d[c] = d[c].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))
        def cor(val):
            try:
                v = float(val.replace("R$ ","").replace(".","").replace(",","."))
                if v >= 0: return "color:#16a34a;font-weight:600"
                return "color:#dc2626;font-weight:600"
            except: return ""
        return d.style.map(cor, subset=["EBITDA","Lucro Líq","Saldo Acum"])

    st.dataframe(fmt_fc(df_fc), use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Análise de Break-Even</div>', unsafe_allow_html=True)
    col_be1, col_be2, col_be3 = st.columns(3)

    with col_be1:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.06)">
          <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:.5px">Ponto de Equilíbrio Mensal</div>
          <div style="font-size:28px;font-weight:700;color:#2563eb;margin:8px 0">R$ {ponto_eq:,.0f}</div>
          <div style="font-size:12px;color:#999">Receita mínima para cobrir todos os custos</div>
        </div>""".replace(",","."), unsafe_allow_html=True)
    with col_be2:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.06)">
          <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:.5px">Mês do Break-Even</div>
          <div style="font-size:28px;font-weight:700;color:#7c3aed;margin:8px 0">{"Mês "+str(be_mes) if be_mes else "Após M12"}</div>
          <div style="font-size:12px;color:#999">Quando o saldo acumulado fica positivo</div>
        </div>""", unsafe_allow_html=True)
    with col_be3:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.06)">
          <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:.5px">Payback do Investimento</div>
          <div style="font-size:28px;font-weight:700;color:#0d9488;margin:8px 0">{payback:.1f} meses</div>
          <div style="font-size:12px;color:#999">Tempo de retorno do CAPEX total</div>
        </div>""", unsafe_allow_html=True)

    # Gráfico break-even
    meses_range = list(range(0, int(max(payback*1.4, 15))))
    acum_real = [-capex_total + df_real["Lucro Líquido"].iloc[:m].sum()
                 if m <= 12 else -capex_total + df_real["Lucro Líquido"].sum()
                 for m in meses_range]

    fig_be = go.Figure()
    fig_be.add_trace(go.Scatter(x=meses_range, y=acum_real,
        fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
        line=dict(color="#2563eb", width=2.5), name="Retorno acumulado"))
    fig_be.add_hline(y=0, line_dash="dash", line_color="#dc2626",
                     annotation_text="Recuperação do investimento")
    fig_be.update_layout(height=220, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
        xaxis_title="Meses", yaxis_title="R$ acumulado")
    fig_be.update_yaxes(gridcolor="#f0f0f0")
    st.plotly_chart(fig_be, use_container_width=True)

# ════════════════════════════════════════════════
# TAB 3 — CONTABILIDADE / DRE
# ════════════════════════════════════════════════
with t_cont:
    col_dre, col_comp = st.columns([1, 1])

    with col_dre:
        st.markdown('<div class="section-title">DRE — Demonstrativo de Resultado (Mês 6)</div>',
                    unsafe_allow_html=True)

        def linha(lbl, val, cls="", indent=0):
            pad = f"padding-left:{indent*16}px"
            sinal = "+" if val >= 0 else "−"
            val_fmt = f"R$ {abs(val):,.0f}".replace(",",".")
            if cls == "total":
                return f"""<div class="dre-row dre-bold" style="{pad};background:#f8faff;border-radius:4px;padding:7px 4px">
                    <span>{lbl}</span><span class="dre-pos" style="color:#111">{val_fmt}</span></div>"""
            elif cls == "pos":
                return f"""<div class="dre-row" style="{pad}">
                    <span style="color:#555">{lbl}</span><span class="dre-pos">{val_fmt}</span></div>"""
            elif cls == "neg":
                return f"""<div class="dre-row" style="{pad}">
                    <span style="color:#555">{lbl}</span><span class="dre-neg">({val_fmt})</span></div>"""
            elif cls == "result":
                cor = "#16a34a" if val >= 0 else "#dc2626"
                return f"""<div class="dre-row dre-bold" style="{pad};margin-top:6px;background:#f0fdf4;border-radius:4px;padding:8px 4px">
                    <span>{lbl}</span>
                    <span style="font-size:16px;color:{cor}">{val_fmt}</span></div>"""
            return f"""<div class="dre-row" style="{pad}">
                <span style="color:#888;font-size:12px">{lbl}</span><span style="color:#888">{val_fmt}</span></div>"""

        lucro_bruto = rec_total_m6 - cmv_prod_m6
        marg_bruta  = lucro_bruto / rec_total_m6 * 100 if rec_total_m6 else 0
        marg_ebitda = ebitda_m6   / rec_total_m6 * 100 if rec_total_m6 else 0
        marg_liq    = lucro_m6    / rec_total_m6 * 100 if rec_total_m6 else 0

        dre_html = '<div class="dre-box">'
        dre_html += linha("(+) RECEITA OPERACIONAL BRUTA", rec_total_m6, "total")
        dre_html += linha("Comissões PUDO", rec_pudo_m, "pos", 1)
        dre_html += linha("Logística Reversa", rec_rev_m, "pos", 1)
        dre_html += linha("Fulfilment", rec_full_m, "pos", 1)
        dre_html += linha(f"Venda {segmento_label} (margem bruta)", rec_prod_m6, "pos", 1)
        dre_html += linha("(−) Impostos — Simples Nacional", imp_m6, "neg")
        dre_html += linha("(=) RECEITA LÍQUIDA", rec_total_m6 - imp_m6, "total")
        dre_html += linha("(−) Custo das Mercadorias Vendidas (CMV)", cmv_prod_m6, "neg")
        dre_html += linha(f"(=) LUCRO BRUTO  —  Margem {marg_bruta:.1f}%", lucro_bruto, "total")
        dre_html += linha("(−) DESPESAS OPERACIONAIS", opex_fixo, "neg")
        dre_html += linha("Pessoal + Encargos", salarios + enc_val, "neg", 1)
        dre_html += linha("Aluguel + Condomínio", aluguel + condominio, "neg", 1)
        dre_html += linha("Energia + Internet + Tel", energia + internet, "neg", 1)
        dre_html += linha("Marketing / ADS", mkt_mensal, "neg", 1)
        dre_html += linha("Contador + ERP", contador + sistema_erp, "neg", 1)
        dre_html += linha("Embalagens + Seguros + Banco", embalagens + seguros + taxas_banco, "neg", 1)
        dre_html += linha(f"(=) EBITDA  —  Margem {marg_ebitda:.1f}%", ebitda_m6, "result")
        dre_html += linha("(−) Depreciação estimada", depreciacao, "neg")
        dre_html += linha(f"(=) LUCRO LÍQUIDO  —  Margem {marg_liq:.1f}%", lucro_m6, "result")
        dre_html += '</div>'

        st.markdown(dre_html, unsafe_allow_html=True)

    with col_comp:
        st.markdown('<div class="section-title">Decomposição de Custos</div>',
                    unsafe_allow_html=True)

        custos_items = {
            "Pessoal + Encargos": salarios + enc_val,
            "Aluguel + Cond.": aluguel + condominio,
            "CMV Produtos": cmv_prod_m6,
            "Impostos": imp_m6,
            "Marketing": mkt_mensal,
            "Energia + Internet": energia + internet,
            "Contador + ERP": contador + sistema_erp,
            "Embalagens + Seg + Banco": embalagens + seguros + taxas_banco,
            "Depreciação": depreciacao,
        }
        custos_items = {k: v for k, v in custos_items.items() if v > 0}

        fig_c = px.bar(
            x=list(custos_items.values()),
            y=list(custos_items.keys()),
            orientation="h",
            color=list(custos_items.values()),
            color_continuous_scale=["#dbeafe","#2563eb"],
            text=[f"R$ {v:,.0f}".replace(",",".") for v in custos_items.values()],
        )
        fig_c.update_traces(textposition="outside")
        fig_c.update_layout(height=340, showlegend=False, coloraxis_showscale=False,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=0,r=80,t=10,b=0))
        fig_c.update_xaxes(visible=False)
        fig_c.update_yaxes(tickfont=dict(size=11))
        st.plotly_chart(fig_c, use_container_width=True)

        # DRE Anual
        st.markdown('<div class="section-title">DRE Anual Projetado</div>',
                    unsafe_allow_html=True)
        dre_anual = {
            "Receita Bruta":    df_real["Receita"].sum(),
            "Impostos":        -df_real["Impostos"].sum(),
            "CMV":             -df_real["CMV"].sum(),
            "Desp. Operac.":   -df_real["Desp Op"].sum(),
            "EBITDA":           df_real["EBITDA"].sum(),
            "Depreciação":     -depreciacao * 12,
            "Lucro Líquido":    df_real["Lucro Líquido"].sum(),
        }
        rows_da = []
        for k, v in dre_anual.items():
            rows_da.append({
                "Item": k,
                "Valor (R$)": f"R$ {v:,.0f}".replace(",","."),
                "% Receita": f"{v/dre_anual['Receita Bruta']*100:.1f}%" if dre_anual["Receita Bruta"] else "—",
            })
        df_da = pd.DataFrame(rows_da)

        def cor_dre(val):
            try:
                v = float(val.replace("R$ ","").replace(".","").replace(",","."))
                if v > 0: return "color:#16a34a;font-weight:600"
                if v < 0: return "color:#dc2626"
            except: pass
            return ""

        st.dataframe(df_da.style.map(cor_dre, subset=["Valor (R$)"]),
                     use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════
# TAB 4 — PLANO DE NEGÓCIO
# ════════════════════════════════════════════════
with t_plano:
    segmento_nome = "Pesca Esportiva" if is_pesca else "Cosméticos e Beleza"
    cor_sec = "green" if is_pesca else "pink"
    emoji_s = "🐟" if is_pesca else "💄"

    st.markdown(f'<div class="section-title {cor_sec}">Modelo de Negócio Integrado — PUDO + {segmento_nome}</div>',
                unsafe_allow_html=True)

    # Modelo canvas simplificado
    c1, c2, c3 = st.columns(3)
    canvas_items = {
        "Proposta de Valor": (
            "• Ponto de conveniência multifuncional\n"
            "• Retirada de qualquer e-commerce (PUDO)\n"
            f"• Venda especializada em {segmento_nome.lower()}\n"
            "• Atendimento consultivo presencial"
        ),
        "Segmentos de Cliente": (
            ("• Pescadores zona leste (masc. 25–55 anos)\n"
             "• Compradores online sem endereço fixo\n"
             "• Vendedores de marketplace (fulfilment)\n"
             "• Clubes e grupos de pesca da região") if is_pesca else
            ("• Mulheres 18–50 anos, classes C/B\n"
             "• Compradores online sem endereço fixo\n"
             "• Vendedores de marketplace (fulfilment)\n"
             "• Profissionais de beleza autônomos")
        ),
        "Fontes de Receita": (
            "• Comissão por pacote PUDO (R$ 3–5)\n"
            "• Comissão logística reversa (R$ 8–15)\n"
            "• Margem sobre venda de produto (45–60%)\n"
            "• Fulfilment para vendedores locais (R$ 12)"
        ),
    }
    for col, (titulo, txt) in zip([c1,c2,c3], canvas_items.items()):
        col.markdown(f"""
        <div style="background:white;border-radius:12px;padding:18px;
             box-shadow:0 1px 4px rgba(0,0,0,.06);height:180px;overflow:auto">
          <div style="font-size:11px;font-weight:700;color:{accent};
               text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">{titulo}</div>
          <div style="font-size:13px;color:#444;white-space:pre-line">{txt}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Plano em expanders
    with st.expander(f"1. ANÁLISE DE MERCADO — {segmento_nome.upper()}", expanded=True):
        if is_pesca:
            st.markdown("""
| Indicador | Dado | Fonte |
|---|---|---|
| Mercado pesca esportiva Brasil (2024) | R$ 3,5 bilhões | ABPESCA / Sebrae |
| Crescimento anual estimado | 12% a.a. | Sebrae Agro |
| Pescadores ativos no Brasil | ~35 milhões | IBAMA |
| Ticket médio online (pesca) | R$ 150–350 | Mercado Livre |
| Sazonalidade alta | Março–Setembro | Calendário IBAMA SP |
| Zona Leste SP — perfil | Classes B2/C1, forte comunidade de lazer | IBGE / DataSP |

**Links de referência:**
[ABPESCA](https://www.abpesca.com.br) · [Sebrae Pesca](https://www.sebrae.com.br/sites/PortalSebrae/artigos/pesca-esportiva) · [MPA](https://www.gov.br/agricultura/pt-br/assuntos/aquicultura-e-pesca) · [Mercado Livre Pesca](https://www.mercadolivre.com.br/c/pesca)
""")
        else:
            st.markdown("""
| Indicador | Dado | Fonte |
|---|---|---|
| Mercado beleza / cosméticos Brasil (2024) | R$ 45 bilhões | ABIHPEC |
| Crescimento e-commerce beleza | +25% (2023→2024) | NielsenIQ |
| Brasil no ranking mundial de beleza | 4º lugar | Euromonitor |
| Ticket médio online (beleza) | R$ 80–200 | ABIHPEC |
| Zona Leste SP — perfil | Classes C1/C2, alta recorrência de compra | IBGE / DataSP |

**Links de referência:**
[ABIHPEC](https://www.abihpec.org.br/publicacao/panorama-do-setor/) · [ANVISA Cosméticos](https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/cosmeticos) · [Beauty Fair](https://www.beautyfair.com.br)
""")

    with st.expander("2. PLANO DE MARKETING — 4Ps"):
        p1, p2 = st.columns(2)
        if is_pesca:
            p1.markdown("**🎣 Produto**\n\nVaras, molinetes, linhas, iscas artificiais, kit iniciante. Foco em pesca em represa/rio (perfil interior paulista).")
            p1.markdown("**💰 Preço**\n\nCompetitivo com marketplace (−10%), desconto em kit, parcelamento 6×.")
            p2.markdown("**📍 Praça**\n\nLoja física + Mercado Livre + Shopee + WhatsApp Business.")
            p2.markdown("**📣 Promoção**\n\nInstagram (#pesca), grupos WhatsApp de pescadores, YouTube reviews, parceria com clubes locais.")
        else:
            p1.markdown("**💄 Produto**\n\nColoração, tratamento capilar, maquiagem, skincare, perfumaria. Linha afro/crespo em destaque.")
            p1.markdown("**💰 Preço**\n\n10–20% abaixo de farmácias, cartão fidelidade, combos temáticos.")
            p2.markdown("**📍 Praça**\n\nLoja física + Mercado Livre + Shopee + Instagram Shopping + delivery motoboy (raio 5 km).")
            p2.markdown("**📣 Promoção**\n\nTikTok/Instagram (tutoriais), micro-influenciadoras zona leste, Google Meu Negócio, stories promocionais.")

    with st.expander("3. PLANO OPERACIONAL — Layout, Estrutura e Metragem", expanded=False):
        col_planta, col_tabop = st.columns([3, 2])

        with col_planta:
            st.markdown("##### 📐 Planta Baixa — Ponto PUDO (60 m²  |  8m × 7,5m)")

            fig_planta = go.Figure()

            # Zonas principais
            zonas = [
                # x0,y0,x1,y1, fill, borda, label, sublabel
                (0,0,8,1.0,   "#fff8dc","#d97706", "ENTRADA / FACHADA", "porta central — 1,2m"),
                (0,1.0,5,4.0, "#dcfce7","#16a34a", "EXPOSIÇÃO DE PRODUTOS", "20 m²  |  gôndolas e prateleiras"),
                (5,1.0,8,4.0, "#dbeafe","#2563eb", "BALCÃO ATENDIMENTO\n+ CAIXA / PDV", "8 m²"),
                (0,4.0,4,6.5, "#fef3c7","#d97706", "ESTOQUE PRODUTO", f"10 m²  |  {segmento_nome}"),
                (4,4.0,8,6.5, "#ede9fe","#7c3aed", "ESTOQUE PUDO\n(encomendas)", "10 m²  |  giro 24–48h"),
                (0,6.5,5.5,7.5,"#f1f5f9","#64748b","ÁREA COMUM / CIRCULAÇÃO","5 m²"),
                (5.5,6.5,8,7.5,"#e2e8f0","#64748b","BANHEIRO","3 m²"),
            ]
            for x0,y0,x1,y1,fc,bc,lbl,sub in zonas:
                fig_planta.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                    fillcolor=fc, line=dict(color=bc, width=2))
                fig_planta.add_annotation(
                    x=(x0+x1)/2, y=(y0+y1)/2,
                    text=f"<b>{lbl}</b><br><span style='font-size:9px;color:#555'>{sub}</span>",
                    showarrow=False, font=dict(size=9.5), align="center",
                    bgcolor="rgba(255,255,255,0.6)", borderpad=2)

            # Mobiliário — prateleiras parede esquerda (exposição)
            for yi in [1.25, 1.75, 2.25, 2.75, 3.25, 3.65]:
                fig_planta.add_shape(type="rect", x0=0.05, y0=yi, x1=0.35, y1=yi+0.15,
                    fillcolor="#92400e", line=dict(color="#78350f", width=1))

            # Prateleiras parede direita (exposição)
            for yi in [1.25, 1.75, 2.25, 2.75, 3.25]:
                fig_planta.add_shape(type="rect", x0=4.65, y0=yi, x1=4.95, y1=yi+0.15,
                    fillcolor="#92400e", line=dict(color="#78350f", width=1))

            # Gôndola central (exposição)
            fig_planta.add_shape(type="rect", x0=1.5, y0=1.4, x1=1.8, y1=3.7,
                fillcolor="#a16207", line=dict(color="#78350f", width=1))
            fig_planta.add_shape(type="rect", x0=2.8, y0=1.4, x1=3.1, y1=3.7,
                fillcolor="#a16207", line=dict(color="#78350f", width=1))

            # Balcão (L shape)
            fig_planta.add_shape(type="rect", x0=5.1, y0=1.1, x1=7.9, y1=1.6,
                fillcolor="#1e40af", line=dict(color="#1e3a8a", width=1))
            fig_planta.add_shape(type="rect", x0=7.4, y0=1.6, x1=7.9, y1=3.0,
                fillcolor="#1e40af", line=dict(color="#1e3a8a", width=1))

            # Cadeira / operador
            fig_planta.add_shape(type="circle", x0=6.2, y0=1.8, x1=6.7, y1=2.3,
                fillcolor="#93c5fd", line=dict(color="#2563eb", width=1))

            # Prateleiras estoque PUDO (fundo)
            for xi in [4.2, 5.0, 5.8, 6.6, 7.4]:
                fig_planta.add_shape(type="rect", x0=xi, y0=4.15, x1=xi+0.5, y1=6.35,
                    fillcolor="#c4b5fd", line=dict(color="#7c3aed", width=1), opacity=0.6)

            # Prateleiras estoque produto (fundo)
            for xi in [0.2, 1.0, 1.8, 2.6, 3.4]:
                fig_planta.add_shape(type="rect", x0=xi, y0=4.15, x1=xi+0.5, y1=6.35,
                    fillcolor="#fde68a", line=dict(color="#d97706", width=1), opacity=0.7)

            # Porta entrada
            fig_planta.add_shape(type="rect", x0=3.4, y0=-0.05, x1=4.6, y1=0.12,
                fillcolor="#d97706", line=dict(color="#b45309", width=2))
            fig_planta.add_annotation(x=4.0, y=-0.25, text="PORTA 1,2m",
                showarrow=False, font=dict(size=8, color="#b45309"))

            # Cotas externas
            for xi, lbl in [(0,"0m"),(2,"2m"),(4,"4m"),(6,"6m"),(8,"8m")]:
                fig_planta.add_annotation(x=xi, y=-0.5, text=lbl,
                    showarrow=False, font=dict(size=8, color="#666"))
            for yi, lbl in [(0,"0m"),(1.5,"1,5m"),(3,"3m"),(4.5,"4,5m"),(6,"6m"),(7.5,"7,5m")]:
                fig_planta.add_annotation(x=-0.45, y=yi, text=lbl,
                    showarrow=False, font=dict(size=8, color="#666"))

            # Legenda mobiliário
            fig_planta.add_annotation(x=4.0, y=7.9,
                text="<b>Legenda:</b>  🟫 Prateleiras/Gôndolas  🔵 Balcão  🟣 Rack PUDO  🟡 Rack Produto",
                showarrow=False, font=dict(size=8.5), align="center")

            fig_planta.update_layout(
                height=480,
                plot_bgcolor="white", paper_bgcolor="white",
                showlegend=False,
                margin=dict(l=30, r=10, t=20, b=30),
                xaxis=dict(range=[-0.6, 8.5], showgrid=False, zeroline=False,
                           showticklabels=False, fixedrange=True),
                yaxis=dict(range=[-0.7, 8.1], showgrid=False, zeroline=False,
                           showticklabels=False, scaleanchor="x", fixedrange=True),
            )
            st.plotly_chart(fig_planta, use_container_width=True)

        with col_tabop:
            st.markdown("##### Zonas e Metragem")
            st.markdown(f"""
| Zona | Área | Uso |
|---|---|---|
| Exposição produtos | 20 m² | Gôndolas + prateleiras parede |
| Balcão + caixa | 8 m² | Atendimento, PDV, embalagem |
| Estoque PUDO | 10 m² | Encomendas giro 24–48h |
| Estoque produto | 10 m² | {segmento_nome} |
| Circulação | 5 m² | Corredor cliente |
| Banheiro | 3 m² | Uso interno |
| Entrada/fachada | 4 m² | Vitrine e acesso |
| **TOTAL** | **60 m²** | |
""")
            st.markdown("##### Mobiliário Mínimo")
            st.markdown("""
| Item | Qtd | Estimativa |
|---|---|---|
| Prateleiras parede (2m) | 8 un | R$ 2.400 |
| Gôndola dupla face | 2 un | R$ 1.600 |
| Balcão L (vidro) | 1 un | R$ 1.800 |
| Rack estoque PUDO | 3 un | R$ 900 |
| Rack estoque produto | 3 un | R$ 900 |
| Computador + impressora | 1 set | R$ 3.500 |
| Balança (até 30kg) | 1 un | R$ 350 |
| Câmeras (4 pontos) | 1 kit | R$ 1.800 |
| Ar-condicionado 9.000 BTU | 1 un | R$ 2.800 |
| **Total Mobiliário** | | **≈ R$ 16.050** |
""")
            st.markdown("##### Horário e Operação")
            st.markdown("""
- **Seg–Sex:** 08h00 às 19h00
- **Sábado:** 08h00 às 14h00
- **Funcionários:** 1 titular + 1 atendente meio período
- **Sistemas:** [Bling ERP](https://www.bling.com.br) · [Melhor Envio](https://www.melhorenvio.com.br)
- **PUDO credenciamento:** [Correios](https://www.correios.com.br/solucoes-empresariais/agentes-correios) · [Jadlog](https://www.jadlog.com.br/jadlog/pickup) · [Pegaki](https://www.pegaki.com.br/seja-um-ponto)
""")

    with st.expander("4. SEGMENTO PUDO — Detalhamento Operacional e Modelo de Receita"):
        pa, pb = st.columns(2)
        with pa:
            st.markdown("##### O que é o PUDO e como funciona")
            st.markdown("""
**PUDO (Pick-Up & Drop-Off)** é um ponto físico credenciado por transportadoras e marketplaces para que o consumidor retire ou devolva encomendas sem depender de horário de Correios.

**Fluxo de Retirada:**
```
Transportadora entrega pacote no ponto
       ↓
Registro no sistema + etiqueta de localização
       ↓
Notificação automática ao destinatário (WhatsApp/SMS)
       ↓
Cliente apresenta código QR ou CPF
       ↓
Entrega + assinatura digital
       ↓
Comissão registrada automaticamente
```

**Fluxo de Devolução (Logística Reversa):**
```
Cliente chega com produto + código de devolução
       ↓
Validação no sistema do marketplace
       ↓
Acondicionamento + etiqueta de retorno
       ↓
Coleta pela transportadora (diária)
       ↓
Comissão registrada
```
""")
            st.markdown("##### Transportadoras — Comissões de Mercado")
            st.markdown("""
| Parceiro | Comissão / Pacote | Coleta | Integração |
|---|---|---|---|
| Correios Agente | R$ 2,50–4,00 | Diária | Sistema Correios |
| Jadlog Pickup | R$ 3,00–5,00 | Diária | App Jadlog |
| Pegaki | R$ 3,00–4,50 | Sob demanda | API Pegaki |
| Shopee Drops | R$ 2,00–3,50 | Diária | App Shopee |
| Mercado Envios | R$ 3,50–5,50 | Diária | App ML |
| Total Express | R$ 3,00–4,00 | Diária | Sistema TE |
""")

        with pb:
            st.markdown("##### Capacidade e Volumetria")
            st.markdown(f"""
| Métrica | Mínimo | Meta M6 | Referência Madura |
|---|---|---|---|
| Pacotes PUDO / dia | 5–10 | 15–20 | 40–60 |
| Pacotes PUDO / mês | 100–200 | 300–500 | 1.000–1.500 |
| Devoluções / mês | 10–20 | 60–100 | 200–400 |
| Fulfilment / mês | 5–10 | 40–60 | 100–200 |
| Capacidade armazenagem simultânea | 30 pacotes | 80 pacotes | 200 pacotes |
| Giro médio por pacote | 1–2 dias | 1,5 dias | 1 dia |

**Piso garantido (configuração atual):**
- Receita PUDO: **R$ {rec_pudo_m:,.0f}/mês**
- Receita Reversa: **R$ {rec_rev_m:,.0f}/mês**
- Receita Fulfilment: **R$ {rec_full_m:,.0f}/mês**
- **Base total PUDO: R$ {rec_log_base:,.0f}/mês** ← independe das vendas de produto
""".replace(",","."))

            st.markdown("##### Requisitos para Credenciamento")
            st.markdown("""
| Requisito | Detalhe |
|---|---|
| CNPJ ativo | MEI ou ME — qualquer regime |
| Ponto físico | Endereço comercial com alvará |
| Conexão internet | Mínimo 50 Mbps estável |
| Computador + impressora | Térmica para etiquetas |
| Câmera de segurança | Mínimo 1 câmera no balcão |
| Horário mínimo | 6h/dia, 5 dias/semana |
| Seguro básico | Recomendado pelas transportadoras |

**Links de cadastro:**
[Correios](https://www.correios.com.br/solucoes-empresariais/agentes-correios) · [Jadlog](https://www.jadlog.com.br/jadlog/pickup) · [Pegaki](https://www.pegaki.com.br/seja-um-ponto) · [Shopee](https://shopee.com.br/m/shopee-drops) · [ML Envios](https://www.mercadolivre.com.br/agencias)
""")

    with st.expander("5. PLANO FINANCEIRO — CAPEX e OPEX"):
        cg1, cg2 = st.columns(2)
        cg1.markdown(f"""
**CAPEX — Investimento Inicial**

| Item | Valor |
|---|---|
| Obra / Reforma | R$ {capex_obra:,.0f} |
| Equipamentos + TI + Segurança | R$ {capex_equip:,.0f} |
| Estoque inicial | R$ {capex_est:,.0f} |
| Marketing inicial | R$ {capex_mkt_i:,.0f} |
| Abertura empresa | R$ {capex_aber:,.0f} |
| Capital de giro ({meses_cg}m) | R$ {opex_fixo*meses_cg:,.0f} |
| **TOTAL** | **R$ {capex_total:,.0f}** |
""".replace(",","."))
        cg2.markdown(f"""
**OPEX — Custo Fixo Mensal**

| Item | Valor |
|---|---|
| Aluguel + Condomínio | R$ {aluguel+condominio:,.0f} |
| Pessoal + Encargos | R$ {salarios+enc_val:,.0f} |
| Energia + Internet | R$ {energia+internet:,.0f} |
| Marketing / ADS | R$ {mkt_mensal:,.0f} |
| Contador + ERP | R$ {contador+sistema_erp:,.0f} |
| Embalagens + Seguros + Banco | R$ {embalagens+seguros+taxas_banco:,.0f} |
| **TOTAL FIXO** | **R$ {opex_fixo:,.0f}** |
""".replace(",","."))

    with st.expander("6. PLANO DE AÇÃO — Primeiros 90 dias"):
        st.markdown("""
| Semana | Ações |
|---|---|
| 1–2 | Definir ponto, assinar contrato, dar entrada na obra |
| 3–4 | Abrir empresa (MEI/ME), conta PJ, contratar contador |
| 5–6 | Credenciar 2 transportadoras PUDO, instalar sistemas (ERP + câmeras) |
| 7–8 | Comprar estoque inicial, montar loja, fotografar produtos |
| 9–10 | Cadastrar produtos nos marketplaces, configurar WhatsApp Business |
| 11–12 | Soft opening — convidar primeiros clientes, coletar avaliações |
| 13+ | Analisar primeiros dados, ajustar mix de produtos, escalar ADS |

**Regulação e licenças:** [Portal Empreendedor](https://www.gov.br/empresas-e-negocios/pt-br/empreendedor) · [JUCESP](https://www.jucesp.sp.gov.br) · [Alvará SP](https://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos)
""")

# ── helpers drawing ──────────────────────────────────────────────────────────
TIPOS_ZONA_G = {
    "Balcão / Caixa":      {"cor": "#bfdbfe", "borda": "#2563eb", "icone": "🔵"},
    "Exposição / Vitrine": {"cor": "#bbf7d0", "borda": "#16a34a", "icone": "🟢"},
    "Estoque PUDO":        {"cor": "#ddd6fe", "borda": "#7c3aed", "icone": "🟣"},
    "Estoque Produto":     {"cor": "#fef08a", "borda": "#ca8a04", "icone": "🟡"},
    "Prateleira Parede":   {"cor": "#fed7aa", "borda": "#ea580c", "icone": "🟠"},
    "Gôndola Central":     {"cor": "#d1fae5", "borda": "#059669", "icone": "🟩"},
    "Banheiro":            {"cor": "#e2e8f0", "borda": "#64748b", "icone": "⬜"},
    "Entrada / Fachada":   {"cor": "#fef9c3", "borda": "#d97706", "icone": "🚪"},
    "Circulação":          {"cor": "#f8fafc", "borda": "#94a3b8", "icone": "➡️"},
    "Outro":               {"cor": "#fce7f3", "borda": "#be185d", "icone": "🔴"},
}

TEMPLATES_G = {
    "45 m² — Linear (9×5m)": {
        "lw": 9.0, "lh": 5.0,
        "desc": "Ideal para lojas estreitas em corredor. PUDO na frente, estoque ao fundo.",
        "zonas": [
            ("Entrada / Fachada",   0,0,9,0.8),
            ("Balcão / Caixa",      6,0.8,9,3.5),
            ("Exposição / Vitrine", 0,0.8,6,3.5),
            ("Estoque PUDO",        4.5,3.5,9,5),
            ("Estoque Produto",     0,3.5,4.5,5),
        ],
    },
    "60 m² — PUDO Front (8×7.5m)": {
        "lw": 8.0, "lh": 7.5,
        "desc": "Balcão PUDO na entrada, produto ao fundo. Maximiza visibilidade do serviço.",
        "zonas": [
            ("Entrada / Fachada",   0,0,8,1),
            ("Balcão / Caixa",      5,1,8,4),
            ("Exposição / Vitrine", 0,1,5,4),
            ("Estoque Produto",     0,4,4,6.5),
            ("Estoque PUDO",        4,4,8,6.5),
            ("Circulação",          0,6.5,5.5,7.5),
            ("Banheiro",            5.5,6.5,8,7.5),
        ],
    },
    "60 m² — Loja em L (10×6m)": {
        "lw": 10.0, "lh": 6.0,
        "desc": "Formato L — produto ocupa a ala longa, PUDO na ala curta. Bom para esquinas.",
        "zonas": [
            ("Entrada / Fachada",   0,0,10,0.8),
            ("Exposição / Vitrine", 0,0.8,7,3.5),
            ("Balcão / Caixa",      7,0.8,10,3.5),
            ("Gôndola Central",     2,1.2,2.5,3.2),
            ("Gôndola Central",     4.5,1.2,5,3.2),
            ("Estoque PUDO",        5,3.5,10,6),
            ("Estoque Produto",     0,3.5,5,6),
            ("Banheiro",            8.5,3.5,10,5),
        ],
    },
    "80 m² — Serviços + Varejo (10×8m)": {
        "lw": 10.0, "lh": 8.0,
        "desc": "Separação clara entre área de serviços (PUDO/logística) e varejo. Ideal para alto volume.",
        "zonas": [
            ("Entrada / Fachada",   0,0,10,0.8),
            ("Balcão / Caixa",      6.5,0.8,10,4),
            ("Exposição / Vitrine", 0,0.8,6.5,4),
            ("Gôndola Central",     1.5,1.3,2,3.7),
            ("Gôndola Central",     3.5,1.3,4,3.7),
            ("Gôndola Central",     5.5,1.3,6,3.7),
            ("Estoque PUDO",        5,4,10,7.5),
            ("Estoque Produto",     0,4,5,7.5),
            ("Banheiro",            0,7.5,2.5,8),
            ("Circulação",          2.5,7.5,10,8),
        ],
    },
    "100 m² — Hub Logístico (12.5×8m)": {
        "lw": 12.5, "lh": 8.0,
        "desc": "Para alto volume PUDO + loja completa. Zona de triagem separada, estoque grande.",
        "zonas": [
            ("Entrada / Fachada",   0,0,12.5,1),
            ("Balcão / Caixa",      8,1,12.5,4),
            ("Exposição / Vitrine", 0,1,8,4.5),
            ("Gôndola Central",     2,1.5,2.5,4),
            ("Gôndola Central",     4.5,1.5,5,4),
            ("Gôndola Central",     6.5,1.5,7,4),
            ("Estoque PUDO",        7,4,12.5,7.5),
            ("Estoque Produto",     0,4.5,7,7.5),
            ("Banheiro",            10.5,7.5,12.5,8),
            ("Circulação",          0,7.5,10.5,8),
        ],
    },
    "Em branco": {"lw": 8.0, "lh": 7.5, "desc": "", "zonas": []},
}

def render_planta(zonas, lw, lh, selected_idx=None, height=520):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=0, x1=lw, y1=lh,
        fillcolor="#f8fafc", line=dict(color="#1e293b", width=3))
    for xi in [i*0.5 for i in range(int(lw/0.5)+2)]:
        fig.add_shape(type="line", x0=xi, y0=0, x1=xi, y1=lh,
            line=dict(color="#e2e8f0", width=0.4 if xi%1 else 0.9, dash="dot"))
    for yi in [i*0.5 for i in range(int(lh/0.5)+2)]:
        fig.add_shape(type="line", x0=0, y0=yi, x1=lw, y1=yi,
            line=dict(color="#e2e8f0", width=0.4 if yi%1 else 0.9, dash="dot"))
    for xi in range(int(lw)+1):
        fig.add_annotation(x=xi, y=-0.38, text=f"{xi}m",
            showarrow=False, font=dict(size=8, color="#64748b"))
    for yi in range(int(lh)+1):
        fig.add_annotation(x=-0.42, y=yi, text=f"{yi}m",
            showarrow=False, font=dict(size=8, color="#64748b"))
    for i, z in enumerate(zonas):
        cfg  = TIPOS_ZONA_G.get(z["tipo"], TIPOS_ZONA_G["Outro"])
        area = (z["x1"]-z["x0"])*(z["y1"]-z["y0"])
        cx   = (z["x0"]+z["x1"])/2
        cy   = (z["y0"]+z["y1"])/2
        borda = "#f59e0b" if i == selected_idx else cfg["borda"]
        lw_b  = 3.5       if i == selected_idx else 1.8
        fig.add_shape(type="rect",
            x0=z["x0"], y0=z["y0"], x1=z["x1"], y1=z["y1"],
            fillcolor=cfg["cor"], line=dict(color=borda, width=lw_b), opacity=0.92)
        fig.add_annotation(x=cx, y=cy+0.13,
            text=f"<b>{z['nome']}</b>",
            showarrow=False, font=dict(size=9.5), align="center",
            bgcolor="rgba(255,255,255,0.75)", borderpad=2)
        fig.add_annotation(x=cx, y=cy-0.16,
            text=f"{z['x1']-z['x0']:.1f}×{z['y1']-z['y0']:.1f}m = {area:.1f}m²",
            showarrow=False, font=dict(size=8, color="#555"), align="center")
    area_usada = sum((z["x1"]-z["x0"])*(z["y1"]-z["y0"]) for z in zonas)
    total = lw*lh
    fig.update_layout(
        height=height, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, margin=dict(l=38, r=10, t=36, b=38),
        title=dict(
            text=f"Área total: {total:.0f} m²  |  Ocupado: {area_usada:.1f} m² ({area_usada/total*100:.0f}%)  |  Livre: {total-area_usada:.1f} m²",
            font=dict(size=11, color="#475569"), x=0.5),
        xaxis=dict(range=[-0.65, lw+0.3], showgrid=False, zeroline=False,
                   showticklabels=False, fixedrange=True),
        yaxis=dict(range=[-0.65, lh+0.4], showgrid=False, zeroline=False,
                   showticklabels=False, scaleanchor="x", fixedrange=True),
    )
    return fig

# ════════════════════════════════════════════════
# TAB 5 — DESENHO DA ESTRUTURA
# ════════════════════════════════════════════════
with t_draw:
    # ── session state
    for k, v in [("zonas",[]),("lw",8.0),("lh",7.5),("sel_idx",None)]:
        if k not in st.session_state:
            st.session_state[k] = v

    # ── Galeria de layouts sugeridos
    with st.expander("💡 Layouts Sugeridos — clique para carregar", expanded=True):
        st.markdown("Escolha o modelo que melhor se encaixa no seu espaço e objetivo:")
        gcols = st.columns(5)
        for gi, (nome_t, tdata) in enumerate(TEMPLATES_G.items()):
            with gcols[gi % 5]:
                # mini preview
                mfig = render_planta(
                    [{"tipo": t,"nome": t,"x0":x0,"y0":y0,"x1":x1,"y1":y1}
                     for t,x0,y0,x1,y1 in tdata["zonas"]],
                    tdata["lw"], tdata["lh"], height=160)
                mfig.update_layout(
                    title=None, margin=dict(l=0,r=0,t=0,b=0),
                    xaxis=dict(showticklabels=False, fixedrange=True),
                    yaxis=dict(showticklabels=False, fixedrange=True),
                )
                st.plotly_chart(mfig, use_container_width=True, key=f"prev_{gi}")
                st.caption(f"**{nome_t}**")
                if tdata["desc"]:
                    st.caption(tdata["desc"])
                if st.button("Usar este", key=f"use_{gi}", use_container_width=True):
                    st.session_state.zonas = [
                        {"tipo":t,"nome":t,"x0":x0,"y0":y0,"x1":x1,"y1":y1}
                        for t,x0,y0,x1,y1 in tdata["zonas"]
                    ]
                    st.session_state.lw = tdata["lw"]
                    st.session_state.lh = tdata["lh"]
                    st.session_state.sel_idx = None
                    st.rerun()

    st.divider()

    # ── Editor principal
    left, mid = st.columns([1, 2.4])

    with left:
        st.markdown("#### 📐 Controles")

        # Dimensões
        st.markdown("**Imóvel**")
        c1, c2 = st.columns(2)
        st.session_state.lw = c1.number_input("Largura m", 3.0, 40.0,
            float(st.session_state.lw), 0.5, key="inp_lw2")
        st.session_state.lh = c2.number_input("Profund. m", 3.0, 40.0,
            float(st.session_state.lh), 0.5, key="inp_lh2")

        st.divider()

        # ── Selecionar e editar zona existente
        if st.session_state.zonas:
            st.markdown("**✏️ Editar zona existente**")
            nomes_sel = [f"{i+1}. {z['nome']}" for i, z in enumerate(st.session_state.zonas)]
            sel_label = st.selectbox("Selecionar zona", ["— nenhuma —"] + nomes_sel, key="sel_label")
            sel_idx = None
            if sel_label != "— nenhuma —":
                sel_idx = int(sel_label.split(".")[0]) - 1
                st.session_state.sel_idx = sel_idx

            if sel_idx is not None:
                z = st.session_state.zonas[sel_idx]
                z["nome"]  = st.text_input("Rótulo",  z["nome"],  key="ed_nome")
                z["tipo"]  = st.selectbox("Tipo", list(TIPOS_ZONA_G.keys()),
                    index=list(TIPOS_ZONA_G.keys()).index(z["tipo"])
                    if z["tipo"] in TIPOS_ZONA_G else 0, key="ed_tipo")

                st.markdown("**Mover (passo 0,5 m)**")
                mc = st.columns(3)
                larg = z["x1"]-z["x0"]; prof = z["y1"]-z["y0"]
                if mc[1].button("⬆", key="mv_u", use_container_width=True):
                    z["y0"]+=0.5; z["y1"]+=0.5; st.rerun()
                if mc[0].button("⬅", key="mv_l", use_container_width=True):
                    z["x0"]-=0.5; z["x1"]-=0.5; st.rerun()
                mc[1].markdown("<div style='text-align:center;font-size:18px'>✛</div>",
                               unsafe_allow_html=True)
                if mc[2].button("➡", key="mv_r", use_container_width=True):
                    z["x0"]+=0.5; z["x1"]+=0.5; st.rerun()
                if mc[1].button("⬇", key="mv_d", use_container_width=True):
                    z["y0"]-=0.5; z["y1"]-=0.5; st.rerun()

                st.markdown("**Redimensionar (passo 0,5 m)**")
                rc = st.columns(2)
                if rc[0].button("← Largura −", key="rs_wm", use_container_width=True) and larg>0.5:
                    z["x1"]-=0.5; st.rerun()
                if rc[1].button("Largura + →", key="rs_wp", use_container_width=True):
                    z["x1"]+=0.5; st.rerun()
                if rc[0].button("↑ Profund. −", key="rs_hm", use_container_width=True) and prof>0.5:
                    z["y1"]-=0.5; st.rerun()
                if rc[1].button("Profund. + ↓", key="rs_hp", use_container_width=True):
                    z["y1"]+=0.5; st.rerun()

                st.markdown("**Posição precisa**")
                pc1, pc2 = st.columns(2)
                nx0 = pc1.number_input("X início", 0.0, 40.0, float(z["x0"]), 0.5, key="px0")
                ny0 = pc1.number_input("Y início", 0.0, 40.0, float(z["y0"]), 0.5, key="py0")
                nx1 = pc2.number_input("X fim",    0.0, 40.0, float(z["x1"]), 0.5, key="px1")
                ny1 = pc2.number_input("Y fim",    0.0, 40.0, float(z["y1"]), 0.5, key="py1")
                if nx1>nx0 and ny1>ny0:
                    z["x0"],z["y0"],z["x1"],z["y1"] = nx0,ny0,nx1,ny1

                if st.button("🗑 Remover esta zona", key="del_sel", use_container_width=True):
                    st.session_state.zonas.pop(sel_idx)
                    st.session_state.sel_idx = None
                    st.rerun()

        st.divider()

        # ── Adicionar nova zona
        st.markdown("**➕ Nova zona**")
        with st.form("form_add", clear_on_submit=True):
            tipo_n = st.selectbox("Tipo", list(TIPOS_ZONA_G.keys()), key="f_tipo")
            nome_n = st.text_input("Rótulo", placeholder="ex: Balcão Principal", key="f_nome")
            a1, a2 = st.columns(2)
            ax0 = a1.number_input("X início", 0.0, 40.0, 0.0, 0.5, key="f_x0")
            ay0 = a1.number_input("Y início", 0.0, 40.0, 0.0, 0.5, key="f_y0")
            ax1 = a2.number_input("X fim",    0.0, 40.0, 2.0, 0.5, key="f_x1")
            ay1 = a2.number_input("Y fim",    0.0, 40.0, 2.0, 0.5, key="f_y1")
            if st.form_submit_button("Adicionar zona", use_container_width=True):
                if ax1 > ax0 and ay1 > ay0:
                    st.session_state.zonas.append({
                        "tipo": tipo_n, "nome": nome_n or tipo_n,
                        "x0": ax0, "y0": ay0, "x1": ax1, "y1": ay1,
                    })
                    st.rerun()

        if st.session_state.zonas:
            if st.button("🗑 Limpar tudo", use_container_width=True, key="clear_all"):
                st.session_state.zonas = []
                st.session_state.sel_idx = None
                st.rerun()

    with mid:
        st.markdown("#### 🏗 Planta Baixa")
        LW = float(st.session_state.lw)
        LH = float(st.session_state.lh)
        sel = st.session_state.get("sel_idx")

        fig_d = render_planta(st.session_state.zonas, LW, LH, selected_idx=sel, height=560)
        st.plotly_chart(fig_d, use_container_width=True)

        # Legenda
        leg_cols = st.columns(5)
        for li, (tipo, cfg) in enumerate(TIPOS_ZONA_G.items()):
            leg_cols[li % 5].markdown(
                f"<span style='background:{cfg['cor']};border:1px solid {cfg['borda']};"
                f"padding:2px 7px;border-radius:4px;font-size:10px'>"
                f"{cfg['icone']} {tipo}</span>", unsafe_allow_html=True)

        # Tabela
        if st.session_state.zonas:
            st.markdown("<br>", unsafe_allow_html=True)
            rows_z = []
            for z in st.session_state.zonas:
                a = round((z["x1"]-z["x0"])*(z["y1"]-z["y0"]), 2)
                rows_z.append({
                    "Zona": z["nome"], "Tipo": z["tipo"],
                    "Posição": f"({z['x0']:.1f},{z['y0']:.1f})→({z['x1']:.1f},{z['y1']:.1f})",
                    "Dim": f"{z['x1']-z['x0']:.1f}m × {z['y1']-z['y0']:.1f}m",
                    "Área m²": a,
                })
            df_z = pd.DataFrame(rows_z)
            st.dataframe(df_z, use_container_width=True, hide_index=True)

st.divider()
st.caption("📦 PUDO Vila Carrão — Plano de Negócio v4.0 | Dashboard · Financeiro · DRE · Plano · Desenho")
