import streamlit as st


@st.cache_data
def show_icon(emoji: str):
    """Shows an emoji as a Notion-style page icon.

    Args:
        emoji (str): name of the emoji, i.e. ":balloon:"
    """

    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )
