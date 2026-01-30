import streamlit as st

st.title("💧 Reservoir Volume Calculator")

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
height_options = sorted(HEIGHT_VOLUME.keys())
selected_height = st.selectbox("Select Water Height (m)", height_options, index=height_options.index(4.0))

cumulative_volume = HEIGHT_VOLUME[selected_height]
above_sea_level = SEA_LEVEL_ZERO + selected_height

st.metric(label="Cumulative Volume", value=f"{cumulative_volume:,.0f} m³")
st.metric(label="Above Sea Level", value=f"{above_sea_level:.3f} m")

st.caption("Cumulative volume values are based on the provided height table.")
