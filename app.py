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
    .badge-lar    { background: #ffedd5; color: #c2410c; }
    .badge-retro  { background: #ede9fe; color: #6d28d9; }
    .badge-pudo   { background: #dbeafe; color: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Parâmetros")

    modelo = st.radio("Modelo de Negócio", [
        "📦🐟  PUDO + Pesca",
        "📦🏠  PUDO + Itens para o Lar",
        "📦🎮  PUDO + HD Jogos Retro",
    ], index=0)
    if "Pesca" in modelo:      segmento = "pesca"
    elif "Lar" in modelo:      segmento = "lar"
    else:                      segmento = "retro"
    is_pesca = segmento == "pesca"  # mantido por compatibilidade
    SEG = {
        "pesca": dict(label="🐟 Pesca",         nome="Pesca Esportiva",
                      badge="badge-pesca", accent="#16a34a", cor_sec="green",
                      chart="#16a34a",   card_bg="#f0fdf4", card_bd="#16a34a", card_txt="#15803d",
                      itens=70, ticket=180., marg=50, capex_est=8000),
        "lar":   dict(label="🏠 Lar",           nome="Itens para o Lar",
                      badge="badge-lar",   accent="#ea580c", cor_sec="orange",
                      chart="#ea580c",   card_bg="#fff7ed", card_bd="#ea580c", card_txt="#c2410c",
                      itens=90, ticket=95.,  marg=45, capex_est=6000),
        "retro": dict(label="🎮 HD Retro",      nome="HD para Jogos Retro",
                      badge="badge-retro", accent="#6d28d9", cor_sec="purple",
                      chart="#6d28d9",   card_bg="#f5f3ff", card_bd="#6d28d9", card_txt="#5b21b6",
                      itens=40, ticket=220., marg=55, capex_est=10000),
    }[segmento]
    accent = SEG["accent"]

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
    st.markdown(f"#### {SEG['label']} — Produto")
    prod_itens  = st.number_input("Itens / mês (meta M6)",  0, 5000,  SEG["itens"],  5)
    prod_ticket = st.number_input("Ticket médio (R$)",     0.0,2000., SEG["ticket"], 10.)
    prod_marg   = st.slider("Margem bruta (%)", 0, 100, SEG["marg"])
    capex_est   = st.number_input("Estoque inicial (R$)",   0, 200000, SEG["capex_est"], 500)

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
segmento_label = SEG["label"]
cor_badge      = SEG["badge"]

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
t_dash, t_fin, t_cont, t_plano, t_draw, t_ctrl, t_cred, t_adm = st.tabs([
    "🎯  Dashboard Executivo",
    "💰  Financeiro",
    "📊  Contabilidade (DRE)",
    "📋  Plano de Negócio",
    "✏️  Desenho da Estrutura",
    "📅  Controle Mensal",
    "🏢  Credenciamento PUDO",
    "🗂️  Gestão Operacional",
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
        cores  = ["#2563eb","#7c3aed","#0d9488", SEG["chart"]]
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
    segmento_nome = SEG["nome"]
    cor_sec       = SEG["cor_sec"]
    emoji_s       = SEG["label"].split()[0]

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
        "Segmentos de Cliente": {
            "pesca":  "• Pescadores zona leste (masc. 25–55 anos)\n• Compradores online s/ endereço fixo\n• Vendedores de marketplace (fulfilment)\n• Clubes e grupos de pesca da região",
            "lar":    "• Famílias classes C/B (25–55 anos)\n• Compradores online s/ endereço fixo\n• Vendedores de marketplace (fulfilment)\n• Pequenos comerciantes locais",
            "retro":  "• Gamers retro (masc. 20–40 anos, A/B)\n• Compradores online s/ endereço fixo\n• Revendedores de eletrônicos\n• Colecionadores de games",
        }[segmento],
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
        if segmento == "pesca":
            st.markdown("""
| Indicador | Dado | Fonte |
|---|---|---|
| Mercado pesca esportiva Brasil (2024) | R$ 3,5 bilhões | ABPESCA / Sebrae |
| Crescimento anual estimado | 12% a.a. | Sebrae Agro |
| Pescadores ativos no Brasil | ~35 milhões | IBAMA |
| Ticket médio online (pesca) | R$ 150–350 | Mercado Livre |
| Sazonalidade alta | Março–Setembro | Calendário IBAMA SP |
| Zona Leste SP — perfil | Classes B2/C1, forte comunidade de lazer | IBGE / DataSP |

**Links:** [ABPESCA](https://www.abpesca.com.br) · [Sebrae Pesca](https://www.sebrae.com.br/sites/PortalSebrae/artigos/pesca-esportiva) · [MPA](https://www.gov.br/agricultura/pt-br/assuntos/aquicultura-e-pesca)
""")
        elif segmento == "lar":
            st.markdown("""
| Indicador | Dado | Fonte |
|---|---|---|
| Mercado utilidades domésticas Brasil (2024) | R$ 80 bilhões | IEMI / ABCasa |
| Crescimento e-commerce casa/decoração | +18% a.a. | ABComm |
| Ticket médio online (lar) | R$ 60–180 | Mercado Livre |
| Perfil do comprador | Famílias classes C/B, 25–55 anos | IBGE |
| Sazonalidade alta | Outubro–Janeiro (Natal + Ano Novo) | ABComm |
| Zona Leste SP — perfil | Alta densidade familiar, classe trabalhadora | IBGE / DataSP |

**Links:** [ABCasa](https://www.abcasafeira.com.br) · [IEMI](https://www.iemi.com.br) · [ABComm](https://www.abcomm.org.br) · [Mercado Livre Lar](https://www.mercadolivre.com.br/c/casa)
""")
        else:
            st.markdown("""
| Indicador | Dado | Fonte |
|---|---|---|
| Mercado games Brasil (2024) | R$ 10 bilhões | Abragames |
| Crescimento retro gaming global | ~15% a.a. | Newzoo |
| Ticket médio HD/SSD configurado | R$ 120–500 | Mercado Livre |
| Perfil do comprador | Masculino 20–40 anos, classes A/B | Abragames |
| Margem produto configurado vs bruto | +30–40% extra | Estimativa |
| Zona Leste SP — perfil | Alta concentração de gamers urbanos | Abragames |

**Links:** [Abragames](https://www.abragames.org) · [Mercado Livre Games](https://www.mercadolivre.com.br/c/videogames) · [Retro Gaming BR (grupos)](https://www.facebook.com/groups/retrogamingbrasil)
""")

    with st.expander("2. PLANO DE MARKETING — 4Ps"):
        p1, p2 = st.columns(2)
        if segmento == "pesca":
            p1.markdown("**🎣 Produto**\n\nVaras, molinetes, linhas, iscas artificiais, kit iniciante. Foco em pesca em represa/rio (perfil interior paulista).")
            p1.markdown("**💰 Preço**\n\nCompetitivo com marketplace (−10%), desconto em kit, parcelamento 6×.")
            p2.markdown("**📍 Praça**\n\nLoja física + Mercado Livre + Shopee + WhatsApp Business.")
            p2.markdown("**📣 Promoção**\n\nInstagram (#pesca), grupos WhatsApp de pescadores, YouTube reviews, parceria com clubes locais.")
        elif segmento == "lar":
            p1.markdown("**🏠 Produto**\n\nUtensílios domésticos, organização closet/cozinha, ferramentas, decoração, limpeza premium. Foco em itens de alto giro não encontrados no mercado local.")
            p1.markdown("**💰 Preço**\n\n10–15% abaixo de supermercados e lojas de departamento, combos temáticos (kit cozinha, kit organização), parcelamento 3×.")
            p2.markdown("**📍 Praça**\n\nLoja física + Mercado Livre + Shopee + Americanas + WhatsApp + delivery motoboy (raio 5 km).")
            p2.markdown("**📣 Promoção**\n\nInstagram/Pinterest (fotos ambiente), grupos de mães/donas de casa zona leste, Google Meu Negócio, promoção 'semana do lar'.")
        else:
            p1.markdown("**🎮 Produto**\n\nSSDs/HDDs com sistema RetroBat/Batocera pré-configurado, pendrives retro, Raspberry Pi kits, consoles clone (Anbernic, MiyooPocket), acessórios. Diferencial: produto entregue pronto para jogar.")
            p1.markdown("**💰 Preço**\n\nPrecificação por valor (produto configurado vale mais), preço similar ao Mercado Livre + suporte presencial gratuito. Parcelamento 6×.")
            p2.markdown("**📍 Praça**\n\nLoja física (demonstração ao vivo) + Mercado Livre + Shopee + grupos Telegram/WhatsApp retrogaming.")
            p2.markdown("**📣 Promoção**\n\nYouTube (unboxing + gameplay retro), TikTok, grupos Facebook retro BR, parceria com streamers locais, showcase mensal na loja.")

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

# ════════════════════════════════════════════════
# TAB 6 — CONTROLE MENSAL
# ════════════════════════════════════════════════
with t_ctrl:
    import json, io

    MESES_BR = ["Jan","Fev","Mar","Abr","Mai","Jun",
                "Jul","Ago","Set","Out","Nov","Dez"]

    if "dados_mensais" not in st.session_state:
        st.session_state.dados_mensais = {}

    # ── helpers
    def chave_mes(m, a): return f"{m}/{a}"
    def calcular(d):
        rec_log  = d.get("rec_pudo",0) + d.get("rec_reversa",0) + d.get("rec_full",0)
        rec_prod = d.get("rec_produto",0)
        rec_tot  = rec_log + rec_prod
        cmv      = d.get("cmv",0)
        imp      = d.get("impostos",0)
        desp_fix = (d.get("desp_aluguel",0) + d.get("desp_pessoal",0) +
                    d.get("desp_marketing",0) + d.get("desp_outras",0))
        lucro_br = rec_tot - cmv
        ebitda   = rec_tot - cmv - imp - desp_fix
        lucro_liq= ebitda - d.get("depreciacao",0)
        mg_br    = lucro_br / rec_tot * 100 if rec_tot else 0
        mg_eb    = ebitda   / rec_tot * 100 if rec_tot else 0
        mg_lq    = lucro_liq/ rec_tot * 100 if rec_tot else 0
        return dict(rec_log=rec_log, rec_prod=rec_prod, rec_tot=rec_tot,
                    cmv=cmv, imp=imp, desp_fix=desp_fix,
                    lucro_br=lucro_br, ebitda=ebitda, lucro_liq=lucro_liq,
                    mg_br=mg_br, mg_eb=mg_eb, mg_lq=mg_lq)

    def semaforo(real, meta, inverso=False):
        if meta == 0: return "⚪"
        pct = real / meta
        if inverso:
            if pct <= 1.0: return "🟢"
            if pct <= 1.1: return "🟡"
            return "🔴"
        if pct >= 1.0: return "🟢"
        if pct >= 0.9: return "🟡"
        return "🔴"

    def fmt(v): return f"R$ {v:,.0f}".replace(",",".")
    def fmtp(v): return f"{v:.1f}%"

    # ── Layout
    col_form, col_main = st.columns([1, 2.6])

    with col_form:
        st.markdown("#### 📝 Lançamento Mensal")

        ano_sel = st.number_input("Ano", 2024, 2030, 2025, key="ctrl_ano")
        mes_sel = st.selectbox("Mês", MESES_BR, key="ctrl_mes")
        chave   = chave_mes(mes_sel, ano_sel)

        # Carrega dados existentes ou default
        d0 = st.session_state.dados_mensais.get(chave, {})

        st.markdown("**📦 Receitas PUDO / Logística**")
        r_pudo  = st.number_input("Comissão PUDO (R$)",       0.0,999999.,float(d0.get("rec_pudo",0)),    50., key="r1")
        r_rev   = st.number_input("Logística Reversa (R$)",   0.0,999999.,float(d0.get("rec_reversa",0)), 50., key="r2")
        r_full  = st.number_input("Fulfilment (R$)",           0.0,999999.,float(d0.get("rec_full",0)),    50., key="r3")

        st.markdown(f"**{segmento_label} — Receitas**")
        r_prod  = st.number_input("Receita c/ produto (margem bruta, R$)", 0.0,999999.,float(d0.get("rec_produto",0)), 50., key="r4")
        cmv_r   = st.number_input("CMV — Custo Mercadoria (R$)",           0.0,999999.,float(d0.get("cmv",0)),         50., key="r5")

        st.markdown("**💸 Despesas Reais do Mês**")
        d_alug  = st.number_input("Aluguel + Cond (R$)",    0.0,99999.,float(d0.get("desp_aluguel",   aluguel+condominio)), 50., key="d1")
        d_pess  = st.number_input("Pessoal + Encargos (R$)",0.0,99999.,float(d0.get("desp_pessoal",   salarios+enc_val)),   50., key="d2")
        d_mkt   = st.number_input("Marketing / ADS (R$)",   0.0,99999.,float(d0.get("desp_marketing", mkt_mensal)),         50., key="d3")
        d_out   = st.number_input("Outras despesas (R$)",   0.0,99999.,float(d0.get("desp_outras",
            energia+internet+contador+sistema_erp+embalagens+seguros+taxas_banco)), 50., key="d4")
        imp_r   = st.number_input("Impostos pagos (R$)",    0.0,99999.,float(d0.get("impostos",0)),      50., key="d5")
        dep_r   = st.number_input("Depreciação (R$)",       0.0,99999.,float(d0.get("depreciacao",depreciacao)), 50., key="d6")
        obs_r   = st.text_area("Observações do mês", d0.get("obs",""), height=70, key="obs_r")

        if st.button("💾 Salvar mês", use_container_width=True, type="primary"):
            st.session_state.dados_mensais[chave] = {
                "rec_pudo": r_pudo, "rec_reversa": r_rev, "rec_full": r_full,
                "rec_produto": r_prod, "cmv": cmv_r,
                "desp_aluguel": d_alug, "desp_pessoal": d_pess,
                "desp_marketing": d_mkt, "desp_outras": d_out,
                "impostos": imp_r, "depreciacao": dep_r, "obs": obs_r,
            }
            st.success(f"✅ {chave} salvo!")

        st.divider()

        # Export / Import
        st.markdown("**📤 Exportar / Importar dados**")
        if st.session_state.dados_mensais:
            json_str = json.dumps(st.session_state.dados_mensais, ensure_ascii=False, indent=2)
            st.download_button("⬇ Baixar JSON", json_str,
                file_name="controle_mensal_pudo.json", mime="application/json",
                use_container_width=True)

        up = st.file_uploader("⬆ Carregar JSON salvo", type="json", key="up_json")
        if up:
            try:
                loaded = json.load(up)
                st.session_state.dados_mensais.update(loaded)
                st.success(f"Importados {len(loaded)} meses!")
                st.rerun()
            except Exception:
                st.error("Arquivo inválido.")

    # ── Painel principal
    with col_main:
        dados_todos = st.session_state.dados_mensais

        if not dados_todos:
            st.info("👈 Salve pelo menos um mês para visualizar os dados.")
            st.stop()

        # Ordena meses
        def sort_key(k):
            m, a = k.split("/")
            return int(a)*100 + MESES_BR.index(m)

        chaves_ord = sorted(dados_todos.keys(), key=sort_key)
        idx_atual  = chaves_ord.index(chave) if chave in chaves_ord else len(chaves_ord)-1
        chave_vis  = st.selectbox("Visualizar mês", chaves_ord,
                                   index=idx_atual, key="vis_mes")
        d_cur  = dados_todos[chave_vis]
        calc   = calcular(d_cur)

        # Mês anterior
        idx_v  = chaves_ord.index(chave_vis)
        d_ant  = calcular(dados_todos[chaves_ord[idx_v-1]]) if idx_v > 0 else None
        chave_ant = chaves_ord[idx_v-1] if idx_v > 0 else "—"

        # Projeção (mês 6 do simulador como meta)
        meta_rec  = rec_total_m6
        meta_ebit = ebitda_m6
        meta_liq  = lucro_m6

        # ── SUBTABS
        sd1, sd2, sd3, sd4 = st.tabs([
            "🎯 Fechamento do Mês",
            "📊 DRE Comparativo",
            "📈 Evolução Mensal",
            "🔍 PUDO vs Produto",
        ])

        # ════════ SUBTAB 1 — Fechamento ════════
        with sd1:
            st.markdown(f"### Fechamento — {chave_vis}")

            # KPIs linha 1
            k1,k2,k3 = st.columns(3)
            def kpi_m(col, label, val, ref=None, inv=False, cls=""):
                delta = f" vs {fmt(ref)}" if ref else ""
                smf   = semaforo(val, ref, inv) if ref else ""
                col.markdown(f"""
                <div class="hero-card {cls}">
                  <div class="hero-lbl">{label}</div>
                  <div class="hero-val">{fmt(val)}</div>
                  <div class="hero-sub">{smf} {delta}</div>
                </div>""", unsafe_allow_html=True)

            kpi_m(k1,"Receita Total",       calc["rec_tot"],  meta_rec,  cls="")
            kpi_m(k2,"EBITDA",              calc["ebitda"],   meta_ebit, cls="green" if calc["ebitda"]>0 else "red")
            kpi_m(k3,"Lucro Líquido",       calc["lucro_liq"],meta_liq,  cls="green" if calc["lucro_liq"]>0 else "red")
            st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)
            k4,k5,k6 = st.columns(3)
            kpi_m(k4,"Receita PUDO/Log",    calc["rec_log"],  rec_log_base)
            kpi_m(k5,"Receita Produto",     calc["rec_prod"], rec_prod_m6)
            ant_liq = d_ant["lucro_liq"] if d_ant else None
            kpi_m(k6,"vs Mês Anterior",
                calc["lucro_liq"] - ant_liq if ant_liq is not None else 0,
                cls="green" if (ant_liq is not None and calc["lucro_liq"]>=ant_liq) else "red")

            st.markdown("<br>", unsafe_allow_html=True)
            cg1, cg2 = st.columns(2)

            # Waterfall simplificado (barras)
            with cg1:
                st.markdown('<div class="section-title">Decomposição do Resultado</div>',
                            unsafe_allow_html=True)
                items_wf = {
                    "Rec PUDO":     calc["rec_log"],
                    f"Rec {segmento_label.split()[-1]}": calc["rec_prod"],
                    "Impostos":    -calc["imp"],
                    "CMV":         -calc["cmv"],
                    "Desp Fixas":  -calc["desp_fix"],
                    "Depreciação": -d_cur.get("depreciacao",0),
                    "Lucro Líq":    calc["lucro_liq"],
                }
                cores_wf2 = ["#2563eb","#7c3aed","#ef4444","#ef4444","#ef4444","#f97316",
                             "#16a34a" if calc["lucro_liq"]>=0 else "#dc2626"]
                fig_wf2 = go.Figure(go.Bar(
                    x=list(items_wf.values()), y=list(items_wf.keys()),
                    orientation="h", marker_color=cores_wf2,
                    text=[fmt(abs(v)) for v in items_wf.values()],
                    textposition="outside", cliponaxis=False))
                fig_wf2.add_vline(x=0, line_color="#666", line_width=1.5)
                fig_wf2.update_layout(height=290, plot_bgcolor="white", paper_bgcolor="white",
                    showlegend=False, margin=dict(l=0,r=110,t=10,b=0),
                    xaxis=dict(gridcolor="#f0f0f0", zeroline=False),
                    yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_wf2, use_container_width=True)

            with cg2:
                st.markdown('<div class="section-title">Distribuição da Receita</div>',
                            unsafe_allow_html=True)
                lbs = ["PUDO","Log. Rev.","Fulfilment","Produto"]
                vls = [d_cur.get("rec_pudo",0), d_cur.get("rec_reversa",0),
                       d_cur.get("rec_full",0), d_cur.get("rec_produto",0)]
                fig_pie2 = go.Figure(go.Pie(labels=lbs, values=vls, hole=.45,
                    marker_colors=["#2563eb","#7c3aed","#0d9488",
                                   SEG["chart"]],
                    textinfo="percent+label", textfont_size=10))
                fig_pie2.update_layout(height=250, showlegend=False,
                    paper_bgcolor="white", margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig_pie2, use_container_width=True)

                if d_cur.get("obs"):
                    st.info(f"📝 **Obs:** {d_cur['obs']}")

            # Semáforos vs meta
            st.markdown('<div class="section-title">Semáforo de Desempenho vs Meta</div>',
                        unsafe_allow_html=True)
            metricas_sem = [
                ("Receita Total",   calc["rec_tot"],   meta_rec,   False),
                ("PUDO / Logística",calc["rec_log"],   rec_log_base,False),
                ("Receita Produto", calc["rec_prod"],  rec_prod_m6, False),
                ("EBITDA",          calc["ebitda"],    meta_ebit,   False),
                ("Lucro Líquido",   calc["lucro_liq"], meta_liq,    False),
                ("Custo Total",     calc["desp_fix"]+calc["cmv"]+calc["imp"],
                                    opex_fixo+cmv_prod_m6+imp_m6, True),
            ]
            cols_sem = st.columns(6)
            for ci, (lbl, real, meta_v, inv) in enumerate(metricas_sem):
                smf = semaforo(real, meta_v, inv)
                pct = real/meta_v*100 if meta_v else 0
                cols_sem[ci].markdown(f"""
                <div style="background:white;border-radius:10px;padding:12px;
                     text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.06)">
                  <div style="font-size:22px">{smf}</div>
                  <div style="font-size:10px;color:#666;margin:4px 0">{lbl}</div>
                  <div style="font-size:13px;font-weight:600">{fmt(real)}</div>
                  <div style="font-size:10px;color:#888">Meta: {fmt(meta_v)}</div>
                  <div style="font-size:10px;color:{'#16a34a' if pct>=90 else '#dc2626'}">{pct:.0f}%</div>
                </div>""", unsafe_allow_html=True)

        # ════════ SUBTAB 2 — DRE Comparativo ════════
        with sd2:
            st.markdown(f"### DRE — {chave_vis}  vs  {chave_ant}  vs  Meta (Simulador)")

            # Monta DRE completa
            dre_linhas = [
                ("RECEITA BRUTA TOTAL",            True,  False, "total"),
                ("  Comissão PUDO",                 False, False, "pos"),
                ("  Logística Reversa",             False, False, "pos"),
                ("  Fulfilment",                    False, False, "pos"),
                (f"  Vendas {segmento_label}",      False, False, "pos"),
                ("(−) Impostos",                   False, True,  "neg"),
                ("RECEITA LÍQUIDA",                True,  False, "total"),
                ("(−) CMV",                        False, True,  "neg"),
                ("LUCRO BRUTO",                    True,  False, "total"),
                ("(−) Despesas Operacionais",      False, True,  "neg"),
                ("  Aluguel + Condomínio",          False, True,  "neg"),
                ("  Pessoal + Encargos",            False, True,  "neg"),
                ("  Marketing / ADS",               False, True,  "neg"),
                ("  Outras Despesas",               False, True,  "neg"),
                ("EBITDA",                         True,  False, "result"),
                ("(−) Depreciação",                False, True,  "neg"),
                ("LUCRO LÍQUIDO",                  True,  False, "result"),
                ("Margem Bruta %",                 False, False, "pct"),
                ("Margem EBITDA %",                False, False, "pct"),
                ("Margem Líquida %",               False, False, "pct"),
            ]

            def val_dre(label, d):
                if not d: return 0
                c = calcular(d)
                m = {
                    "RECEITA BRUTA TOTAL":         c["rec_tot"],
                    "  Comissão PUDO":              d.get("rec_pudo",0),
                    "  Logística Reversa":          d.get("rec_reversa",0),
                    "  Fulfilment":                 d.get("rec_full",0),
                    f"  Vendas {segmento_label}":   d.get("rec_produto",0),
                    "(−) Impostos":                -d.get("impostos",0),
                    "RECEITA LÍQUIDA":              c["rec_tot"]-c["imp"],
                    "(−) CMV":                     -c["cmv"],
                    "LUCRO BRUTO":                  c["lucro_br"],
                    "(−) Despesas Operacionais":   -c["desp_fix"],
                    "  Aluguel + Condomínio":      -d.get("desp_aluguel",0),
                    "  Pessoal + Encargos":        -d.get("desp_pessoal",0),
                    "  Marketing / ADS":           -d.get("desp_marketing",0),
                    "  Outras Despesas":           -d.get("desp_outras",0),
                    "EBITDA":                       c["ebitda"],
                    "(−) Depreciação":             -d.get("depreciacao",0),
                    "LUCRO LÍQUIDO":                c["lucro_liq"],
                    "Margem Bruta %":               c["mg_br"],
                    "Margem EBITDA %":              c["mg_eb"],
                    "Margem Líquida %":             c["mg_lq"],
                }
                return m.get(label, 0)

            def val_meta(label):
                m = {
                    "RECEITA BRUTA TOTAL":         rec_total_m6,
                    "  Comissão PUDO":              rec_pudo_m,
                    "  Logística Reversa":          rec_rev_m,
                    "  Fulfilment":                 rec_full_m,
                    f"  Vendas {segmento_label}":   rec_prod_m6,
                    "(−) Impostos":                -imp_m6,
                    "RECEITA LÍQUIDA":              rec_total_m6-imp_m6,
                    "(−) CMV":                     -cmv_prod_m6,
                    "LUCRO BRUTO":                  rec_total_m6-cmv_prod_m6,
                    "(−) Despesas Operacionais":   -opex_fixo,
                    "  Aluguel + Condomínio":      -(aluguel+condominio),
                    "  Pessoal + Encargos":        -(salarios+enc_val),
                    "  Marketing / ADS":           -mkt_mensal,
                    "  Outras Despesas":           -(energia+internet+contador+sistema_erp+embalagens+seguros+taxas_banco),
                    "EBITDA":                       ebitda_m6,
                    "(−) Depreciação":             -depreciacao,
                    "LUCRO LÍQUIDO":                lucro_m6,
                    "Margem Bruta %":               (rec_total_m6-cmv_prod_m6)/rec_total_m6*100 if rec_total_m6 else 0,
                    "Margem EBITDA %":              ebitda_m6/rec_total_m6*100 if rec_total_m6 else 0,
                    "Margem Líquida %":             lucro_m6/rec_total_m6*100 if rec_total_m6 else 0,
                }
                return m.get(label, 0)

            rows_dre = []
            for lbl, bold, neg, tipo in dre_linhas:
                v_cur = val_dre(lbl, d_cur)
                v_ant = val_dre(lbl, dados_todos.get(chave_ant)) if chave_ant != "—" else None
                v_met = val_meta(lbl)
                if tipo == "pct":
                    rows_dre.append({
                        "Item": lbl,
                        chave_vis: f"{v_cur:.1f}%",
                        chave_ant: f"{v_ant:.1f}%" if v_ant is not None else "—",
                        "Meta": f"{v_met:.1f}%",
                        "∆ Meta": f"{v_cur-v_met:+.1f}pp",
                    })
                else:
                    rows_dre.append({
                        "Item": lbl,
                        chave_vis: fmt(v_cur),
                        chave_ant: fmt(v_ant) if v_ant is not None else "—",
                        "Meta": fmt(v_met),
                        "∆ Meta": f"R$ {v_cur-v_met:+,.0f}".replace(",","."),
                    })

            df_dre2 = pd.DataFrame(rows_dre)

            BOLD_ROWS = {"RECEITA BRUTA TOTAL","RECEITA LÍQUIDA","LUCRO BRUTO","EBITDA","LUCRO LÍQUIDO"}

            def estilo_dre(row):
                styles = [""] * len(row)
                lbl = row["Item"]
                if lbl in BOLD_ROWS:
                    styles = ["font-weight:700;background:#f0f4ff"] * len(row)
                try:
                    delta_str = row.get("∆ Meta","0").replace("R$ ","").replace(".","").replace(",",".")
                    dv = float(delta_str.replace("+",""))
                    col_idx = list(row.index).index("∆ Meta")
                    styles[col_idx] = f"color:{'#16a34a' if dv>=0 else '#dc2626'};font-weight:600"
                except: pass
                return styles

            st.dataframe(
                df_dre2.style.apply(estilo_dre, axis=1),
                use_container_width=True, hide_index=True)

            # Gráfico comparativo EBITDA / Lucro
            st.markdown('<div class="section-title">EBITDA e Lucro — Comparativo</div>',
                        unsafe_allow_html=True)
            cats_comp  = [chave_ant, chave_vis, "Meta"]
            ebitdas    = [
                calcular(dados_todos[chave_ant])["ebitda"] if chave_ant!="—" and chave_ant in dados_todos else 0,
                calc["ebitda"], meta_ebit
            ]
            lucros     = [
                calcular(dados_todos[chave_ant])["lucro_liq"] if chave_ant!="—" and chave_ant in dados_todos else 0,
                calc["lucro_liq"], meta_liq
            ]
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(x=cats_comp, y=ebitdas, name="EBITDA",
                marker_color=["#93c5fd","#2563eb","#7c3aed"]))
            fig_comp.add_trace(go.Bar(x=cats_comp, y=lucros, name="Lucro Líquido",
                marker_color=["#86efac","#16a34a","#059669"]))
            fig_comp.add_hline(y=0, line_dash="dot", line_color="#666")
            fig_comp.update_layout(barmode="group", height=260,
                plot_bgcolor="white", paper_bgcolor="white",
                legend=dict(orientation="h", y=-0.25),
                margin=dict(l=0,r=0,t=10,b=0))
            fig_comp.update_yaxes(gridcolor="#f0f0f0")
            st.plotly_chart(fig_comp, use_container_width=True)

        # ════════ SUBTAB 3 — Evolução Mensal ════════
        with sd3:
            st.markdown("### Evolução Mensal — Todos os Meses Lançados")

            if len(dados_todos) < 2:
                st.info("Lance pelo menos 2 meses para ver a evolução.")
            else:
                ev_meses, ev_rec, ev_ebitda, ev_liq, ev_pudo, ev_prod = [],[],[],[],[],[]
                for ch in chaves_ord:
                    d = dados_todos[ch]
                    c = calcular(d)
                    ev_meses.append(ch)
                    ev_rec.append(c["rec_tot"])
                    ev_ebitda.append(c["ebitda"])
                    ev_liq.append(c["lucro_liq"])
                    ev_pudo.append(c["rec_log"])
                    ev_prod.append(c["rec_prod"])

                fig_ev = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=("Receita e Resultado", "Composição da Receita"),
                    vertical_spacing=0.12)

                fig_ev.add_trace(go.Bar(x=ev_meses, y=ev_rec, name="Receita Total",
                    marker_color="#2563eb", opacity=.8), row=1, col=1)
                fig_ev.add_trace(go.Scatter(x=ev_meses, y=ev_ebitda, name="EBITDA",
                    line=dict(color="#7c3aed",width=2.5), mode="lines+markers"), row=1, col=1)
                fig_ev.add_trace(go.Scatter(x=ev_meses, y=ev_liq, name="Lucro Líquido",
                    line=dict(color="#16a34a",width=2.5), mode="lines+markers"), row=1, col=1)
                fig_ev.add_hline(y=meta_liq, line_dash="dash", line_color="#dc2626",
                    annotation_text=f"Meta lucro {fmt(meta_liq)}", row=1, col=1)

                fig_ev.add_trace(go.Bar(x=ev_meses, y=ev_pudo, name="PUDO/Log",
                    marker_color="#2563eb"), row=2, col=1)
                fig_ev.add_trace(go.Bar(x=ev_meses, y=ev_prod, name="Produto",
                    marker_color=SEG["chart"]), row=2, col=1)

                fig_ev.update_layout(barmode="stack", height=520,
                    plot_bgcolor="white", paper_bgcolor="white",
                    legend=dict(orientation="h", y=-0.08),
                    margin=dict(l=0,r=0,t=30,b=0))
                fig_ev.update_yaxes(gridcolor="#f0f0f0")
                st.plotly_chart(fig_ev, use_container_width=True)

                # Tabela resumo
                st.markdown('<div class="section-title">Resumo Acumulado do Período</div>',
                            unsafe_allow_html=True)
                rows_ev = []
                for ch in chaves_ord:
                    d = dados_todos[ch]
                    c = calcular(d)
                    vs_meta_liq = c["lucro_liq"] - meta_liq
                    rows_ev.append({
                        "Mês": ch,
                        "Receita": fmt(c["rec_tot"]),
                        "PUDO/Log": fmt(c["rec_log"]),
                        "Produto": fmt(c["rec_prod"]),
                        "EBITDA": fmt(c["ebitda"]),
                        "Lucro Líq": fmt(c["lucro_liq"]),
                        "Mg Líq%": fmtp(c["mg_lq"]),
                        "∆ vs Meta": fmt(vs_meta_liq),
                    })
                # totais
                rows_ev.append({
                    "Mês": "TOTAL",
                    "Receita": fmt(sum(calcular(dados_todos[c])["rec_tot"] for c in chaves_ord)),
                    "PUDO/Log": fmt(sum(calcular(dados_todos[c])["rec_log"] for c in chaves_ord)),
                    "Produto":  fmt(sum(calcular(dados_todos[c])["rec_prod"] for c in chaves_ord)),
                    "EBITDA":   fmt(sum(calcular(dados_todos[c])["ebitda"] for c in chaves_ord)),
                    "Lucro Líq":fmt(sum(calcular(dados_todos[c])["lucro_liq"] for c in chaves_ord)),
                    "Mg Líq%":  "—",
                    "∆ vs Meta":fmt(sum(calcular(dados_todos[c])["lucro_liq"]-meta_liq for c in chaves_ord)),
                })

                def cor_ev(val):
                    try:
                        v = float(val.replace("R$ ","").replace(".","").replace(",",".").replace("+",""))
                        if v > 0: return "color:#16a34a;font-weight:600"
                        if v < 0: return "color:#dc2626"
                    except: pass
                    return ""

                df_ev = pd.DataFrame(rows_ev)
                st.dataframe(df_ev.style.map(cor_ev, subset=["Lucro Líq","∆ vs Meta"]),
                             use_container_width=True, hide_index=True)

        # ════════ SUBTAB 4 — PUDO vs Produto ════════
        with sd4:
            st.markdown(f"### PUDO vs {segmento_label} — Análise Detalhada")

            if len(dados_todos) == 0:
                st.info("Lance pelo menos 1 mês.")
            else:
                # Radar chart de performance
                c_cur = calcular(d_cur)
                pudo_pct  = c_cur["rec_log"] / c_cur["rec_tot"] * 100 if c_cur["rec_tot"] else 0
                prod_pct  = c_cur["rec_prod"]/ c_cur["rec_tot"] * 100 if c_cur["rec_tot"] else 0

                col_pu, col_pr = st.columns(2)

                with col_pu:
                    st.markdown(f"""
                    <div style="background:#eff6ff;border:2px solid #2563eb;border-radius:12px;padding:20px">
                      <div style="font-size:13px;font-weight:700;color:#1d4ed8;margin-bottom:12px">
                        📦 PUDO + LOGÍSTICA — {chave_vis}</div>
                      <table style="width:100%;font-size:13px">
                        <tr><td style="color:#555">Comissão PUDO</td>
                            <td style="font-weight:600;text-align:right">{fmt(d_cur.get("rec_pudo",0))}</td></tr>
                        <tr><td style="color:#555">Logística Reversa</td>
                            <td style="font-weight:600;text-align:right">{fmt(d_cur.get("rec_reversa",0))}</td></tr>
                        <tr><td style="color:#555">Fulfilment</td>
                            <td style="font-weight:600;text-align:right">{fmt(d_cur.get("rec_full",0))}</td></tr>
                        <tr style="border-top:1px solid #bfdbfe">
                            <td style="font-weight:700">Total PUDO</td>
                            <td style="font-weight:700;text-align:right;color:#1d4ed8">{fmt(c_cur["rec_log"])}</td></tr>
                        <tr><td style="color:#888;font-size:11px">% da receita total</td>
                            <td style="color:#1d4ed8;font-size:11px;text-align:right">{pudo_pct:.1f}%</td></tr>
                        <tr><td style="color:#888;font-size:11px">Margem bruta</td>
                            <td style="color:#1d4ed8;font-size:11px;text-align:right">100% (serviço)</td></tr>
                        <tr><td style="color:#888;font-size:11px">Meta PUDO</td>
                            <td style="color:#888;font-size:11px;text-align:right">{fmt(rec_log_base)}</td></tr>
                        <tr><td style="font-size:11px">∆ vs Meta</td>
                            <td style="font-size:11px;text-align:right;color:{'#16a34a' if c_cur['rec_log']>=rec_log_base else '#dc2626'}">{fmt(c_cur['rec_log']-rec_log_base)}</td></tr>
                      </table>
                    </div>""", unsafe_allow_html=True)

                with col_pr:
                    cor_prod_hex = SEG["card_bg"]
                    cor_bd_hex   = SEG["card_bd"]
                    cor_txt_hex  = SEG["card_txt"]
                    st.markdown(f"""
                    <div style="background:{cor_prod_hex};border:2px solid {cor_bd_hex};border-radius:12px;padding:20px">
                      <div style="font-size:13px;font-weight:700;color:{cor_txt_hex};margin-bottom:12px">
                        {segmento_label} — {chave_vis}</div>
                      <table style="width:100%;font-size:13px">
                        <tr><td style="color:#555">GMV (vendas brutas)</td>
                            <td style="font-weight:600;text-align:right">{fmt(d_cur.get("rec_produto",0)+d_cur.get("cmv",0))}</td></tr>
                        <tr><td style="color:#555">CMV (custo produto)</td>
                            <td style="font-weight:600;text-align:right;color:#dc2626">({fmt(d_cur.get("cmv",0))})</td></tr>
                        <tr style="border-top:1px solid {cor_bd_hex}20">
                            <td style="font-weight:700">Margem Produto</td>
                            <td style="font-weight:700;text-align:right;color:{cor_txt_hex}">{fmt(d_cur.get("rec_produto",0))}</td></tr>
                        <tr><td style="color:#888;font-size:11px">% da receita total</td>
                            <td style="color:{cor_txt_hex};font-size:11px;text-align:right">{prod_pct:.1f}%</td></tr>
                        <tr><td style="color:#888;font-size:11px">Margem bruta %</td>
                            <td style="color:{cor_txt_hex};font-size:11px;text-align:right">
                            {d_cur.get("rec_produto",0)/(d_cur.get("rec_produto",0)+d_cur.get("cmv",1))*100:.1f}%</td></tr>
                        <tr><td style="color:#888;font-size:11px">Meta Produto</td>
                            <td style="color:#888;font-size:11px;text-align:right">{fmt(rec_prod_m6)}</td></tr>
                        <tr><td style="font-size:11px">∆ vs Meta</td>
                            <td style="font-size:11px;text-align:right;color:{'#16a34a' if c_cur['rec_prod']>=rec_prod_m6 else '#dc2626'}">{fmt(c_cur['rec_prod']-rec_prod_m6)}</td></tr>
                      </table>
                    </div>""", unsafe_allow_html=True)

                # Evolução PUDO vs Produto ao longo dos meses
                if len(dados_todos) >= 2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Evolução PUDO vs Produto — Todos os Meses</div>',
                                unsafe_allow_html=True)
                    fig_pvp = go.Figure()
                    meses_p = chaves_ord
                    pudos   = [calcular(dados_todos[c])["rec_log"]  for c in meses_p]
                    prods   = [calcular(dados_todos[c])["rec_prod"] for c in meses_p]
                    lucros2 = [calcular(dados_todos[c])["lucro_liq"]for c in meses_p]

                    fig_pvp.add_trace(go.Bar(x=meses_p, y=pudos, name="PUDO/Log",
                        marker_color="#2563eb"))
                    fig_pvp.add_trace(go.Bar(x=meses_p, y=prods, name=f"Produto",
                        marker_color=SEG["chart"]))
                    fig_pvp.add_trace(go.Scatter(x=meses_p, y=lucros2, name="Lucro Líquido",
                        line=dict(color="#f59e0b",width=3), mode="lines+markers"))
                    fig_pvp.add_hline(y=0, line_dash="dot", line_color="#999")
                    fig_pvp.update_layout(barmode="stack", height=300,
                        plot_bgcolor="white", paper_bgcolor="white",
                        legend=dict(orientation="h", y=-0.25),
                        margin=dict(l=0,r=0,t=10,b=0))
                    fig_pvp.update_yaxes(gridcolor="#f0f0f0")
                    st.plotly_chart(fig_pvp, use_container_width=True)

# ════════════════════════════════════════════════
# TAB 7 — CREDENCIAMENTO PUDO
# ════════════════════════════════════════════════
with t_cred:
    st.markdown("## 🏢 Credenciamento como Ponto PUDO")
    st.caption("Informações oficiais das plataformas · Atualizado Jun/2025")

    # ── Comparativo rápido no topo
    st.markdown("### Comparativo Rápido — 3 Plataformas Principais")

    PLAT = {
        "Mercado Livre": {
            "emoji": "🟡", "cor": "#fff7e6", "borda": "#f59e0b",
            "titulo_cor": "#b45309",
            "area_min": "4 m²",
            "comissao": "Variável / mensal*",
            "prazo_resp": "Variável (por demanda)",
            "funcionarios": "Mín. 2 pessoas",
            "horario": "Seg–Sex, horário comercial",
            "cnpj": "Obrigatório",
            "link": "https://envios.mercadolivre.com.br/agencias-mercado-livre/registro",
            "link_label": "Cadastrar como Agência ML",
        },
        "Shopee": {
            "emoji": "🟠", "cor": "#fff4ed", "borda": "#ea580c",
            "titulo_cor": "#c2410c",
            "area_min": "4 m²",
            "comissao": "R$ 0,60 – R$ 1,50 / pacote",
            "prazo_resp": "Até 10 dias úteis",
            "funcionarios": "Mín. 2 pessoas",
            "horario": "Seg–Sab, horário comercial",
            "cnpj": "Obrigatório + CNAE compatível",
            "link": "https://help.shopee.com.br/portal/4/article/175942",
            "link_label": "Cadastrar como Agência Shopee",
        },
        "Amazon Hub": {
            "emoji": "🔵", "cor": "#eff6ff", "borda": "#2563eb",
            "titulo_cor": "#1d4ed8",
            "area_min": "Não divulgado*",
            "comissao": "R$ 1,95 – R$ 2,23 / pacote",
            "prazo_resp": "15 a 40 dias",
            "funcionarios": "Equipe existente",
            "horario": "Até 7 dias/sem · entrega até 20h",
            "cnpj": "Obrigatório + seguro operacional",
            "link": "https://hub.amazon.com.br/counter",
            "link_label": "Cadastrar como Amazon Hub Counter",
        },
    }

    cols_cmp = st.columns(3)
    for ci, (nome, p) in enumerate(PLAT.items()):
        with cols_cmp[ci]:
            st.markdown(f"""
<div style="background:{p['cor']};border:2px solid {p['borda']};
     border-radius:14px;padding:20px;height:100%">
  <div style="font-size:22px;margin-bottom:6px">{p['emoji']} <span style="font-size:17px;font-weight:700;color:{p['titulo_cor']}">{nome}</span></div>
  <table style="width:100%;font-size:13px;color:#444">
    <tr><td>📐 Área mín.</td><td style="font-weight:600;text-align:right">{p['area_min']}</td></tr>
    <tr><td>💰 Comissão</td><td style="font-weight:600;text-align:right">{p['comissao']}</td></tr>
    <tr><td>⏱ Resp. cadastro</td><td style="text-align:right">{p['prazo_resp']}</td></tr>
    <tr><td>👥 Equipe</td><td style="text-align:right">{p['funcionarios']}</td></tr>
    <tr><td>🕐 Horário</td><td style="text-align:right">{p['horario']}</td></tr>
    <tr><td>📋 CNPJ</td><td style="text-align:right">{p['cnpj']}</td></tr>
  </table>
  <div style="margin-top:14px;text-align:center">
    <a href="{p['link']}" target="_blank"
       style="background:{p['borda']};color:white;padding:8px 14px;
              border-radius:8px;text-decoration:none;font-size:12px;font-weight:600">
      Cadastrar agora →
    </a>
  </div>
</div>""", unsafe_allow_html=True)

    st.divider()

    # ── Gráfico de comissão por volume
    st.markdown("### 💰 Potencial de Receita PUDO — Estimativa por Volume")

    vols = [100, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500]
    fig_com = go.Figure()
    fig_com.add_trace(go.Scatter(x=vols, y=[v*1.0  for v in vols],
        name="ML (estimativa R$1/pct)", line=dict(color="#f59e0b", width=2.5),
        fill="tozeroy", fillcolor="rgba(245,158,11,0.08)"))
    fig_com.add_trace(go.Scatter(x=vols, y=[v*1.05 for v in vols],
        name="Shopee (R$1,05 médio)", line=dict(color="#ea580c", width=2.5),
        fill="tozeroy", fillcolor="rgba(234,88,12,0.08)"))
    fig_com.add_trace(go.Scatter(x=vols, y=[v*2.09 for v in vols],
        name="Amazon (R$2,09 médio)", line=dict(color="#2563eb", width=2.5),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.08)"))
    fig_com.update_layout(
        height=280, plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="Pacotes / mês", yaxis_title="Receita estimada (R$)",
        legend=dict(orientation="h", y=-0.30),
        margin=dict(l=0,r=0,t=10,b=0))
    fig_com.update_yaxes(gridcolor="#f0f0f0", tickprefix="R$ ")
    fig_com.update_xaxes(gridcolor="#f0f0f0")
    st.plotly_chart(fig_com, use_container_width=True)
    st.caption("* Comissão ML não divulgada oficialmente — estimativa baseada em relatos de parceiros. Amazon: conversão ~R$2,09 (€0,38 × R$5,50).")

    st.divider()

    # ── Detalhamento por plataforma
    with st.expander("🟡 MERCADO LIVRE — Agência Mercado Envios (Detalhes Completos)", expanded=True):
        d1, d2 = st.columns(2)
        with d1:
            st.markdown("#### Requisitos Mínimos")
            st.markdown("""
| Requisito | Detalhe |
|---|---|
| **Área mínima** | 4 m² exclusivos para pacotes |
| **Localização** | Térreo, acesso público, acessível |
| **CNPJ** | Ativo (qualquer segmento) |
| **Conta Mercado Pago** | Obrigatória para receber pagamentos |
| **Emissão de NF-e** | Necessário |
| **Equipe mínima** | 2 pessoas disponíveis |
| **Acesso à internet** | Smartphone ou computador |
| **Reformas** | Nenhuma adaptação obrigatória |
| **Equipamento especial** | Não é necessário comprar |
| **Horário mínimo** | Seg–Sex, horário comercial |
""")
            st.markdown("#### Equipamentos Recomendados")
            st.markdown("""
- ✅ Smartphone com acesso ao app Mercado Livre
- ✅ Leitor de QR Code (câmera do celular é suficiente)
- ✅ Espaço físico seguro para guardar pacotes
- ✅ Impressora (não obrigatória — ML gera etiquetas)
- ✅ Câmera de segurança (recomendada)
""")
        with d2:
            st.markdown("#### Como Funciona")
            st.markdown("""
**Fluxo operacional:**
1. Transportadora deposita o pacote na sua loja
2. Você escaneia o código no app ML
3. Sistema notifica o comprador automaticamente
4. Comprador apresenta QR Code para retirada
5. Você confirma a entrega no app
6. Comissão registrada — pagamento mensal

**Fluxo de devolução (logística reversa):**
1. Comprador chega com o produto e código de devolução
2. Você embala e gera etiqueta no sistema
3. Transportadora coleta no dia seguinte
4. Comissão registrada

**Vantagens:**
- Sem investimento inicial para ML
- Visibilidade no app como ponto de retirada
- Marca Mercado Livre na fachada (faixa/adesivo fornecido)
- Renda passiva sem precisar alterar o negócio principal
""")
            st.markdown("#### Cadastro e Documentos")
            st.markdown("""
| Documento | Detalhe |
|---|---|
| CNPJ | Cartão CNPJ atualizado |
| Razão Social | Nome da empresa |
| Endereço completo | Com CEP |
| Conta Mercado Pago | Vinculada ao CNPJ |
| Dados bancários | Para recebimento |
""")
            st.markdown("**🔗 [Fazer cadastro como Agência ML](https://envios.mercadolivre.com.br/agencias-mercado-livre/registro)**")
            st.markdown("**🔗 [Central de Ajuda ML — Ponto de Coleta](https://www.mercadolivre.com.br/ajuda/inscricao-agencia-pontos-coleta_39565)**")

    with st.expander("🟠 SHOPEE — Agência Shopee Drops (Detalhes Completos)"):
        d1, d2 = st.columns(2)
        with d1:
            st.markdown("#### Requisitos Mínimos")
            st.markdown("""
| Requisito | Detalhe |
|---|---|
| **Área mínima** | 4 m² para armazenagem de pacotes |
| **Endereço** | Comercial fixo (não residencial) |
| **CNPJ** | Ativo com CNAE compatível (comércio/logística) |
| **Certificado Digital** | Obrigatório |
| **Equipe mínima** | 2 funcionários para atendimento |
| **Horário mínimo** | Seg–Sab, horário comercial |
| **Treinamento** | Obrigatório (online, feito após aprovação) |
| **Câmeras de segurança** | Obrigatório |
| **App SHPX SVP** | Para escanear pacotes (obrigatório) |
""")
            st.markdown("#### Equipamentos Obrigatórios")
            st.markdown("""
- 🔴 **Leitor de código de barras** (scanner)
- 🔴 **Impressora térmica** de etiquetas
- 🔴 **Câmera de segurança** (mínimo 1, focada no balcão)
- 🔴 **Smartphone com internet** + app SHPX SVP instalado
- ✅ Computador (recomendado, não obrigatório)
- ✅ Armário/rack para organizar pacotes por código
""")
            st.markdown("""
> ⚠️ **Atenção:** escanear pacote sem tê-lo fisicamente em mãos resulta em **descredenciamento imediato**.
""")
        with d2:
            st.markdown("#### Modelo de Comissão")
            st.markdown("""
| Volume mensal | Comissão estimada / pacote |
|---|---|
| Até 200 pacotes | R$ 1,20 – R$ 1,50 |
| 200–500 pacotes | R$ 0,90 – R$ 1,20 |
| 500–1.000 pacotes | R$ 0,70 – R$ 0,90 |
| Acima de 1.000 | R$ 0,60 – R$ 0,70 |

*Shopee paga tanto pela **entrada** (recebimento) quanto pela **saída** (retirada pelo cliente).*
""")
            st.markdown("#### Processo de Cadastro")
            st.markdown("""
1. Acessar página oficial de cadastro Shopee
2. Preencher formulário com dados da empresa e localização
3. Shopee avalia em até **10 dias úteis**
4. Se aprovado: e-mail de confirmação + agendamento de treinamento
5. Treinamento online obrigatório (duração ~2h)
6. Liberação para receber pacotes

**Prazo total estimado: 2 a 4 semanas**
""")
            st.markdown("**🔗 [Como se tornar uma Agência Shopee](https://help.shopee.com.br/portal/4/article/175942)**")
            st.markdown("**🔗 [FAQ Completo Agências Shopee](https://help.shopee.com.br/portal/4/article/147066)**")
            st.markdown("**🔗 [Termos e Condições SHPX](https://help.shopee.com.br/portal/4/article/148797)**")

    with st.expander("🔵 AMAZON HUB COUNTER — Detalhes Completos"):
        d1, d2 = st.columns(2)
        with d1:
            st.markdown("#### Requisitos Mínimos")
            st.markdown("""
| Requisito | Detalhe |
|---|---|
| **Área mínima** | Não divulgada — "espaço seguro disponível" |
| **Localização** | Área comercial, shopping ou zona de alto tráfego |
| **CNPJ** | Ativo com documentação completa |
| **Contrato Social** | Atualizado |
| **Comprovante de endereço** | Conta de luz, água ou internet |
| **Seguro operacional** | Obrigatório (certificado de seguro) |
| **Equipe** | Equipe existente da loja (sem contratação extra) |
| **Horário** | Até 7 dias/semana · entregas finalizadas até 20h |
| **Capacidade diária** | 20 a 40 pacotes/dia |
| **Armazenagem** | Pacotes ficam até **14 dias** em espera |
""")
            st.markdown("#### Equipamentos Mínimos")
            st.markdown("""
- 🔴 **Computador ou tablet** com internet para gerir inventário
- 🔴 **Impressora de etiquetas** (térmica recomendada)
- 🔴 **Espaço seguro e organizado** para armazenar pacotes
- ✅ Câmera de segurança (recomendada)
- ✅ Leitor de código de barras (facilita operação)
""")
        with d2:
            st.markdown("#### Modelo de Comissão")
            st.markdown("""
| Métrica | Valor |
|---|---|
| **Comissão por pacote entregue** | ~R$ 1,95 – R$ 2,23 |
| **Base oficial** | €0,35 – €0,40 por pacote |
| **Volume esperado** | 20–40 pacotes / dia |
| **Receita estimada (30 pct/dia)** | R$ 1.755 – R$ 2.007 / mês |
| **Prazo de pagamento** | Mensal |
| **Armazenagem** | Até 14 dias sem custo adicional |

> 💡 Amazon Hub foi lançado em 2024 no Brasil. O programa pode gerar mais de **R$ 300 milhões/ano** em pagamentos às PMEs participantes.
""")
            st.markdown("#### Processo de Cadastro")
            st.markdown("""
1. Acessar **hub.amazon.com.br/counter**
2. Preencher formulário com dados da empresa
3. Enviar documentação: CNPJ, contrato social, comprovante de endereço, seguro
4. Amazon avalia em **15 a 40 dias**
5. Aprovação + onboarding (treinamento operacional)
6. Início das operações

**Prazo total estimado: 1 a 2 meses**
""")
            st.markdown("**🔗 [Cadastro Amazon Hub Counter](https://hub.amazon.com.br/counter)**")
            st.markdown("**🔗 [Portal Amazon Hub Brasil](https://hub.amazon.com.br)**")
            st.markdown("**🔗 [Amazon Hub Delivery (entregador)](https://logistics.amazon.com.br/hubdelivery)**")

    st.divider()

    # ── Checklist de equipamentos consolidado
    st.markdown("### 🛒 Checklist de Equipamentos — O Que Você Precisa Para as 3 Plataformas")

    eq_data = [
        ("Smartphone com internet",                "✅ ML", "✅ Shopee", "✅ Amazon", "Obrigatório",  "R$ 0 (já possui)"),
        ("App Mercado Livre",                      "✅ ML", "—",         "—",         "Gratuito",     "R$ 0"),
        ("App SHPX SVP (Shopee)",                  "—",     "✅ Shopee", "—",         "Obrigatório",  "R$ 0 (gratuito)"),
        ("Leitor código de barras / scanner",      "⬜ Rec","✅ Obrig",  "⬜ Rec",    "Recomendado",  "R$ 150–400"),
        ("Impressora térmica de etiquetas",        "⬜ Rec","✅ Obrig",  "✅ Obrig",   "Obrigatório",  "R$ 400–900"),
        ("Computador ou tablet",                   "⬜ Rec","⬜ Rec",   "✅ Obrig",   "Recomendado",  "R$ 800–2.500"),
        ("Câmera de segurança (mín. 1)",           "⬜ Rec","✅ Obrig",  "⬜ Rec",    "Obrigatório",  "R$ 200–600 / câmera"),
        ("Espaço físico organizado (4 m²+)",       "✅ ML", "✅ Shopee", "✅ Amazon",  "Obrigatório",  "—"),
        ("CNPJ ativo",                             "✅ ML", "✅ Shopee", "✅ Amazon",  "Obrigatório",  "R$ 0–1.500 abertura"),
        ("Conta Mercado Pago",                     "✅ ML", "—",         "—",         "Obrigatório",  "R$ 0 (gratuito)"),
        ("Certificado Digital e-CNPJ",             "—",     "✅ Shopee", "—",         "Obrigatório",  "R$ 200–350 / ano"),
        ("Seguro operacional",                     "—",     "—",         "✅ Amazon",  "Obrigatório",  "R$ 150–400 / mês"),
        ("Balança (até 30 kg)",                    "⬜ Rec","⬜ Rec",   "—",         "Recomendado",  "R$ 200–500"),
        ("Rack/armário organizador de pacotes",    "⬜ Rec","⬜ Rec",   "⬜ Rec",    "Recomendado",  "R$ 300–900"),
    ]

    df_eq = pd.DataFrame(eq_data, columns=[
        "Equipamento", "Mercado Livre", "Shopee", "Amazon Hub", "Status", "Custo Estimado"])

    def cor_eq(val):
        if "✅" in str(val): return "color:#16a34a;font-weight:600"
        if "⬜" in str(val): return "color:#ca8a04"
        if "—"  in str(val): return "color:#94a3b8"
        return ""

    st.dataframe(
        df_eq.style.map(cor_eq, subset=["Mercado Livre","Shopee","Amazon Hub"]),
        use_container_width=True, hide_index=True)

    # ── Custo total de setup
    st.divider()
    st.markdown("### 💸 Custo Total de Setup para 3 Plataformas Simultaneamente")
    setup_items = {
        "Impressora térmica": 650,
        "Scanner de código de barras": 280,
        "Câmera de segurança (2 un)": 700,
        "Rack organizador de pacotes": 600,
        "Certificado Digital e-CNPJ": 280,
        "Balança até 30kg": 350,
        "Tablet para Amazon Hub": 1200,
        "Seguro operacional (1 mês)": 250,
        "Abertura de empresa (se necessário)": 1200,
    }
    total_setup = sum(setup_items.values())
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("**Itens e valores estimados:**")
        for item, val in setup_items.items():
            st.markdown(f"- {item}: **R$ {val:,.0f}**".replace(",","."))
        st.markdown(f"**💰 Total estimado: R$ {total_setup:,.0f}**".replace(",","."))
        st.caption("Valores de mercado — podem variar. Itens que já possui reduzem o total.")

    with s2:
        fig_setup = px.bar(
            x=list(setup_items.values()), y=list(setup_items.keys()),
            orientation="h",
            color=list(setup_items.values()),
            color_continuous_scale=["#dbeafe","#1d4ed8"],
            text=[f"R$ {v:,.0f}".replace(",",".") for v in setup_items.values()],
        )
        fig_setup.update_traces(textposition="outside")
        fig_setup.update_layout(
            height=320, showlegend=False, coloraxis_showscale=False,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=0,r=90,t=10,b=0))
        fig_setup.update_xaxes(visible=False)
        st.plotly_chart(fig_setup, use_container_width=True)

    st.divider()

    # ── Outras plataformas
    st.markdown("### 📦 Outras Plataformas PUDO — Referências")
    outras = [
        ("Correios Agente",  "R$ 2,50–4,00/pct", "CNPJ + alvará",           "https://www.correios.com.br/solucoes-empresariais/agentes-correios"),
        ("Jadlog Pickup",    "R$ 3,00–5,00/pct", "CNPJ + espaço físico",    "https://www.jadlog.com.br/jadlog/pickup"),
        ("Pegaki",           "R$ 3,00–4,50/pct", "CNPJ + cadastro online",  "https://www.pegaki.com.br/seja-um-ponto"),
        ("Total Express",    "R$ 3,00–4,00/pct", "CNPJ + parceria",         "https://www.totalexpress.com.br/seja-parceiro"),
        ("Loggi",            "Variável",          "CNPJ + app Loggi",        "https://www.loggi.com"),
        ("Sequoia Pickup",   "Variável",          "CNPJ + parceria",         "https://www.sequoialog.com.br"),
    ]
    cols_out = st.columns(3)
    for oi, (nome, comissao, req, link) in enumerate(outras):
        with cols_out[oi % 3]:
            st.markdown(f"""
<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;
     padding:14px;margin-bottom:10px;box-shadow:0 1px 3px rgba(0,0,0,.05)">
  <div style="font-weight:700;font-size:14px;color:#1e293b">{nome}</div>
  <div style="font-size:12px;color:#16a34a;margin:4px 0">💰 {comissao}</div>
  <div style="font-size:11px;color:#64748b">📋 {req}</div>
  <a href="{link}" target="_blank"
     style="font-size:11px;color:#2563eb;text-decoration:none">🔗 Cadastrar →</a>
</div>""", unsafe_allow_html=True)

st.divider()
# ════════════════════════════════════════════════════════════════
# TAB 8 — GESTÃO OPERACIONAL
# ════════════════════════════════════════════════════════════════
with t_adm:
    import uuid as _uuid
    from datetime import date as _date, datetime as _dt

    # ── Constantes
    CATEGORIAS = {
        # label: (natureza, cor, icone)
        "Entrada PUDO — Pacote Recebido":    ("entrada", "#2563eb", "📥"),
        "Saída PUDO — Pacote Entregue":      ("entrada", "#0d9488", "📤"),
        "Logística Reversa — Recebida":      ("entrada", "#7c3aed", "↩️"),
        "Logística Reversa — Despachada":    ("entrada", "#7c3aed", "↪️"),
        "Venda Produto — Loja Física":       ("entrada", "#16a34a", "🏪"),
        "Venda Produto — Mercado Livre":     ("entrada", "#f59e0b", "🟡"),
        "Venda Produto — Shopee":            ("entrada", "#ea580c", "🟠"),
        "Venda Produto — Amazon":            ("entrada", "#1d4ed8", "🔵"),
        "Venda Produto — Outro Canal":       ("entrada", "#16a34a", "🛒"),
        "Troca / Devolução — Recebida":      ("saida",   "#dc2626", "🔄"),
        "Compra de Estoque":                 ("saida",   "#dc2626", "📦"),
        "Despesa — Aluguel":                 ("saida",   "#dc2626", "🏠"),
        "Despesa — Pessoal":                 ("saida",   "#dc2626", "👥"),
        "Despesa — Marketing":               ("saida",   "#dc2626", "📣"),
        "Despesa — Operacional":             ("saida",   "#dc2626", "⚙️"),
        "Despesa — Imposto":                 ("saida",   "#dc2626", "📋"),
        "Outra Entrada":                     ("entrada", "#16a34a", "➕"),
        "Outra Saída":                       ("saida",   "#dc2626", "➖"),
    }
    PLATAFORMAS = ["Mercado Livre","Shopee","Amazon","Loja Física","Correios","Jadlog","Outro"]
    STATUS_OPTS = ["✅ Concluído","⏳ Pendente","❌ Cancelado"]

    # ── Session state
    if "lancamentos" not in st.session_state:
        st.session_state.lancamentos = []
    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    def novo_id():
        return str(_uuid.uuid4())[:8].upper()

    def nat_categoria(cat):
        return CATEGORIAS.get(cat, ("entrada","#16a34a","•"))[0]

    def cor_categoria(cat):
        return CATEGORIAS.get(cat, ("entrada","#16a34a","•"))[1]

    def ico_categoria(cat):
        return CATEGORIAS.get(cat, ("entrada","#16a34a","•"))[2]

    # ── Layout
    form_col, main_col = st.columns([1, 2.8])

    # ════ FORMULÁRIO ════
    with form_col:
        st.markdown("#### ➕ Novo Lançamento")

        edit_obj = None
        if st.session_state.edit_id:
            edit_obj = next((l for l in st.session_state.lancamentos
                             if l["id"] == st.session_state.edit_id), None)

        with st.form("form_lanc", clear_on_submit=True):
            data_l  = st.date_input("Data", value=_date.today(), key="fl_data")
            cat     = st.selectbox("Categoria", list(CATEGORIAS.keys()),
                                   index=0, key="fl_cat")
            plat    = st.selectbox("Plataforma / Canal", PLATAFORMAS, key="fl_plat")
            desc    = st.text_input("Descrição / Produto",
                                    placeholder="Ex: Isca artificial Rapala 7cm", key="fl_desc")
            c1, c2  = st.columns(2)
            qtd     = c1.number_input("Qtd", 1, 99999, 1, key="fl_qtd")
            vunit   = c2.number_input("Valor Unit (R$)", 0.0, 999999., 0.0, 0.5, key="fl_vunit")
            vtotal  = qtd * vunit
            st.markdown(f"**Total: R$ {vtotal:,.2f}**".replace(",","."))
            status  = st.selectbox("Status", STATUS_OPTS, key="fl_status")
            obs_l   = st.text_area("Observações", height=55, key="fl_obs")

            salvar = st.form_submit_button(
                "💾 Salvar Lançamento" if not edit_obj else "✏️ Atualizar",
                use_container_width=True, type="primary")

            if salvar and desc:
                nat = nat_categoria(cat)
                reg = {
                    "id":       novo_id(),
                    "data":     str(data_l),
                    "cat":      cat,
                    "plat":     plat,
                    "desc":     desc,
                    "qtd":      qtd,
                    "vunit":    vunit,
                    "vtotal":   vtotal if nat == "entrada" else -vtotal,
                    "natureza": nat,
                    "status":   status,
                    "obs":      obs_l,
                }
                if edit_obj:
                    idx = next(i for i,l in enumerate(st.session_state.lancamentos)
                               if l["id"] == st.session_state.edit_id)
                    reg["id"] = st.session_state.edit_id
                    st.session_state.lancamentos[idx] = reg
                    st.session_state.edit_id = None
                else:
                    st.session_state.lancamentos.append(reg)
                st.rerun()

        st.divider()

        # ── Filtros
        st.markdown("#### 🔍 Filtros")
        filt_nat  = st.multiselect("Natureza", ["entrada","saida"],
                                   default=["entrada","saida"], key="filt_nat")
        filt_plat = st.multiselect("Plataforma", PLATAFORMAS, default=[], key="filt_plat")
        filt_stat = st.multiselect("Status", STATUS_OPTS, default=[], key="filt_stat")
        filt_txt  = st.text_input("Buscar descrição", key="filt_txt")
        data_ini  = st.date_input("De", value=_date(2025,1,1), key="filt_ini")
        data_fim  = st.date_input("Até", value=_date.today(), key="filt_fim")

        st.divider()

        # ── Export / Import
        st.markdown("#### 💾 Dados")
        if st.session_state.lancamentos:
            j = json.dumps(st.session_state.lancamentos, ensure_ascii=False, indent=2)
            st.download_button("⬇ Exportar JSON", j,
                file_name="gestao_operacional_pudo.json",
                mime="application/json", use_container_width=True)

            # CSV
            df_exp = pd.DataFrame(st.session_state.lancamentos)
            csv_str = df_exp.to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig")
            st.download_button("⬇ Exportar CSV (Excel)", csv_str,
                file_name="gestao_operacional_pudo.csv",
                mime="text/csv", use_container_width=True)

        upf = st.file_uploader("⬆ Importar JSON", type="json", key="up_adm")
        if upf:
            try:
                loaded = json.load(upf)
                st.session_state.lancamentos += loaded
                st.success(f"{len(loaded)} lançamentos importados!")
                st.rerun()
            except Exception:
                st.error("Arquivo inválido.")

        if st.session_state.lancamentos:
            if st.button("🗑 Limpar todos os lançamentos",
                         use_container_width=True, key="clear_lanc"):
                st.session_state.lancamentos = []
                st.rerun()

    # ════ PAINEL PRINCIPAL ════
    with main_col:
        # Aplica filtros
        lancs = st.session_state.lancamentos
        if filt_nat:
            lancs = [l for l in lancs if l["natureza"] in filt_nat]
        if filt_plat:
            lancs = [l for l in lancs if l["plat"] in filt_plat]
        if filt_stat:
            lancs = [l for l in lancs if l["status"] in filt_stat]
        if filt_txt:
            lancs = [l for l in lancs if filt_txt.lower() in l["desc"].lower()]
        lancs = [l for l in lancs
                 if str(data_ini) <= l["data"] <= str(data_fim)]
        lancs_ord = sorted(lancs, key=lambda x: x["data"], reverse=True)

        if not st.session_state.lancamentos:
            st.info("👈 Adicione o primeiro lançamento pelo formulário ao lado.")
        else:
            # ── KPIs
            total_ent = sum(l["vtotal"] for l in lancs if l["natureza"]=="entrada")
            total_sai = sum(abs(l["vtotal"]) for l in lancs if l["natureza"]=="saida")
            saldo     = total_ent - total_sai
            n_pudo    = sum(1 for l in lancs if "PUDO" in l["cat"])
            n_prod    = sum(1 for l in lancs if "Venda" in l["cat"])
            n_pen     = sum(1 for l in lancs if "Pendente" in l["status"])

            ka,kb,kc,kd,ke,kf = st.columns(6)
            def km(col, lbl, val, fmt_fn, cls=""):
                col.markdown(f"""<div class="hero-card {cls}">
                  <div class="hero-lbl">{lbl}</div>
                  <div class="hero-val" style="font-size:18px">{fmt_fn(val)}</div>
                </div>""", unsafe_allow_html=True)
            km(ka,"Total Entradas",  total_ent, lambda v: f"R$ {v:,.0f}".replace(",","."), "green")
            km(kb,"Total Saídas",    total_sai, lambda v: f"R$ {v:,.0f}".replace(",","."), "red")
            km(kc,"Saldo Período",   saldo,     lambda v: f"R$ {v:,.0f}".replace(",","."),
               "green" if saldo>=0 else "red")
            km(kd,"Lançamentos PUDO",n_pudo,   str)
            km(ke,"Vendas Produto",  n_prod,   str, "green")
            km(kf,"Pendentes",       n_pen,    str, "orange" if n_pen>0 else "")

            st.markdown("<div style='margin:10px 0'></div>", unsafe_allow_html=True)

            # ── Gráficos
            g1, g2 = st.columns([2,1])

            with g1:
                # Saldo acumulado por data
                if lancs_ord:
                    df_gc = pd.DataFrame(lancs_ord).sort_values("data")
                    df_gc["acum"] = df_gc["vtotal"].cumsum()
                    fig_gc = go.Figure()
                    fig_gc.add_trace(go.Bar(
                        x=df_gc["data"], y=df_gc["vtotal"],
                        marker_color=["#16a34a" if v>=0 else "#dc2626"
                                      for v in df_gc["vtotal"]],
                        name="Valor lançamento", opacity=.8))
                    fig_gc.add_trace(go.Scatter(
                        x=df_gc["data"], y=df_gc["acum"],
                        name="Saldo acumulado",
                        line=dict(color="#2563eb", width=2.5),
                        mode="lines+markers"))
                    fig_gc.add_hline(y=0, line_dash="dot", line_color="#999")
                    fig_gc.update_layout(
                        height=220, barmode="relative",
                        plot_bgcolor="white", paper_bgcolor="white",
                        legend=dict(orientation="h", y=-0.35),
                        margin=dict(l=0,r=0,t=10,b=0),
                        title=dict(text="Lançamentos e Saldo Acumulado",
                                   font=dict(size=11), x=0))
                    fig_gc.update_yaxes(gridcolor="#f0f0f0")
                    st.plotly_chart(fig_gc, use_container_width=True)

            with g2:
                # Pizza por plataforma (entradas)
                ent_plat = {}
                for l in lancs:
                    if l["natureza"] == "entrada":
                        ent_plat[l["plat"]] = ent_plat.get(l["plat"],0) + l["vtotal"]
                if ent_plat:
                    fig_pp = go.Figure(go.Pie(
                        labels=list(ent_plat.keys()),
                        values=list(ent_plat.values()),
                        hole=.45, textinfo="percent+label",
                        textfont_size=9,
                        marker_colors=["#f59e0b","#ea580c","#2563eb",
                                       "#16a34a","#7c3aed","#0d9488","#64748b"]))
                    fig_pp.update_layout(
                        height=210, showlegend=False,
                        paper_bgcolor="white",
                        margin=dict(l=0,r=0,t=20,b=0),
                        title=dict(text="Entradas por Canal",
                                   font=dict(size=11), x=0.5))
                    st.plotly_chart(fig_pp, use_container_width=True)

            # ── Tabela de lançamentos
            st.markdown(f"**{len(lancs_ord)} lançamento(s) no período**")

            if lancs_ord:
                rows_t = []
                for l in lancs_ord:
                    ico = ico_categoria(l["cat"])
                    rows_t.append({
                        "ID": l["id"],
                        "Data": l["data"],
                        "Tipo": f"{ico} {l['cat'][:35]}",
                        "Canal": l["plat"],
                        "Descrição": l["desc"][:40],
                        "Qtd": l["qtd"],
                        "Unit (R$)": f"{l['vunit']:,.2f}".replace(",","."),
                        "Total (R$)": f"{l['vtotal']:,.2f}".replace(",","."),
                        "Status": l["status"],
                    })
                df_t = pd.DataFrame(rows_t)

                def cor_row(val):
                    try:
                        v = float(val.replace(".","").replace(",","."))
                        if v > 0: return "color:#16a34a;font-weight:600"
                        if v < 0: return "color:#dc2626;font-weight:600"
                    except: pass
                    return ""

                st.dataframe(
                    df_t.style.map(cor_row, subset=["Total (R$)"]),
                    use_container_width=True, hide_index=True,
                    height=320)

                # ── Editar / Excluir lançamento
                st.markdown("**✏️ Editar ou excluir um lançamento**")
                ids_disp = [l["id"] for l in lancs_ord]
                sel_id   = st.selectbox("Selecionar lançamento pelo ID",
                                        ["— selecione —"] + ids_disp, key="sel_edit_id")
                if sel_id != "— selecione —":
                    obj_sel = next(l for l in st.session_state.lancamentos if l["id"]==sel_id)
                    st.markdown(f"""
> **{obj_sel['data']}** · {ico_categoria(obj_sel['cat'])} {obj_sel['cat']}
> {obj_sel['plat']} · {obj_sel['desc']} · Qtd {obj_sel['qtd']} · **R$ {abs(obj_sel['vtotal']):,.2f}** · {obj_sel['status']}
""".replace(",","."))
                    ec1, ec2 = st.columns(2)
                    if ec1.button("✏️ Carregar para edição", use_container_width=True):
                        st.session_state.edit_id = sel_id
                        st.info("Lançamento carregado no formulário ao lado. Edite e salve.")
                    if ec2.button("🗑 Excluir este lançamento",
                                  use_container_width=True, type="secondary"):
                        st.session_state.lancamentos = [
                            l for l in st.session_state.lancamentos if l["id"] != sel_id]
                        st.success("Excluído.")
                        st.rerun()

            # ── Resumo por categoria
            st.divider()
            st.markdown("**📊 Resumo por Categoria**")
            cat_res = {}
            for l in lancs:
                c = l["cat"]
                if c not in cat_res:
                    cat_res[c] = {"qtd_lanc":0,"qtd_itens":0,"total":0.0}
                cat_res[c]["qtd_lanc"]  += 1
                cat_res[c]["qtd_itens"] += l["qtd"]
                cat_res[c]["total"]     += l["vtotal"]
            if cat_res:
                rows_cr = []
                for cat_k, v in sorted(cat_res.items(),
                                       key=lambda x: abs(x[1]["total"]), reverse=True):
                    rows_cr.append({
                        "Categoria": f"{ico_categoria(cat_k)} {cat_k}",
                        "Lançamentos": v["qtd_lanc"],
                        "Itens": v["qtd_itens"],
                        "Total (R$)": f"{v['total']:,.2f}".replace(",","."),
                    })
                df_cr = pd.DataFrame(rows_cr)
                st.dataframe(
                    df_cr.style.map(cor_row, subset=["Total (R$)"]),
                    use_container_width=True, hide_index=True)

            # ── Resumo por plataforma
            st.markdown("**📊 Resumo por Plataforma / Canal**")
            plat_res = {}
            for l in lancs:
                p = l["plat"]
                if p not in plat_res:
                    plat_res[p] = {"entradas":0.,"saidas":0.,"saldo":0.}
                if l["natureza"]=="entrada":
                    plat_res[p]["entradas"] += l["vtotal"]
                else:
                    plat_res[p]["saidas"]   += abs(l["vtotal"])
                plat_res[p]["saldo"] = plat_res[p]["entradas"] - plat_res[p]["saidas"]
            if plat_res:
                rows_pr = [{"Canal": k,
                            "Entradas": f"R$ {v['entradas']:,.2f}".replace(",","."),
                            "Saídas":   f"R$ {v['saidas']:,.2f}".replace(",","."),
                            "Saldo":    f"R$ {v['saldo']:,.2f}".replace(",",".")}
                           for k,v in sorted(plat_res.items(),
                                             key=lambda x: x[1]["entradas"], reverse=True)]
                df_pr = pd.DataFrame(rows_pr)
                st.dataframe(
                    df_pr.style.map(cor_row, subset=["Saldo"]),
                    use_container_width=True, hide_index=True)

st.divider()
st.caption("📦 PUDO Vila Carrão — v7.0 | Dashboard · Financeiro · DRE · Plano · Desenho · Controle Mensal · Credenciamento · Gestão Operacional")
