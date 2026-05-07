import streamlit as st

st.set_page_config(layout="centered")
st.title("iPhone Screen Share")

vdo_link = st.text_input(
    "VDO.Ninja Viewer URL",
    value="https://vdo.ninja/?view=YOUR_ID"
)

st.markdown(
    """
    <style>
    .phone-frame {
        width: 390px;
        height: 760px;
        margin: auto;
        border-radius: 24px;
        overflow: hidden;
        border: 2px solid #333;
        background: #000;
    }
    .phone-frame iframe {
        width: 100%;
        height: 100%;
        border: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="phone-frame">
        <iframe src="{vdo_link}" allow="camera; microphone; autoplay; fullscreen"></iframe>
    </div>
    """,
    unsafe_allow_html=True
)
