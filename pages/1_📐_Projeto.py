# ============================================================
# CSS — APARÊNCIA 6C PROFISSIONAL
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       TIPOGRAFIA GLOBAL
       ====================================================== */

    html,
    body,
    [class*="css"],
    .stApp,
    .stMarkdown,
    .stTextInput,
    .stNumberInput,
    .stDateInput,
    .stTextArea,
    .stSelectbox,
    .stButton,
    .stDataFrame {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;
    }

    .stApp {
        background: #f5f7fa;
        color: #17202a;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ======================================================
       TÍTULOS STREAMLIT
       ====================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        color: #17202a !important;
        font-weight: 750 !important;
        letter-spacing: -0.35px !important;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        background:
            linear-gradient(
                135deg,
                #17202a 0%,
                #263746 55%,
                #34495e 100%
            );

        border-radius: 18px;

        padding: 34px 38px;

        margin-bottom: 30px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.12);

        color: white;
    }

    .hero-title {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        font-size: 2.15rem;

        font-weight: 800;

        letter-spacing: -0.7px;

        line-height: 1.2;

        margin-bottom: 10px;

        color: #ffffff;
    }

    .hero-subtitle {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        font-size: 1rem;

        font-weight: 400;

        color: #dce3e8;

        line-height: 1.6;

        margin-bottom: 18px;
    }

    .hero-badge {
        display: inline-block;

        background:
            rgba(255,255,255,0.12);

        border:
            1px solid rgba(255,255,255,0.22);

        border-radius: 999px;

        padding: 7px 14px;

        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        font-size: 0.75rem;

        font-weight: 700;

        letter-spacing: 0.6px;

        color: #ffffff;
    }

    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-header {
        margin-top: 30px;
        margin-bottom: 17px;
    }

    .section-title {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        font-size: 1.30rem;

        font-weight: 750;

        color: #17202a;

        letter-spacing: -0.35px;

        line-height: 1.35;

        margin-bottom: 4px;
    }

    .section-subtitle {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #6b7280;

        font-size: 0.88rem;

        font-weight: 400;

        line-height: 1.5;

        margin-bottom: 18px;
    }

    /* ======================================================
       LABELS DOS CAMPOS
       ====================================================== */

    label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        font-weight: 600 !important;

        color: #374151 !important;

        font-size: 0.86rem !important;
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 9px !important;

        border-color: #d9dee3 !important;

        background: #ffffff !important;

        box-shadow:
            0 1px 2px rgba(0,0,0,0.02) !important;
    }

    input,
    textarea {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        font-size: 0.91rem !important;

        color: #17202a !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #9aa3ad !important;
    }

    /* ======================================================
       CARDS
       ====================================================== */

    .info-card {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 14px;

        padding: 18px 20px;

        margin-bottom: 14px;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
    }

    .card-label {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #7b8794;

        font-size: 0.70rem;

        font-weight: 750;

        text-transform: uppercase;

        letter-spacing: 0.7px;

        margin-bottom: 5px;
    }

    .card-value {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #17202a;

        font-size: 0.98rem;

        font-weight: 600;

        line-height: 1.45;
    }

    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 14px;

        padding: 20px;

        text-align: center;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
    }

    .metric-label {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #7b8794;

        font-size: 0.70rem;

        font-weight: 800;

        letter-spacing: 0.8px;

        margin-bottom: 7px;
    }

    .metric-value {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #17202a;

        font-size: 1.60rem;

        font-weight: 800;

        letter-spacing: -0.5px;
    }

    /* ======================================================
       TOTAL
       ====================================================== */

    .total-card {
        background:
            linear-gradient(
                135deg,
                #ecfdf3,
                #f6fff9
            );

        border:
            2px solid #28a745;

        border-radius: 16px;

        padding: 25px;

        text-align: center;

        margin: 22px 0;

        box-shadow:
            0 5px 18px rgba(40,167,69,0.10);
    }

    .total-label {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #36734a;

        font-size: 0.76rem;

        font-weight: 800;

        letter-spacing: 1px;
    }

    .total-value {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #176b35;

        font-size: 2.2rem;

        font-weight: 900;

        letter-spacing: -0.8px;

        margin-top: 5px;
    }

    /* ======================================================
       ASSINATURA
       ====================================================== */

    .assinatura {
        margin: 55px auto 25px auto;

        max-width: 520px;

        text-align: center;
    }

    .linha-assinatura {
        border-top:
            1px solid #333;

        width: 85%;

        margin:
            0 auto 10px auto;
    }

    .assinatura-nome {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        font-weight: 700;

        color: #17202a;

        font-size: 0.95rem;
    }

    .assinatura-cargo {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        color: #777;

        font-size: 0.80rem;

        margin-top: 5px;
    }

    /* ======================================================
       TABELAS
       ====================================================== */

    .table-card {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 14px;

        padding: 8px;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
    }

    /* ======================================================
       AVISOS
       ====================================================== */

    .notice-card {
        background: #ffffff;

        border-left:
            4px solid #34495e;

        border-radius: 10px;

        padding: 15px 18px;

        margin: 12px 0;

        color: #374151;

        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

        font-size: 0.90rem;

        line-height: 1.55;
    }

    /* ======================================================
       BOTÕES
       ====================================================== */

    .stButton > button {
        border-radius: 9px !important;

        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        font-weight: 700 !important;

        min-height: 42px;

        letter-spacing: 0.1px;
    }

    /* ======================================================
       MÉTRICAS STREAMLIT
       ====================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 12px;

        padding: 12px;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricLabel"] {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        font-weight: 650 !important;
    }

    div[data-testid="stMetricValue"] {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        font-weight: 800 !important;
    }

    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ======================================================
       CAPTION
       ====================================================== */

    .stCaption,
    [data-testid="stCaptionContainer"] {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        color: #7b8794 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
