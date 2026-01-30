import streamlit as st

st.title("💧 Beit Shearim Reservoir Volume")

# Fixed reference data (Height -> Cumulative Volume)
HEIGHT_VOLUME = {
    0.0: 0,
    0.5: 2013,
    1.0: 9641,
    1.5: 25331,
    2.0: 51435,
    2.5: 86203,
    3.0: 124604,
    3.5: 164730,
    4.0: 206313,
    4.5: 249121,
    5.0: 293050,
    5.5: 338059,
    6.0: 384120,
    6.5: 431262,
    7.0: 479554,
    7.5: 529058,
    8.0: 579873,
    8.5: 632162,
}

SEA_LEVEL_ZERO = 51.108

st.header("Field Measurement")
selected_height = st.number_input(
    "Water Height (m)",
    min_value=0.0,
    max_value=8.5,
    value=4.0,
    step=0.01,
)

# Linear interpolation between the nearest 0.5m levels
lower_step = round((selected_height // 0.5) * 0.5, 2)
upper_step = round(min(lower_step + 0.5, 8.5), 2)
lower_volume = HEIGHT_VOLUME[lower_step]
upper_volume = HEIGHT_VOLUME[upper_step]

if upper_step == lower_step:
    cumulative_volume = lower_volume
else:
    fraction = (selected_height - lower_step) / 0.5
    cumulative_volume = lower_volume + (upper_volume - lower_volume) * fraction

above_sea_level = SEA_LEVEL_ZERO + selected_height

st.metric(label="Cumulative Volume", value=f"{cumulative_volume:,.0f} m³")
st.metric(label="Above Sea Level", value=f"{above_sea_level:.3f} m")

st.caption("Cumulative volume values are based on the provided height table.")
st.caption("Powered by Yair and Amit Kahanovitch. Descendants of Kahanovitch family, Beit Shearim pioneers")
