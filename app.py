import streamlit as st
from datetime import date

from src.prediction import (
    predict_complaint,
    get_input_categories,
    company_frequency_mapping,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Consumer Complaint Predictor",
    page_icon="🤖",
    layout="wide",
)


st.markdown(r'''
<style>
:root{--bg:#07111f;--card:rgba(15,28,47,.78);--border:rgba(148,163,184,.16);--muted:#a9b7ca}
html,body,[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 8% 8%,rgba(124,92,255,.15),transparent 27%),radial-gradient(circle at 92% 18%,rgba(25,195,255,.11),transparent 25%),radial-gradient(circle at 50% 95%,rgba(124,92,255,.08),transparent 30%),var(--bg);color:#f8fafc}
[data-testid="stHeader"]{background:rgba(7,17,31,.72);backdrop-filter:blur(14px)}
.block-container{max-width:1180px;padding:2rem 1.25rem 4rem}
[data-testid="stAppViewContainer"]::before,[data-testid="stAppViewContainer"]::after{content:"";position:fixed;width:330px;height:330px;border-radius:50%;filter:blur(70px);pointer-events:none;z-index:0}
[data-testid="stAppViewContainer"]::before{background:rgba(124,92,255,.07);top:8%;left:-120px;animation:orb1 10s ease-in-out infinite}
[data-testid="stAppViewContainer"]::after{background:rgba(25,195,255,.06);right:-120px;bottom:4%;animation:orb2 12s ease-in-out infinite}
@keyframes orb1{50%{transform:translate(50px,35px)}}@keyframes orb2{50%{transform:translate(-45px,-30px)}}
.hero{position:relative;overflow:hidden;padding:2.25rem 2.1rem;margin-bottom:1.7rem;border:1px solid var(--border);border-radius:28px;background:linear-gradient(135deg,rgba(124,92,255,.20),rgba(25,195,255,.07)),rgba(12,24,41,.84);box-shadow:0 24px 80px rgba(0,0,0,.24);backdrop-filter:blur(18px);animation:heroIn .8s ease both}
.hero::after{content:"";position:absolute;width:220px;height:220px;right:-75px;top:-100px;border-radius:50%;border:1px solid rgba(255,255,255,.08);box-shadow:0 0 0 30px rgba(255,255,255,.018),0 0 0 60px rgba(255,255,255,.012);animation:pulseRing 4s ease-in-out infinite}
@keyframes heroIn{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}@keyframes pulseRing{50%{transform:scale(1.08);opacity:1}}
.hero-badge{display:inline-flex;padding:7px 12px;border-radius:999px;background:rgba(124,92,255,.14);border:1px solid rgba(124,92,255,.28);color:#cfc6ff;font-size:.78rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase}
.hero-title{margin:14px 0 0;font-size:clamp(2rem,5vw,3.55rem);line-height:1.03;font-weight:850;letter-spacing:-.045em;background:linear-gradient(90deg,#fff,#dcd5ff,#b7efff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-subtitle{max-width:760px;margin-top:14px;color:var(--muted);line-height:1.7}
.section-heading{display:flex;align-items:center;gap:12px;margin:1.9rem 0 1rem;animation:fadeUp .65s ease both}
.section-icon{width:42px;height:42px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,rgba(124,92,255,.22),rgba(25,195,255,.14));border:1px solid var(--border)}
.section-title{margin:0;font-size:1.35rem;font-weight:800;color:#f8fafc}.section-description{margin:2px 0 0;color:var(--muted);font-size:.88rem}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.glass-card{padding:1.2rem 1.25rem;border:1px solid var(--border);border-radius:22px;background:var(--card);box-shadow:0 18px 55px rgba(0,0,0,.16);backdrop-filter:blur(14px);transition:.28s ease;animation:cardIn .65s ease both}
.glass-card:hover{transform:translateY(-4px);border-color:rgba(124,92,255,.34);box-shadow:0 24px 65px rgba(0,0,0,.23)}
@keyframes cardIn{from{opacity:0;transform:translateY(15px)}to{opacity:1;transform:none}}
label,[data-testid="stWidgetLabel"] p{color:#d9e2f0!important;font-weight:650!important}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,textarea,input{background:rgba(7,17,31,.72)!important;border-color:rgba(148,163,184,.18)!important;color:#f8fafc!important;border-radius:13px!important}
textarea{min-height:160px!important}
.stButton>button{min-height:54px;border:0;border-radius:16px;color:white!important;font-weight:800;font-size:1rem;background:linear-gradient(110deg,#6f4df6,#8b5cf6,#13b9ef,#6f4df6);background-size:250% 100%;box-shadow:0 12px 32px rgba(91,67,220,.28);transition:.22s ease;animation:gradientMove 5s linear infinite}
.stButton>button:hover{transform:translateY(-3px) scale(1.01);box-shadow:0 18px 42px rgba(91,67,220,.38)}
@keyframes gradientMove{to{background-position:250% 50%}}
.result-banner{margin:1.4rem 0;padding:1.4rem 1.5rem;border-radius:20px;border:1px solid rgba(34,197,94,.24);background:linear-gradient(135deg,rgba(34,197,94,.13),rgba(25,195,255,.06));animation:resultIn .7s ease both}
.result-label{color:#86efac;font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;font-weight:800}.result-value{margin-top:5px;font-size:clamp(1.35rem,3vw,2rem);font-weight:850}
@keyframes resultIn{from{opacity:0;transform:scale(.97) translateY(10px)}to{opacity:1;transform:none}}
[data-testid="stMetric"]{padding:1.1rem 1.15rem;min-height:118px;border:1px solid var(--border);border-radius:19px;background:var(--card);box-shadow:0 15px 45px rgba(0,0,0,.14);transition:.25s ease}
[data-testid="stMetric"]:hover{transform:translateY(-4px);border-color:rgba(25,195,255,.3)}
[data-testid="stMetricLabel"]{color:#9fb0c7!important}[data-testid="stMetricValue"]{color:#fff!important;font-weight:850!important}
[data-testid="stProgressBar"]>div{background:rgba(255,255,255,.07);border-radius:99px}
[data-testid="stProgressBar"]>div>div{border-radius:99px;background:linear-gradient(90deg,#6f4df6,#17c7f2);background-size:200% 100%;animation:progressGlow 2.2s linear infinite}
@keyframes progressGlow{to{background-position:200% 50%}}
.model-note{padding:1.15rem 1.25rem;border:1px solid rgba(25,195,255,.16);border-radius:18px;background:rgba(25,195,255,.055);color:#c4d3e5;line-height:1.7}
hr{border-color:rgba(148,163,184,.11)!important}
@media(max-width:768px){.block-container{padding:1rem .8rem 3rem}.hero{padding:1.5rem 1.25rem;border-radius:22px}.hero-title{font-size:2rem}.hero-subtitle{font-size:.9rem}.glass-card{padding:1rem;border-radius:18px}[data-testid="stMetric"]{min-height:96px}}
</style>
''', unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================


st.markdown(r'''
<div class="hero">
  <div class="hero-badge">✦ AI / ML • Consumer Analytics</div>
  <h1 class="hero-title">Consumer Complaint<br>Response Predictor</h1>
  <p class="hero-subtitle">Analyze complaint details and estimate the most likely company response using your trained machine-learning model.</p>
</div>
''', unsafe_allow_html=True)

st.divider()


# =========================================================
# LOAD CATEGORIES
# =========================================================

categories = get_input_categories()

companies = company_frequency_mapping["company"].tolist()


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown("""<div class="section-heading"><div class="section-icon">📋</div><div><h2 class="section-title">Complaint Information</h2><p class="section-description">Provide the complaint metadata used by the model.</p></div></div>""", unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    product = st.selectbox(
        "Product",
        categories["product"],
    )

    sub_product = st.selectbox(
        "Sub-product",
        categories["sub_product"],
    )

    issue = st.selectbox(
        "Issue",
        categories["issue"],
    )

    sub_issue = st.selectbox(
        "Sub-issue",
        categories["sub_issue"],
    )


with col2:

    submitted_via = st.selectbox(
        "Submitted Via",
        categories["submitted_via"],
    )

    state = st.selectbox(
        "State",
        categories["state"],
    )

    company = st.selectbox(
        "Company",
        companies,
    )

    received_date = st.date_input("Date Received", value=date.today())

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# NARRATIVE
# =========================================================

st.divider()

st.markdown("""<div class="section-heading"><div class="section-icon">📝</div><div><h2 class="section-title">Complaint Narrative</h2><p class="section-description">Add the customer's complaint for additional engineered features.</p></div></div>""", unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

narrative = st.text_area(
    "Describe the complaint",
    placeholder=(
        "Example: I was charged an incorrect fee on my "
        "credit card and the amount has not been refunded."
    ),
    height=150,
)

st.caption(
    "The current model uses engineered narrative features such as "
    "whether a narrative is present, its length, and its word count."
)
st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# PREDICTION BUTTON
# =========================================================

st.divider()

predict = st.button(
    "🚀 Predict Company Response",
    type="primary",
    use_container_width=True,
)


# =========================================================
# PREDICTION
# =========================================================

if predict:

    with st.spinner(
        "Analyzing complaint and generating prediction..."
    ):

        prediction, probabilities = predict_complaint(
            product=product,
            sub_product=sub_product,
            issue=issue,
            sub_issue=sub_issue,
            submitted_via=submitted_via,
            state=state,
            company=company,
            received_date=received_date,
            narrative=narrative,
        )


    # =====================================================
    # RESULT
    # =====================================================

    st.divider()

    st.markdown("""<div class="section-heading"><div class="section-icon">🎯</div><div><h2 class="section-title">Prediction Result</h2><p class="section-description">Model output and probability breakdown.</p></div></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="result-banner"><div class="result-label">Predicted Company Response</div><div class="result-value">{prediction}</div></div>""", unsafe_allow_html=True)


    # =====================================================
    # MAIN METRICS
    # =====================================================

    highest_probability = max(
        probabilities.values()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Predicted Response",
            prediction,
        )

    with col2:

        st.metric(
            "Model Probability",
            f"{highest_probability:.2%}",
        )

    with col3:

        st.metric(
            "Classes Evaluated",
            len(probabilities),
        )


    # =====================================================
    # PROBABILITY BREAKDOWN
    # =====================================================

    st.markdown("""<div class="section-heading"><div class="section-icon">📊</div><div><h2 class="section-title">Probability Breakdown</h2><p class="section-description">Relative confidence across evaluated response classes.</p></div></div>""", unsafe_allow_html=True)

    for class_name, probability in probabilities.items():

        col1, col2 = st.columns([3, 1])

        with col1:

            st.write(
                f"**{class_name}**"
            )

            st.progress(
                probability
            )

        with col2:

            st.write(
                f"**{probability:.2%}**"
            )


    # =====================================================
    # INTERPRETATION
    # =====================================================

    st.divider()

    st.markdown("""<div class="section-heading"><div class="section-icon">💡</div><div><h2 class="section-title">Interpretation</h2><p class="section-description">A short explanation of the model output.</p></div></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="model-note">The model predicts <strong>{prediction}</strong> as the most likely company response for the information provided, with an estimated probability of <strong>{highest_probability:.2%}</strong>.</div>""", unsafe_allow_html=True)


    # =====================================================
    # MODEL NOTE
    # =====================================================

    with st.expander("ℹ️ About this prediction"):

        st.write(
            "This model predicts the company response category "
            "using complaint metadata and engineered features."
        )

        st.write(
            "The current model does not perform semantic "
            "understanding of the complaint narrative. "
            "The narrative contributes through engineered "
            "features such as presence, length, and word count."
        )