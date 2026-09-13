import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from database import init_db, save_search

init_db()



def format_volume(value):
    if value is None:
        return "N/A"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:.0f}"


def render_line_chart(hist):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            name="Close"
        )
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified"
    )

    config = {
        "displaylogo": False,
        "modeBarButtonsToAdd": [
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape"
        ]
    }

    st.plotly_chart(fig, use_container_width=True, config=config)


def render_candlestick_chart(hist):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=hist.index,
                open=hist["Open"],
                high=hist["High"],
                low=hist["Low"],
                close=hist["Close"],
                increasing_line_color="green",
                decreasing_line_color="red",
                name="Candlestick"
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    config = {
        "displaylogo": False,
        "modeBarButtonsToAdd": [
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape"
        ]
    }

    st.plotly_chart(fig, use_container_width=True, config=config)


st.title("Crypto Checker")
st.write("Search for a cryptocurrency and view recent price data.")

crypto = st.text_input("Enter a crypto ticker", "BTC-USD").upper()
period = st.selectbox(
    "Choose timeframe",
    ["1mo", "3mo", "6mo", "1y", "5y"],
    index=2,
    key="crypto_period"
)

if "crypto_hist" not in st.session_state:
    st.session_state.crypto_hist = None
if "crypto_ticker" not in st.session_state:
    st.session_state.crypto_ticker = ""
if "crypto_period_saved" not in st.session_state:
    st.session_state.crypto_period_saved = ""
if "crypto_last_saved_key" not in st.session_state:
    st.session_state.crypto_last_saved_key = None

if st.button("Analyze Crypto"):
    try:
        asset = yf.Ticker(crypto)
        hist = asset.history(period=period)

        if hist.empty:
            st.error("No data found for that crypto ticker.")
        else:
            st.session_state.crypto_hist = hist
            st.session_state.crypto_ticker = crypto
            st.session_state.crypto_period_saved = period

            current_save_key = f"{crypto}_{period}"
            if st.session_state.crypto_last_saved_key != current_save_key:
                save_search("crypto", crypto, 0, "Chart viewed")
                st.session_state.crypto_last_saved_key = current_save_key

            st.success("Crypto search saved to database.")

    except Exception as e:
        st.error(f"Error: {e}")

if st.session_state.crypto_hist is not None:
    hist = st.session_state.crypto_hist
    saved_crypto = st.session_state.crypto_ticker
    saved_period = st.session_state.crypto_period_saved

    st.subheader(f"{saved_crypto} Price")
    st.write(f"Timeframe: **{saved_period}**")
    st.write("### Price Chart")

    chart_type = st.radio(
        "Choose chart type",
        ["Line", "Candlestick"],
        horizontal=True,
        key="crypto_chart_type"
    )

    if chart_type == "Line":
        render_line_chart(hist)
    else:
        render_candlestick_chart(hist)

    latest_volume = hist["Volume"].iloc[-1] if "Volume" in hist.columns and not hist["Volume"].empty else None
    avg_volume = hist["Volume"].mean() if "Volume" in hist.columns and not hist["Volume"].empty else None

    st.write("### Volume")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Latest Volume", format_volume(latest_volume))
    with col2:
        st.metric("Average Volume", format_volume(avg_volume))
