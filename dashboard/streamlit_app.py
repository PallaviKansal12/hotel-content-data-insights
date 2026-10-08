from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "content_evaluation_results.csv"

st.set_page_config(
    page_title="Hotel Content Insights",
    page_icon="🏨",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["risk_level"] = df["risk_level"].fillna("UNKNOWN").astype(str).str.upper()
    df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0)
    return df


df = load_data()

st.title("Hotel Content Insights Dashboard")
st.markdown(
    """
    This dashboard helps marketing and content teams decide whether AI-generated hotel descriptions are accurate,
    trustworthy, and ready to publish. It highlights factual mismatches, unsupported claims, and the share of content
    that needs human review before publication.
    """
)

risk_order = ["LOW", "MEDIUM", "HIGH"]
total_hotels = len(df)
mean_confidence = round(df["confidence"].mean() * 100, 1)
human_review_share = round(df["human_review_required"].mean() * 100, 1)

col1, col2, col3 = st.columns(3)
col1.metric("Hotels evaluated", total_hotels)
col2.metric("Average confidence", f"{mean_confidence}%")
col3.metric("Needing human review", f"{human_review_share}%")

risk_counts = df["risk_level"].value_counts().reindex(risk_order, fill_value=0)

left, right = st.columns([1.2, 1.8])
with left:
    st.subheader("Risk distribution")
    st.bar_chart(risk_counts)

with right:
    st.subheader("Quality snapshot")
    st.markdown(
        f"- Low-risk content: **{risk_counts.get('LOW', 0)}**\n"
        f"- Medium-risk content: **{risk_counts.get('MEDIUM', 0)}**\n"
        f"- High-risk content: **{risk_counts.get('HIGH', 0)}**\n"
        f"- Average confidence score: **{mean_confidence}%**\n"
        f"- Human review share: **{human_review_share}%**"
    )

issue_counts = {}
for claims in df["unsupported_claims"].dropna():
    for claim in str(claims).split(" | "):
        claim = claim.strip()
        if claim:
            issue_counts[claim] = issue_counts.get(claim, 0) + 1

issue_df = pd.DataFrame(
    [{"Issue": key, "Count": value} for key, value in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)]
).head(10)

st.subheader("Most common issue types")
if not issue_df.empty:
    st.bar_chart(issue_df.set_index("Issue")["Count"])
else:
    st.info("No unsupported claims detected in the current evaluation data.")

st.subheader("Flagged hotels")
flagged = df[
    ["hotel_name", "risk_level", "unsupported_claim_count", "human_review_required", "confidence"]
].sort_values(["risk_level", "unsupported_claim_count"], ascending=[True, False])

st.dataframe(flagged, use_container_width=True, hide_index=True)

st.caption("This view is designed to support product and content decision-making: identify risky AI-generated copy early and decide whether it needs approval or revision.")
