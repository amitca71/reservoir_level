import altair as alt
import pandas as pd
import streamlit as st

st.markdown(
    "<h4 style='margin-bottom:0.25rem; white-space:nowrap; text-align:right; direction:rtl;'>💧 מאגר בית שערים</h4>",
    unsafe_allow_html=True,
)

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

selected_height = st.number_input(
    "גובה המים (מ')",
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

st.markdown(
    f"""
    <div style="display:flex; gap:12px; align-items:flex-start; justify-content:space-between; direction:rtl;">
      <div style="font-size:0.85rem; white-space:nowrap; text-align:right;">
        <strong>נפח מצטבר</strong><br>{cumulative_volume:,.0f} מ״ק
      </div>
      <div style="font-size:0.8rem; white-space:nowrap; text-align:right;">
        <strong>גובה מעל פני הים</strong><br>{above_sea_level:.3f} מ׳
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div style='margin-top:0.5rem; text-align:right; direction:rtl; font-size:0.8rem; font-weight:600;'>גרף נפח לפי גובה</div>",
    unsafe_allow_html=True,
)
points = [{"Height": h, "Volume": v} for h, v in sorted(HEIGHT_VOLUME.items())]

blue_points = [p for p in points if p["Height"] <= selected_height]
if not any(p["Height"] == selected_height for p in blue_points):
    blue_points.append({"Height": selected_height, "Volume": cumulative_volume})
blue_points = sorted(blue_points, key=lambda p: p["Height"])

gray_points = [{"Height": selected_height, "Volume": cumulative_volume}]
gray_points.extend([p for p in points if p["Height"] > selected_height])
gray_points = sorted(gray_points, key=lambda p: p["Height"])

blue_df = pd.DataFrame(blue_points)
gray_df = pd.DataFrame(gray_points)

blue_line = alt.Chart(blue_df).mark_line(color="#1f77b4").encode(
    x=alt.X("Height", title="גובה (מ')", scale=alt.Scale(domain=[0, 8.5])),
    y=alt.Y("Volume", title="נפח (מ״ק)"),
)
gray_line = alt.Chart(gray_df).mark_line(color="#9aa0a6").encode(
    x=alt.X("Height", scale=alt.Scale(domain=[0, 8.5])),
    y="Volume",
)

st.altair_chart(blue_line + gray_line, use_container_width=True)

st.markdown(
    "<div style='text-align:right; direction:rtl; font-size:0.75rem; margin-top:0.05rem;'>"
    "מופעל על ידי יאיר ועמית כהנוביץ. צאצאי משפחת כהנוביץ, ממיסדי מושב בית שערים"
    "</div>",
    unsafe_allow_html=True,
)
