import streamlit as st
import os
import numpy as np
from models.logistic import logistic_curve
from utils.plotting import plot_logistic

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

#  Custom CSS tweaks 
st.markdown(
    """
    <style>
    /* Sidebar width */
    [data-testid="stSidebar"] {
        min-width: 203px;
        max-width: 203px;
    }

    /* Compact sliders: reduce vertical padding */
    div[data-testid="stSlider"] {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }

    /* Reduce default margins for wider content */
    .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📈 Logistic Growth Dashboard")

#Sidebar: baseline scenario + reset button
st.sidebar.title("Baseline Scenario")

profiles = {
    "Default": {"K": 1000, "r": 0.2, "P0": 20, "t_max": 50},
    "High Growth": {"K": 1000, "r": 0.5, "P0": 20, "t_max": 60},
    "Large Capacity": {"K": 3000, "r": 0.2, "P0": 20, "t_max": 50},
}

baseline_option = st.sidebar.selectbox(
    "Choose comparison baseline",
    list(profiles.keys())
)
baseline = profiles[baseline_option]

def reset_to_baseline():
    st.session_state["K"] = baseline["K"]
    st.session_state["r"] = baseline["r"]
    st.session_state["P0"] = baseline["P0"]
    st.session_state["t_max"] = baseline["t_max"]

st.sidebar.button("Reset sliders to baseline", on_click=reset_to_baseline)

#Baseline metrics for comparison 
baseline_c = (baseline["K"] - baseline["P0"]) / baseline["P0"]
baseline_inflect = (1 / baseline["r"]) * np.log(baseline_c)
baseline_t90 = (1 / baseline["r"]) * np.log(9 * baseline_c)

# Main layout: 3 columns 
col_controls, col_plot, col_diag = st.columns([2, 5, 3])

# Controls expander (open by default)
with col_controls:
    with st.expander("⚙️ Adjust sliders/Parameters", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            K = st.slider(
                "Carrying Capacity (K)", 100, 5000,
                value=st.session_state.get("K", 1000), step=100
            )
            P0 = st.slider(
                "Initial Population (P₀)", 1, K,
                value=st.session_state.get("P0", 20), step=1
            )
        with c2:
            r = st.slider(
                "Growth Rate (r)", 0.01, 1.0,
                value=st.session_state.get("r", 0.2), step=0.01
            )
            t_max = st.slider(
                "Time Horizon (t_max)", 10, 200,
                value=st.session_state.get("t_max", 50), step=5
            )

# Plot column
with col_plot:
    t, P, c = logistic_curve(K, r, P0, t_max)
    fig = plot_logistic(t, P, K, r, c)
    st.pyplot(fig)

    if st.button("Export Plot"):
        filepath = os.path.join("assets", "logistic_plot.png")
        fig.savefig(filepath, dpi=300, bbox_inches="tight")
        st.success(f"Plot saved to {filepath} (300 DPI, publication quality)")

# Diagnostics column
with col_diag:
    with st.expander("📊 Model Diagnostics", expanded=False):
        st.info(f"Comparisons shown relative to the **{baseline_option}** scenario.")

        col1, col2 = st.columns(2)

        # Left column: computed metrics
        with col1:
            if c > 0 and r > 0:
                t_inflect = (1 / r) * np.log(c)
                if np.isfinite(t_inflect) and t_inflect > 0:
                    st.metric(
                        label="Inflection Time ⏱️",
                        value=f"{t_inflect:.2f}",
                        delta="▲ later" if t_inflect > baseline_inflect else "▼ sooner",
                        help="Time when growth is fastest (curve bends)."

                    )
                    st.metric(
                        label="Pop @ Inflect. 👥",
                        value=f"{K/2:.2f}",
                        help="Population size at the inflection time."

                    )

            try:
                t_90 = (1 / r) * np.log(9 * c)
                if np.isfinite(t_90) and t_90 > 0:
                    st.metric(
                        label="Time to 90% K 📈",
                        value=f"{t_90:.2f}",
                        delta="▲ slower" if t_90 > baseline_t90 else "▼ faster",
                        help="Time required to reach 90% of carrying capacity."
                    )
            except Exception:
                st.write("⚠️ Could not compute time to 90% capacity.")

        # Right column: parameter recap with color-coded labels
        with col2:
            st.markdown(f"<span style='color:green'>**Growth Rate (r):**</span> {r}", unsafe_allow_html=True)
            st.markdown(f"<span style='color:red'>**Carrying Capacity (K):**</span> {K}", unsafe_allow_html=True)
            st.markdown(f"<span style='color:blue'>**Initial Pop (P₀):**</span> {P0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color:purple'>**Time Horizon (tₘₐₓ):**</span> {t_max}", unsafe_allow_html=True)        # Right column: parameter recap with color-coded labels
