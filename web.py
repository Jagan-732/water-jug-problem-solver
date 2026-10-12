import streamlit as st
import pandas as pd

from src.csp_allocator import demo_scenarios, solve_allocation
from src.diagnosis_engine import diagnose

st.set_page_config(
    page_title="AquaCity | Smart Water AI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: #f4f7fb;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102c4a 0%, #071a2d 100%);
}
[data-testid="stSidebar"] * {
    color: #f0f6ff !important;
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
.hero {
    background: linear-gradient(120deg, #103c68, #087eaa);
    padding: 30px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(16, 60, 104, .14);
}
.hero h1 {
    color: white;
    font-size: 34px;
    margin: 0;
}
.hero p {
    color: #d8efff;
    margin: 10px 0 0 0;
    font-size: 15px;
}
.section-title {
    color: #163653;
    font-size: 22px;
    font-weight: 700;
    margin: 16px 0 12px 0;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e1eaf3;
    padding: 19px 20px;
    border-radius: 15px;
    box-shadow: 0 3px 12px rgba(25, 60, 90, .04);
}
div[data-testid="stMetricLabel"] {
    color: #64788b;
}
div[data-testid="stMetricValue"] {
    color: #103c68;
}
div.stButton > button {
    background: #087eaa;
    color: white;
    border: 0;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}
div.stButton > button:hover {
    background: #075f83;
    color: white;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #e1eaf3;
    border-radius: 12px;
    overflow: hidden;
}
.info-card {
    background: white;
    padding: 19px;
    border: 1px solid #e1eaf3;
    border-radius: 15px;
    margin-bottom: 12px;
}
.info-card h4 {
    color: #163653;
    margin: 0 0 8px 0;
}
.info-card p {
    color: #64788b;
    margin: 0;
    font-size: 14px;
}
.small-note {
    color: #718399;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="padding:10px 0 22px 0;">
    <div style="font-size:35px;">💧</div>
    <div style="font-size:22px;font-weight:800;">AquaCity</div>
    <div style="font-size:12px;color:#a9c9e8;">
        SMART WATER INTELLIGENCE
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Overview",
        "Water Allocation",
        "CSP Performance",
        "Network Diagnosis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**SYSTEM STATUS**")
st.sidebar.success("Application running")
st.sidebar.caption("Academic prototype · Simulated data")

st.markdown("""
<div class="hero">
    <h1>💧 Smart City Water Management</h1>
    <p>Intelligent allocation · Constraint satisfaction · Fair distribution ·
    Knowledge-based diagnosis</p>
</div>
""", unsafe_allow_html=True)

scenarios = demo_scenarios()

if page == "Overview":
    st.markdown('<div class="section-title">System Overview</div>',
                unsafe_allow_html=True)

    normal_capacity, normal_zones = scenarios["normal"]
    drought_capacity, drought_zones = scenarios["drought"]

    st.markdown("""
    <div class="info-card">
        <h4>Welcome to AquaCity Intelligence</h4>
        <p>Explore water distribution scenarios, compare CSP search strategies,
        and investigate possible network faults using simulated sensor readings.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Operating Scenarios", "2", "Normal + Drought")
    c2.metric("AI Techniques", "3", "CSP · Search · Rules")
    c3.metric("Water Unit", "10,000 L", "Per allocation unit")

    st.markdown('<div class="section-title">Scenario Summary</div>',
                unsafe_allow_html=True)

    summary = pd.DataFrame([
        {
            "Scenario": "Normal",
            "Available Units": normal_capacity,
            "Zones": len(normal_zones),
            "Status": "Ready to simulate"
        },
        {
            "Scenario": "Drought",
            "Available Units": drought_capacity,
            "Zones": len(drought_zones),
            "Status": "Ready to simulate"
        }
    ])
    st.dataframe(summary, use_container_width=True, hide_index=True)

    left, right = st.columns(2)
    with left:
        st.markdown("""
        <div class="info-card">
            <h4>🏙️ Water Allocation</h4>
            <p>Distribute limited water between hospital, residential,
            and commercial zones while respecting constraints.</p>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="info-card">
            <h4>🧠 CSP Performance</h4>
            <p>Compare search nodes and backtracking with forward
            checking enabled and disabled.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("Choose a module from the sidebar to start a simulation.")

elif page == "Water Allocation":
    st.markdown('<div class="section-title">Water Distribution</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        scenario = st.selectbox("Supply Scenario", ["Normal", "Drought"])
        default_capacity, zones = scenarios[scenario.lower()]
        capacity = st.number_input(
            "Available water (units)",
            min_value=0,
            max_value=100,
            value=int(default_capacity),
            step=1
        )
        st.caption("1 unit = 10,000 litres")

        run = st.button("⚡ Calculate Allocation", type="primary",
                        use_container_width=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>Allocation objective</h4>
            <p>Find a feasible distribution under reservoir capacity and
            zone constraints. Hospital priority is considered by the
            educational allocation model.</p>
        </div>
        """, unsafe_allow_html=True)

    if run:
        try:
            result = solve_allocation(
                int(capacity), zones,
                propagation=True, heuristic=True
            )

            if not result.feasible:
                st.error(result.message)
            else:
                total = sum(result.allocation.values())
                a, b, c, d = st.columns(4)
                a.metric("Reservoir Capacity", f"{capacity} units")
                b.metric("Water Allocated", f"{total} units")
                c.metric("Search Nodes", result.nodes)
                d.metric("Backtracks", result.backtracks)

                rows = []
                for zone in zones:
                    amount = result.allocation[zone.name]
                    rows.append({
                        "Zone": zone.name,
                        "Allocated Units": amount,
                        "Water (Litres)": amount * 10000,
                        "Minimum Units": zone.minimum,
                        "Demand Units": zone.demand,
                        "Minimum Met": amount >= zone.minimum
                    })

                st.markdown('<div class="section-title">Allocation Results</div>',
                            unsafe_allow_html=True)
                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True
                )

                chart_data = pd.DataFrame(rows).set_index("Zone")
                st.markdown('<div class="section-title">Supply vs Demand</div>',
                            unsafe_allow_html=True)
                st.bar_chart(chart_data[["Allocated Units", "Demand Units"]])

                if all(row["Minimum Met"] for row in rows):
                    st.success("All minimum supply requirements are met.")
                else:
                    st.warning("Some minimum supply requirements are unmet.")

                with st.expander("Algorithm details"):
                    st.write("Solver message:", result.message)
                    st.write("Execution time (ms):", result.elapsed_ms)
        except (ValueError, KeyError, AttributeError) as error:
            st.error(f"Allocation error: {error}")

elif page == "CSP Performance":
    st.markdown('<div class="section-title">Constraint Solver Performance</div>',
                unsafe_allow_html=True)
    scenario = st.selectbox("Scenario", ["Normal", "Drought"])
    capacity, zones = scenarios[scenario.lower()]

    st.caption("Compare the same scenario with forward checking on and off.")

    if st.button("▶ Run Performance Comparison", type="primary"):
        results = []
        for enabled in [False, True]:
            result = solve_allocation(
                capacity, zones,
                propagation=enabled,
                heuristic=True
            )
            results.append({
                "Forward Checking": "ON" if enabled else "OFF",
                "Feasible": result.feasible,
                "Search Nodes": result.nodes,
                "Backtracks": result.backtracks,
                "Execution Time (ms)": round(result.elapsed_ms, 3)
            })

        frame = pd.DataFrame(results)
        st.dataframe(frame, use_container_width=True, hide_index=True)
        st.markdown('<div class="section-title">Search Nodes Comparison</div>',
                    unsafe_allow_html=True)
        st.bar_chart(frame.set_index("Forward Checking")[["Search Nodes"]])
        st.caption("Execution times vary between runs. Forward checking does "
                   "not guarantee fewer backtracks for every problem.")

elif page == "Network Diagnosis":
    st.markdown('<div class="section-title">Network Fault Diagnosis</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <h4>Knowledge-based reasoning</h4>
        <p>Choose simulated sensor readings to trigger the prototype's
        diagnostic rules. Certainty factors are illustrative, not calibrated
        real-world probabilities.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        pressure = st.selectbox("Water Pressure", ["low", "normal", "high"])
    with c2:
        flow = st.selectbox("Water Flow", ["low", "normal", "high"])

    if st.button("🔍 Diagnose Network", type="primary"):
        try:
            findings = diagnose(pressure, flow)
            if not findings:
                st.info("No matching diagnosis rule was triggered.")

            for finding in findings:
                st.markdown('<div class="info-card">',
                            unsafe_allow_html=True)
                st.subheader(finding["conclusion"])
                st.write(finding["explanation"])
                certainty = max(
                    0.0, min(1.0, float(finding["certainty_factor"]))
                )
                st.progress(certainty)
                st.write(f"Illustrative certainty factor: {certainty:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

            st.warning("Simulated educational results only. Confirm faults "
                       "using real sensors and qualified inspection.")
        except (ValueError, KeyError, TypeError) as error:
            st.error(f"Diagnosis error: {error}")

st.markdown("---")
st.markdown(
    '<p class="small-note">AquaCity · Smart City Water Allocation System · '
    'Academic demonstration using simulated data</p>',
    unsafe_allow_html=True
)
