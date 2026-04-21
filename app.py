import pandas as pd
import streamlit as st

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="FDA Recall Dashboard",
    layout="wide",
    page_icon="📊"
)

# -------------------------
# HEADER
# -------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #2E86C1;'>📊 FDA Recall Intelligence Dashboard</h1>
    <p style='text-align: center;'>Analyze FDA recall datasets with smart insights</p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# -------------------------
# FILE UPLOAD
# -------------------------
uploaded_file = st.file_uploader("📂 Upload FDA CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # -------------------------
    # COLUMN DETECTION
    # -------------------------
    company_col = None
    reason_col = None

    for col in df.columns:
        col_lower = col.lower()

        if not company_col and ("firm" in col_lower or "company" in col_lower or "manufacturer" in col_lower):
            company_col = col

        if not reason_col and "reason" in col_lower:
            reason_col = col

    # -------------------------
    # METRICS (TOP KPIs)
    # -------------------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))

    if company_col:
        col2.metric("Unique Companies", df[company_col].nunique())
    else:
        col2.metric("Unique Companies", "N/A")

    if reason_col:
        col3.metric("Unique Reasons", df[reason_col].nunique())
    else:
        col3.metric("Unique Reasons", "N/A")

    st.markdown("---")

    # -------------------------
    # CHARTS (SIDE BY SIDE)
    # -------------------------
    st.subheader("📊 Insights")

    col1, col2 = st.columns(2)

    if company_col:
        with col1:
            st.markdown("### 🏢 Top Companies")
            st.bar_chart(df[company_col].value_counts().head(10))
    else:
        col1.warning("No company column found")

    if reason_col:
        with col2:
            st.markdown("### ⚠️ Recall Reasons")
            st.bar_chart(df[reason_col].value_counts().head(10))
    else:
        col2.warning("No reason column found")

    st.markdown("---")

    # -------------------------
    # DATA PREVIEW (EXPANDABLE)
    # -------------------------
    with st.expander("📄 View Raw Data"):
        st.dataframe(df)

    # -------------------------
    # SMART QUERY ASSISTANT
    # -------------------------
    st.subheader("🤖 Smart Query Assistant")

    q = st.text_input("Ask something (e.g., top company, reason, summary, count)")

    if q:
        q = q.lower()

        if "count" in q:
            st.success(f"Total records: {len(df)}")

        elif "company" in q or "firm" in q or "top" in q:
            if company_col:
                st.write(df[company_col].value_counts().head(10))
            else:
                st.error("No company column found")

        elif "reason" in q:
            if reason_col:
                st.write(df[reason_col].value_counts().head(10))
            else:
                st.error("No reason column found")

        elif "summary" in q:
            if company_col and reason_col:
                top_company = df[company_col].value_counts().idxmax()
                top_reason = df[reason_col].value_counts().idxmax()

                st.info(f"""
                📌 Summary:
                - Total records: {len(df)}
                - Top company: {top_company}
                - Top issue: {top_reason}
                """)
            else:
                st.warning("Not enough data for summary")

        else:
            st.warning("Try: top company, reason, summary, or count")