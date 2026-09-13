import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


def render_buy_button():
    gif_path = Path("chow.gif")

    if not gif_path.exists():
        st.warning("chow.gif was not found in the project folder.")
        return

    gif_base64 = base64.b64encode(gif_path.read_bytes()).decode("utf-8")

    popup_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Buy Stock</title>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background: black;
                display: flex;
                justify-content: center;
                align-items: center;
