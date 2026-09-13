import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from scoring import score_stock
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


def render_line_chart(hist, key_prefix):
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


def render_candlestick_chart(hist, key_prefix):
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


st.title("Stock Buy Checker")
st.write("Educational only — not financial advice.")


ticker = st.text_input("Enter a stock ticker", "AAPL").upper()
period = st.selectbox(
    "Choose timeframe",
    ["1mo", "3mo", "6mo", "1y", "5y"],
    index=2,
    key="stock_period"
)

if "stock_hist" not in st.session_state:
    st.session_state.stock_hist = None
if "stock_result" not in st.session_state:
    st.session_state.stock_result = None
if "stock_ticker" not in st.session_state:
    st.session_state.stock_ticker = ""
if "stock_period_saved" not in st.session_state:
    st.session_state.stock_period_saved = ""
if "stock_last_saved_key" not in st.session_state:
    st.session_state.stock_last_saved_key = None

if st.button("Analyze Stock"):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period=period)

        if hist.empty:
            st.error("No data found for that ticker.")
        else:
            result = score_stock(info, hist)

            st.session_state.stock_hist = hist
            st.session_state.stock_result = result
            st.session_state.stock_ticker = ticker
            st.session_state.stock_period_saved = period

            current_save_key = f"{ticker}_{period}_{result['score']}_{result['label']}"
            if st.session_state.stock_last_saved_key != current_save_key:
                save_search("stock", ticker, result["score"], result["label"])
                st.session_state.stock_last_saved_key = current_save_key

            st.success("Stock result saved to database.")

    except Exception as e:
        st.error(f"Error: {e}")

if st.session_state.stock_hist is not None and st.session_state.stock_result is not None:
    hist = st.session_state.stock_hist
    result = st.session_state.stock_result
    saved_ticker = st.session_state.stock_ticker
    saved_period = st.session_state.stock_period_saved

    st.subheader(f"Result for {saved_ticker}")
    st.write(f"Timeframe: **{saved_period}**")
    st.write(f"Score: **{result['score']} / 4**")
    st.write(f"Recommendation: **{result['label']}**")

    st.write("### Reasons")
    for reason in result["reasons"]:
        st.write(f"- {reason}")

    st.write("### Price Chart")

    chart_type = st.radio(
        "Choose chart type",
        ["Line", "Candlestick"],
        horizontal=True,
        key="stock_chart_type"
    )

    if chart_type == "Line":
        render_line_chart(hist, "stock")
    else:
        render_candlestick_chart(hist, "stock")

    latest_volume = hist["Volume"].iloc[-1] if "Volume" in hist.columns and not hist["Volume"].empty else None
    avg_volume = hist["Volume"].mean() if "Volume" in hist.columns and not hist["Volume"].empty else None

    st.write("### Volume")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Latest Volume", format_volume(latest_volume))
    with col2:
        st.metric("Average Volume", format_volume(avg_volume))
