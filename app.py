import altair as alt
import pandas as pd
import streamlit as st

st.markdown(
    "<h4 style='margin-bottom:0.25rem; white-space:nowrap; text-align:right; direction:rtl;'>💧 מאגר בית שערים</h4>",
    unsafe_allow_html=True,
)

# --- CHANGED: Dictionary keys now represent Absolute Height (50.0 - 58.5) ---
# Original 0.0 is now 50.0
HEIGHT_VOLUME = { 
    51.5: 4000,
    52.0: 11628,
    52.5: 27317,
    53.0: 53421,
    53.5: 88189,
    54.0: 126590,
    54.5: 166717,
    55.0: 208299,
    55.5: 251107,
    56.0: 295037,
    56.5: 340045,
    57.0: 386106,
    57.5: 433249,
    58.0: 481540,
    58.5: 531045,
    59: 581859,
    59.5: 634148
}

# Constants
MIN_ABS_HEIGHT = 50.0
MAX_ABS_HEIGHT = 59.5
RELATIVE_OFFSET = 50.608  # The offset added when input is < 10

# Input
user_input = st.number_input(
    "גובה המים (מ')",
    min_value=0.0,
    value=6.1,
    step=0.01,
)

# --- LOGIC: Determine Absolute Height ---
if user_input < 10:
    # Relative input: Add 50.608
    final_height = user_input + RELATIVE_OFFSET
    input_type = "relative"
elif user_input > 50:
    # Absolute input: Use as is
    final_height = user_input
    input_type = "absolute"
else:
    # Input is between 10 and 50 (ambiguous/invalid based on rules)
    st.error("ערך לא חוקי. נא להזין גובה נמוך מ-10 (יחסי) או מעל 50 (אבסולוטי).")
    st.stop()

# --- VALIDATION: Check if calculated height is within reservoir limits ---
if final_height < MIN_ABS_HEIGHT or final_height > MAX_ABS_HEIGHT:
    st.error(f"חריגה מגבולות המאגר. הגובה המחושב ({final_height:.3f} מ') חייב להיות בטווח {MIN_ABS_HEIGHT}-{MAX_ABS_HEIGHT}")
    st.stop()

# --- CALCULATION: Interpolate Volume based on final_height ---
# We need to find the nearest 0.5 steps in the absolute range (e.g. 50.0, 50.5, 51.0...)
lower_step = round((final_height // 0.5) * 0.5, 2)
upper_step = round(lower_step + 0.5, 2)

# Handle edge case where upper_step might exceed max dict key due to float math
if upper_step > MAX_ABS_HEIGHT:
    upper_step = MAX_ABS_HEIGHT
    lower_step = MAX_ABS_HEIGHT - 0.5

lower_volume = HEIGHT_VOLUME.get(lower_step, 0)
upper_volume = HEIGHT_VOLUME.get(upper_step, HEIGHT_VOLUME[MAX_ABS_HEIGHT])

if upper_step == lower_step:
    cumulative_volume = lower_volume
else:
    # Interpolation
    fraction = (final_height - lower_step) / 0.5
    cumulative_volume = lower_volume + (upper_volume - lower_volume) * fraction

# --- DISPLAY METRICS ---
st.markdown(
    f"""
    <div style="display:flex; gap:12px; align-items:flex-start; justify-content:space-between; direction:rtl;">
      <div style="font-size:0.8rem; white-space:nowrap; text-align:right;">
        <strong>נפח מצטבר</strong><br><span style="font-size:1.05rem;">{cumulative_volume:,.0f}</span> מ״ק
      </div>
      <div style="font-size:0.8rem; white-space:nowrap; text-align:right;">
        <strong>גובה מעל פני הים</strong><br>{final_height:.3f} מ׳
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div style='margin-top:0.5rem; text-align:right; direction:rtl; font-size:0.8rem; font-weight:600;'>גרף נפח לפי גובה</div>",
    unsafe_allow_html=True,
)

# --- GRAPH ---
# Create dataframe directly from the absolute HEIGHT_VOLUME map
points = [{"AbsHeight": h, "Volume": v} for h, v in sorted(HEIGHT_VOLUME.items())]

# Split into Blue (filled) and Gray (empty)
blue_points = [p for p in points if p["AbsHeight"] <= final_height]

# Ensure the exact current point is included in the blue line
if not any(p["AbsHeight"] == final_height for p in blue_points):
    blue_points.append({
        "AbsHeight": final_height,
        "Volume": cumulative_volume
    })
blue_points = sorted(blue_points, key=lambda p: p["AbsHeight"])

# The gray line starts from the current point to the end
gray_points = [{
    "AbsHeight": final_height,
    "Volume": cumulative_volume
}]
gray_points.extend([p for p in points if p["AbsHeight"] > final_height])
gray_points = sorted(gray_points, key=lambda p: p["AbsHeight"])

blue_df = pd.DataFrame(blue_points)
gray_df = pd.DataFrame(gray_points)

# Chart Config
x_domain = [MIN_ABS_HEIGHT, MAX_ABS_HEIGHT]

blue_line = alt.Chart(blue_df).mark_line(color="#1f77b4").encode(
    x=alt.X("AbsHeight", title="גובה מעל פני הים (מ')", scale=alt.Scale(domain=x_domain, zero=False)),
    y=alt.Y("Volume", title="נפח (מ״ק)"),
).properties(height=220)

gray_line = alt.Chart(gray_df).mark_line(color="#9aa0a6").encode(
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
