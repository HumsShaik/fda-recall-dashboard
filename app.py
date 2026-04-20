import pandas as pd
import streamlit as st

# Page setup
st.set_page_config(page_title="FDA Recall Dashboard", layout="wide")

st.title("📊 FDA Recall Intelligence Dashboard")
st.write("Upload any FDA recall dataset CSV and analyze it instantly.")

# Upload file
uploaded_file = st.file_uploader("Upload FDA CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.write(df.head())

    st.subheader("📌 Columns in Dataset")
    st.write(df.columns)

    # ---------------------------
    # FIND RELEVANT COLUMNS SAFELY
    # ---------------------------

    company_col = None
    reason_col = None

    for col in df.columns:
        col_lower = col.lower()

        if not company_col and ("firm" in col_lower or "company" in col_lower or "manufacturer" in col_lower):
            company_col = col

        if not reason_col and "reason" in col_lower:
            reason_col = col

    # ---------------------------
    # INSIGHTS
    # ---------------------------

    st.subheader("📊 Insights")

    if company_col:
        st.write("### Top Companies / Firms")
        st.bar_chart(df[company_col].value_counts().head(10))
    else:
        st.warning("No company/firm column found")

    if reason_col:
        st.write("### Top Recall Reasons")
        st.bar_chart(df[reason_col].value_counts().head(10))
    else:
        st.warning("No reason column found")

    # ---------------------------
    # SMART CHATBOT (NO API)
    # ---------------------------

    st.subheader("🤖 Smart Query Assistant")

    q = st.text_input("Ask something (e.g., top company, reason, summary, count)")

    if q:
        q = q.lower()

        # Count
        if "count" in q:
            st.success(f"Total records: {len(df)}")

        # Top companies
        elif "company" in q or "firm" in q or "top" in q:
            if company_col:
                st.write(df[company_col].value_counts().head(10))
            else:
                st.error("No company column found in dataset")

        # Reasons
        elif "reason" in q:
            if reason_col:
                st.write(df[reason_col].value_counts().head(10))
            else:
                st.error("No reason column found in dataset")

        # Summary
        elif "summary" in q:
            summary_text = ""

            if company_col and reason_col:
                top_company = df[company_col].value_counts().idxmax()
                top_reason = df[reason_col].value_counts().idxmax()

                summary_text = f"""
                📌 Summary of Dataset:
                - Total records: {len(df)}
                - Most active company: {top_company}
                - Most common issue: {top_reason}
                """
            else:
                summary_text = "Dataset does not have expected columns for summary."

            st.info(summary_text)

        else:
            st.warning("Try: top company, reason, summary, or count")