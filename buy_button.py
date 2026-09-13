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
                overflow: hidden;
            }}
            img {{
                max-width: 150vw;
                max-height: 150vh;
                
                object-fit: contain;
                display: block;
            }}
        </style>
    </head>
    <body>
        <img src="data:image/gif;base64,{gif_base64}" alt="Buy Stock Gif">
    </body>
    </html>
    """

    popup_html_js = popup_html.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    button_html = f"""
    <div style="text-align:center; margin-top:30px; margin-bottom:20px;">
        <button id="buy-btn" style="
            display:inline-block;
            background-color:#ff1f1f;
            color:white;
            font-size:28px;
            font-weight:800;
            padding:18px 42px;
            border-radius:14px;
            border:none;
            cursor:pointer;
            box-shadow:0 6px 18px rgba(255,0,0,0.35);
        ">
            BUY STOCK
        </button>
    </div>

    <script>
        const btn = document.getElementById("buy-btn");
        btn.addEventListener("click", function() {{
            const win = window.open("", "_blank");
            win.document.open();
            win.document.write(`{popup_html_js}`);
            win.document.close();
        }});
    </script>
    """

    components.html(button_html, height=110)
