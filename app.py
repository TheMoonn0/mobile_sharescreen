import streamlit as st

st.set_page_config(layout="wide")

st.title("iPhone Screen Share")

vdo_link = st.text_input(
    "VDO.Ninja Viewer URL",
    value="https://vdo.ninja/?view=YOUR_ID"
)

st.components.v1.iframe(
    vdo_link,
    height=800,
    scrolling=False
)
