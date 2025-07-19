# app.py  –  complete, updated
import streamlit as st

st.set_page_config(
    page_title="Risk-PWA",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- expanded risk tables ----------
COUNTRY_RISK = {
    # very low
    "germany": 1, "netherlands": 1, "belgium": 1, "luxembourg": 1,
    "usa": 1, "canada": 1, "united kingdom": 1, "france": 1,
    "singapore": 1, "switzerland": 1, "sweden": 1, "norway": 1,
    "denmark": 1, "finland": 1, "austria": 1, "australia": 1,
    "new zealand": 1, "japan": 1, "south korea": 1,

    # low–medium
    "spain": 2, "italy": 2, "portugal": 2, "czech republic": 2,
    "poland": 2, "hungary": 2, "slovakia": 2, "slovenia": 2,
    "estonia": 2, "latvia": 2, "lithuania": 2, "chile": 2,
    "panama": 2, "uae": 2, "malaysia": 2, "thailand": 2,

    # medium
    "china": 3, "india": 3, "brazil": 3, "mexico": 3, "argentina": 3,
    "south africa": 3, "turkey": 3, "greece": 3, "egypt": 3,
    "saudi arabia": 3, "qatar": 3, "vietnam": 3, "indonesia": 3,

    # high
    "russia": 4, "iran": 4, "iraq": 4, "nigeria": 4,
    "pakistan": 4, "bangladesh": 4, "venezuela": 4, "belarus": 4,
    "myanmar": 4, "ethiopia": 4, "libya": 4, "lebanon": 4,

    # extreme
    "somalia": 5, "afghanistan": 5, "yemen": 5, "syria": 5,
    "mali": 5, "central african republic": 5, "north korea": 5
}

MODALITY_FACTOR = {"air": 0.7, "sea": 1.0, "land": 1.4}

# ---------- UI ----------
st.title("🛡️ Supply-Chain Risk Quick-Check")

value_usd = st.number_input(
    "💰  Load value (USD)",
    min_value=0,
    max_value=100_000_000,
    value=500_000,
    step=10_000
)

n_legs = st.number_input("🧭  Number of legs", min_value=1, max_value=10, value=2)

locations, modalities = [], []
for i in range(n_legs):
    col1, col2 = st.columns([2, 1])
    loc = col1.text_input(
        f"Leg {i+1} location",
        placeholder="Country or city",
        key=f"loc_{i}"
    ).strip().lower()
    mod = col2.selectbox(
        "Mode",
        ["land", "sea", "air"],
        key=f"mod_{i}"
    ).lower()
    locations.append(loc)
    modalities.append(mod)

if st.button("⚡ Calculate risk", use_container_width=True, type="primary"):
    # Geography risk (max of all legs)
    geo_score = max(COUNTRY_RISK.get(loc, 3) for loc in locations)

    # Penalty for extra stops
    stop_penalty = (len(locations) - 1) * 0.25 * 5   # 0-5 scale

    # Modality multiplier (worst leg drives the factor)
    modality_mult = max(MODALITY_FACTOR.get(m, 1.0) for m in modalities)

    # Value severity (0-5)
    value_severity = min(5, max(1, value_usd / 1_000_000))

    # Final score 0-100
    raw = (geo_score + stop_penalty) * modality_mult + value_severity * 0.3
    risk = min(100, raw * 20)

    # Display
    color = "🟢" if risk < 33 else "🟡" if risk < 66 else "🔴"
    st.metric("Risk Score", f"{risk:.1f} / 100")
    st.caption(f"{color}  → Long-press → Add to Home Screen")

    # Optional explanation
    with st.expander("📊  Breakdown"):
        st.write(
            f"- Highest-risk location: **{max(locations, key=lambda x: COUNTRY_RISK.get(x,3))}** "
            f"({max(COUNTRY_RISK.get(l,3) for l in locations)}/5)\n"
            f"- Stops penalty: **+{stop_penalty:.1f}**\n"
            f"- Modality multiplier: **×{modality_mult:.1f}**\n"
            f"- Value severity: **{value_severity:.1f}/5**"
        )
 streamlit as st
