import streamlit as st
st.set_page_config(page_title="Risk-PWA", page_icon="🛡️", layout="centered")

# Super-simple risk engine
C = {"germany": 1, "usa": 1, "china": 3, "egypt": 3, "somalia": 5, "netherlands": 1}
M = {"air": 0.7, "sea": 1.0, "land": 1.4}

value = st.number_input("💰 Load value ($)", 0, 10000000, 500000, 10000)
n = st.number_input("🧭 Legs", 1, 6, 2)

locations, modes = [], [] 
for i in range(n):
    c1, c2 = st.columns([2, 1])
    loc = c1.text_input(f"Leg {i+1} location", key=f"l{i}").strip()
    mod = c2.selectbox("Mode", ["land", "sea", "air"], key=f"m{i}")
    locations.append(loc.lower())
    modes.append(mod.lower())

if st.button("⚡ Calculate", use_container_width=True, type="primary"):
    base = max(C.get(l, 3) for l in locations)
    base += (len(locations) - 1) * 0.25
    base *= max(M.get(m, 1) for m in modes)
    val_mult = min(5, value / 1e6)
    score = min(100, (base * 0.7 + val_mult * 0.3) * 20)
    color = "🟢" if score < 33 else "🟡" if score < 66 else "🔴"
    st.metric("Risk", f"{score:.1f}/100")
    st.caption(color + " → Add this page to your home screen!")
