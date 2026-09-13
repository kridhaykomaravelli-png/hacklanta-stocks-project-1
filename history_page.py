import streamlit as st
import pandas as pd
from database import init_db, get_search_history, delete_all_history, delete_history_item

init_db()

st.title("Search History")

top_col1, top_col2 = st.columns([1, 1])


with top_col1:
    if st.button("Refresh History"):
        st.rerun()

with top_col2:
    if st.button("Delete All History", type="primary"):
        delete_all_history()
        st.success("All history deleted.")
        st.rerun()

rows = get_search_history()

if not rows:
    st.info("No history yet.")
else:
    df = pd.DataFrame(
        rows,
        columns=["ID", "Asset Type", "Ticker", "Score", "Label", "Created At"]
    )

    st.subheader("Saved Searches")
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True)

    st.subheader("Delete Individual Items")
    for row in rows:
        item_id, asset_type, ticker, score, label, created_at = row
        col1, col2 = st.columns([6, 1])

        with col1:
            st.write(f"**{ticker}** | {asset_type} | Score: {score} | {label} | {created_at}")

        with col2:
            if st.button("Delete", key=f"delete_{item_id}"):
                delete_history_item(item_id)
                st.success(f"Deleted {ticker} from history.")
                st.rerun()
