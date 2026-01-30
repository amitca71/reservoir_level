import streamlit as st

st.title("💧 Reservoir Volume Calculator")

# 1. Inputs
st.sidebar.header("Configuration")
base_area = st.sidebar.number_input("Base Area (sqm)", min_value=0.0, value=70000.0)
top_area = st.sidebar.number_input("Top Area (sqm)", min_value=0.0, value=100000.0)
max_depth = st.sidebar.number_input("Max Depth (m)", min_value=0.1, value=8.5, step=0.1)

if top_area < base_area:
    st.sidebar.error("Top Area must be greater than or equal to Base Area.")
    st.stop()

st.header("Field Measurement")
if "current_h" in st.session_state:
    st.session_state.current_h = min(st.session_state.current_h, max_depth)
current_h = st.number_input(
    "Current Water Height (m)",
    min_value=0.0,
    max_value=max_depth,
    value=min(4.0, max_depth),
    step=0.1,
    key="current_h",
)

# 2. Calculation
# Calculate area at current height (Linear Interpolation)
current_surface_area = base_area + ((current_h / max_depth) * (top_area - base_area))

# Calculate Volume: Average of Base Area and Current Surface Area * Height
volume = current_h * (base_area + current_surface_area) / 2

# 3. Output
st.metric(label="Total Water Volume", value=f"{volume:,.0f} m³")

# Visual feedback
fill_percent = current_h / max_depth
st.progress(fill_percent)
st.caption(f"The reservoir is {fill_percent*100:.1f}% full by height.")

# 4. Curve preview
st.subheader("Volume vs. Height")
steps = 50
heights = [max_depth * i / steps for i in range(steps + 1)]
volumes = []
for h in heights:
    surface_area = base_area + ((h / max_depth) * (top_area - base_area))
    volumes.append(h * (base_area + surface_area) / 2)
st.line_chart({"Height (m)": heights, "Volume (m³)": volumes})
