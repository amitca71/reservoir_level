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
    0.5: 4027,
    1.0: 11655,
    1.5: 27344,
    2.0: 53448,
    2.5: 88216,
    3.0: 126617,
    3.5: 166744,
    4.0: 208327,
    4.5: 251136,
    5.0: 295066,
    5.5: 340074,
    6.0: 386135,
    6.5: 433278,
    7.0: 481569,
    7.5: 531074,
    8.0: 581888,
    8.5: 634177,
}

SEA_LEVEL_ZERO = 50.608

selected_height = st.number_input(
    "גובה המים (מ')",
    min_value=0.0,
    max_value=8.5,
    value=6.1,
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
      <div style="font-size:0.8rem; white-space:nowrap; text-align:right;">
        <strong>נפח מצטבר</strong><br><span style="font-size:1.05rem;">{cumulative_volume:,.0f}</span> מ״ק
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

# --- 1. PREPARE DATA WITH ABSOLUTE HEIGHT ---
# We calculate 'AbsHeight' (Absolute Height) for every point
points = [{"Height": h, "AbsHeight": h + SEA_LEVEL_ZERO, "Volume": v} for h, v in sorted(HEIGHT_VOLUME.items())]

# --- 2. SPLIT DATA FOR COLORING ---
blue_points = [p for p in points if p["Height"] <= selected_height]
if not any(p["Height"] == selected_height for p in blue_points):
    # Add the specifically selected point
    blue_points.append({
        "Height": selected_height, 
        "AbsHeight": above_sea_level, 
        "Volume": cumulative_volume
    })
blue_points = sorted(blue_points, key=lambda p: p["Height"])

gray_points = [{
    "Height": selected_height, 
    "AbsHeight": above_sea_level, 
    "Volume": cumulative_volume
}]
gray_points.extend([p for p in points if p["Height"] > selected_height])
gray_points = sorted(gray_points, key=lambda p: p["Height"])

blue_df = pd.DataFrame(blue_points)
gray_df = pd.DataFrame(gray_points)

# --- 3. CHART CONFIGURATION ---
# We define the domain for the X axis based on min/max absolute sea levels
x_domain = [SEA_LEVEL_ZERO, SEA_LEVEL_ZERO + 8.5]

blue_line = alt.Chart(blue_df).mark_line(color="#1f77b4").encode(
    # Changed x to use "AbsHeight"
    x=alt.X("AbsHeight", title="גובה מעל פני הים (מ')", scale=alt.Scale(domain=x_domain, zero=False)),
    y=alt.Y("Volume", title="נפח (מ״ק)"),
).properties(height=220)

gray_line = alt.Chart(gray_df).mark_line(color="#9aa0a6").encode(
    # Changed x to use "AbsHeight"
    x=alt.X("AbsHeight", scale=alt.Scale(domain=x_domain, zero=False)),
    y="Volume",
).properties(height=220)

chart = (blue_line + gray_line).configure_view(strokeWidth=0).configure_axis(
    labelPadding=2, titlePadding=4
)
st.altair_chart(chart, use_container_width=True)

st.markdown(
    "<div style='text-align:right; direction:rtl; font-size:0.75rem; margin-top:0.05rem;'>"
    "מופעל על ידי יאיר ועמית כהנוביץ. צאצאי משפחת כהנוביץ, ממיסדי מושב בית שערים"
    "</div>",
    unsafe_allow_html=True,
)
