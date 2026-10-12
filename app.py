from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Spotify Hit Intelligence", page_icon="🎵", layout="wide")
st.markdown("""<style>
.stApp {background-color:#111714;color:#F4F7F4}
[data-testid="stMetric"] {background:#202B24;padding:16px;border-radius:12px}
h1,h2,h3 {color:#EAF8EF}
</style>""", unsafe_allow_html=True)

REQUIRED = {"song", "artist", "year", "popularity", "danceability", "energy"}
OPTIONAL = {"valence", "tempo", "genre", "duration_ms"}

@st.cache_data
def read_csv(path_or_file):
    return pd.read_csv(path_or_file)

st.title("🎵 Spotify Hit Intelligence")
st.caption("A decision-support dashboard for music promotion managers | Historical dataset, not a hit predictor")

local_file = Path(__file__).parent / "data" / "songs_normalize.csv"
upload = st.sidebar.file_uploader("Upload Spotify CSV", type="csv")
if upload is not None:
    df = read_csv(upload)
elif local_file.exists():
    df = read_csv(local_file)
else:
    st.info("Upload songs_normalize.csv in the sidebar, or place it in data/songs_normalize.csv to start.")
    st.stop()

df.columns = df.columns.str.strip().str.lower()
missing = REQUIRED - set(df.columns)
if missing:
    st.error(f"CSV missing columns: {', '.join(sorted(missing))}. Check the Kaggle dataset format.")
    st.stop()

for column in ["year", "popularity", "danceability", "energy", "valence", "tempo"]:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
df = df.dropna(subset=list(REQUIRED)).copy()
df = df[df["popularity"].between(0,100) & df["danceability"].between(0,1) & df["energy"].between(0,1)]
if df.empty:
    st.warning("No valid rows found.")
    st.stop()
df["year"] = df["year"].astype(int)

st.sidebar.header("Filters")
years = sorted(df["year"].unique().tolist())
year_range = st.sidebar.slider("Release year", min_value=min(years), max_value=max(years), value=(min(years), max(years)))
artist_options = sorted(df["artist"].astype(str).unique().tolist())
selected_artists = st.sidebar.multiselect("Artists (optional)", artist_options)
filtered = df[df["year"].between(*year_range)].copy()
if selected_artists:
    filtered = filtered[filtered["artist"].astype(str).isin(selected_artists)]

if filtered.empty:
    st.warning("No songs match these filters. Try widening your selection.")
    st.stop()

st.subheader("Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Average popularity", f"{filtered['popularity'].mean():.1f}/100")
col2.metric("High-popularity share (≥70)", f"{(filtered['popularity'] >= 70).mean():.1%}")
col3.metric("Tracks analyzed", f"{len(filtered):,}")

left, right = st.columns(2)
with left:
    fig = px.scatter(filtered, x="energy", y="popularity", color="danceability",
                     hover_data=["song", "artist", "year"],
                     labels={"energy":"Energy", "popularity":"Popularity score", "danceability":"Danceability"},
                     title="How does energy relate to popularity?", color_continuous_scale="Greens")
    fig.update_layout(template="plotly_dark", paper_bgcolor="#111714", plot_bgcolor="#111714")
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_year = filtered.groupby("year", as_index=False).agg(mean_popularity=("popularity", "mean"), track_count=("song", "size"))
    fig2 = px.line(by_year, x="year", y="mean_popularity", markers=True,
                   labels={"year":"Release year", "mean_popularity":"Average popularity"},
                   title="Average popularity by release year")
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#111714", plot_bgcolor="#111714")
    st.plotly_chart(fig2, use_container_width=True)
st.caption("Interpretation caution: this historical dataset may overrepresent successful songs. Correlation does not show causation; popularity may change over time.")

st.subheader("Song Explorer & Promotion Review")
st.write("Filter for attributes that fit a proposed campaign, then review the matching tracks. A shortlist is **not** a prediction of commercial success.")
a, b, c = st.columns(3)
with a:
    min_pop = st.slider("Minimum popularity", 0, 100, 70)
with b:
    min_energy = st.slider("Minimum energy", 0.0, 1.0, 0.6, step=0.05)
with c:
    min_dance = st.slider("Minimum danceability", 0.0, 1.0, 0.6, step=0.05)
shortlist = filtered[(filtered["popularity"] >= min_pop) & (filtered["energy"] >= min_energy) & (filtered["danceability"] >= min_dance)].copy()
shortlist = shortlist.sort_values("popularity", ascending=False)
cols = [c for c in ["song", "artist", "year", "popularity", "energy", "danceability", "valence", "tempo"] if c in shortlist.columns]
st.write(f"**{len(shortlist)}** tracks match your review criteria.")
st.dataframe(shortlist[cols], use_container_width=True, hide_index=True)
st.download_button("Download review shortlist (CSV)", shortlist[cols].to_csv(index=False).encode("utf-8"), file_name="promotion_review_shortlist.csv", mime="text/csv")

with st.expander("Data, refresh, and caveats"):
    st.write("Source: Kaggle Spotify songs_normalize.csv. Confirm the exact creator, date, source and licensing on the selected Kaggle page before submission.")
    st.write("Current refresh: static historical CSV snapshot; it does not update automatically. Proposed operational refresh: weekly, if an authorized current data feed becomes available.")
    st.write("Excluded from the primary dashboard: song duration and loudness; neither is required for the selected weekly review decision. There is no live streaming, marketing spend, or conversion data here.")
    st.write("Potential biases: historical hit-selection bias, popularity snapshot ambiguity, missing values, and nonrepresentativeness of new releases.")
