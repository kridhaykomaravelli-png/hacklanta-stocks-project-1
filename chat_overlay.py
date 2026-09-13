import streamlit as st
from database import get_search_history


def _build_history_summary():
    
    rows = get_search_history()
    if not rows:
        return "There is no saved search history yet."

    latest = rows[:5]
    parts = []
    for row in latest:
        item_id, asset_type, ticker, score, label, created_at = row
        parts.append(f"{ticker} ({asset_type}) - score {score}, label: {label}")

    return "Recent saved searches: " + "; ".join(parts)


def _assistant_reply(user_text: str) -> str:
    text = user_text.lower().strip()

    if "history" in text or "recent searches" in text:
        return _build_history_summary()

    if "chart" in text or "charts" in text or "graph" in text or "graphs" in text:
        return (
            "This app supports two chart types: Line and Candlestick. "
            "Line charts show the closing price over time. Candlestick charts show open, high, low, and close prices. "
            "You can also use the drawing tools on the charts to draw lines, shapes, and mark trends."
        )

    if "candlestick" in text:
        return (
            "Candlestick charts show open, high, low, and close prices. "
            "Green means price closed higher than it opened. Red means it closed lower."
        )

    if "line chart" in text or "line charts" in text:
        return "A line chart is simpler and shows the closing price over time."

    if "timeframe" in text or "time frame" in text or "period" in text:
        return (
            "Use the timeframe selector above Analyze. "
            "Short ranges like 1mo show recent movement. Longer ranges like 1y or 5y show the bigger trend."
        )

    if "volume" in text:
        return (
            "Under each chart, the app shows two volume metrics: Latest Volume and Average Volume. "
            "This helps show how actively the asset is being traded."
        )

    if "stock" in text and "crypto" in text:
        return (
            "Stocks are shares of companies. Crypto assets are digital tokens and are usually more volatile. "
            "The Stocks page scores companies, while the Crypto page mainly shows price history."
        )

    if "stock" in text:
        return (
            "The Stocks page lets you enter a company ticker like AAPL or MSFT, choose a timeframe, "
            "see a score, reasons, a chart, and volume data."
        )

    if "crypto" in text:
        return (
            "The Crypto page lets you enter a crypto ticker like BTC-USD or ETH-USD, choose a timeframe, "
            "view line or candlestick charts, and see volume data."
        )

    if "index fund" in text or "etf" in text or "fund" in text:
        return (
            "Index funds and ETFs usually track a basket of assets, which makes them more diversified than a single stock. "
            "Try tickers like VOO, SPY, IVV, VTI, or QQQ."
        )

    if "btc" in text or "bitcoin" in text:
        return "Use BTC-USD on the Crypto page."

    if "eth" in text or "ethereum" in text:
        return "Use ETH-USD on the Crypto page."

    if "spy" in text or "voo" in text or "s&p 500" in text:
        return "For S&P 500 style funds, try SPY, VOO, or IVV on the Index Funds page."

    if "help" in text or "how do i use" in text or "how to use" in text:
        return (
            "Pick a page at the top, type a ticker, choose a timeframe, and press Analyze. "
            "Then switch between Line and Candlestick charts if you want."
        )

    if "score" in text or "recommendation" in text:
        return (
            "The Stocks and Index Funds pages use simple scoring rules. "
            "Higher scores mean the asset looked stronger based on the current checks."
        )

    return (
        "Try asking about charts, candlesticks, timeframes, volume, tickers, stocks, crypto, ETFs, or search history."
    )


def render_chat_overlay():
    if "overlay_chat_messages" not in st.session_state:
        st.session_state.overlay_chat_messages = [
            {
                "role": "assistant",
                "content": "Hi! Ask me about charts, timeframes, volume, tickers, stocks, crypto, ETFs, or history."
            }
        ]

    st.markdown(
        """
        <style>
        div[data-testid="stPopover"] {
            position: fixed;
            right: 20px;
            bottom: 20px;
            z-index: 999999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.popover("💬 Assistant"):
        st.caption("Quick help")

        for msg in st.session_state.overlay_chat_messages[-6:]:
            if msg["role"] == "assistant":
                st.markdown(f"**Assistant:** {msg['content']}")
            else:
                st.markdown(f"**You:** {msg['content']}")

        user_text = st.text_input("Ask something", key="overlay_chat_input")

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Send", key="overlay_send"):
                if user_text.strip():
                    st.session_state.overlay_chat_messages.append(
                        {"role": "user", "content": user_text}
                    )
                    reply = _assistant_reply(user_text)
                    st.session_state.overlay_chat_messages.append(
                        {"role": "assistant", "content": reply}
                    )
                    st.rerun()

        with col2:
            if st.button("Clear", key="overlay_clear"):
                st.session_state.overlay_chat_messages = [
                    {
                        "role": "assistant",
                        "content": "Chat cleared. Ask me anything about the app."
                    }
                ]
                st.rerun()
