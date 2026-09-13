import streamlit as st
from database import init_db
from chat_overlay import render_chat_overlay
from buy_button import render_buy_button


st.set_page_config(page_title="Stock & Crypto Checker", layout="wide")

init_db()

home = st.Page("home_page.py", title="Home", icon="🏠")
stocks = st.Page("stocks_page.py", title="Stocks", icon="📈")
crypto = st.Page("crypto_page.py", title="Crypto", icon="🪙")
index_funds = st.Page("index_funds_page.py", title="Index Funds", icon="📊")
history = st.Page("history_page.py", title="History", icon="🕘")

pg = st.navigation(
    [home, stocks, crypto, index_funds, history],
    position="top"
)

pg.run()

render_buy_button()
render_chat_overlay()
