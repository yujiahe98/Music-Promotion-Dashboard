# Spotify Hit Intelligence — Music Promotion Dashboard

**Live app:** https://music-promotion-dashboard-yujiah.streamlit.app/

## Purpose and audience

I built this Streamlit dashboard for **music promotion managers** who need to decide **which existing songs to review for a proposed campaign**. Rather than predicting the next hit, the app helps a manager understand patterns in a historical Spotify dataset and create a shortlist of tracks whose characteristics fit a campaign brief. The shortlist is a starting point for human review, not an automatic recommendation to spend money.

## Data and how to use the app

The app accepts an uploaded Spotify CSV (the example shown uses `songs_normalize.csv`). After uploading the file, a manager can filter the dataset by **release-year range** and, optionally, by **artist**. The overview updates for the selected data. In the **Song Explorer & Promotion Review** section, the manager can set minimum **popularity**, **energy**, and **danceability** thresholds, examine the matching tracks, and download a review shortlist as a CSV.

The shortlist table includes the song, artist, release year, popularity, energy, danceability, valence, and tempo. These fields give a reviewer both basic identification information and musical characteristics to compare. For example, a team planning an upbeat campaign might raise the energy and danceability thresholds before reviewing the remaining songs.

## What I chose to show — and why

- **Three overview metrics:** Average popularity summarizes the selected tracks; the share with popularity **70 or above** indicates how common higher-popularity tracks are; and the number of tracks analyzed gives context for both figures. I show the sample size because an impressive average is less convincing if it comes from only a few songs.
- **Energy vs. popularity scatter plot, colored by danceability:** This lets a manager see the spread of individual tracks, including exceptions, instead of assuming high energy automatically means high popularity. Color adds a second musical characteristic without needing another chart.
- **Average popularity by release year:** This shows how averages vary across years in the historical sample, helping reviewers consider whether a comparison may be affected by release period. It does not establish that release year causes popularity.
- **Release-year and artist filters:** These make comparisons more relevant to a specific period or artist instead of forcing every user to analyze all tracks at once.
- **Promotion-review thresholds and downloadable shortlist:** The dashboard leads to an actual decision-support output: a manageable list to discuss or investigate further, not just graphs to look at.

## What I deliberately left out

I did **not** add a “hit probability” prediction, a ranking of which tracks are guaranteed to succeed, or an automatic promotion-budget allocation. Historical popularity and audio features do not establish future campaign outcomes, and the dataset shown does not provide causal evidence about advertising effectiveness. I also avoided separate plots for every audio attribute: too many charts would make the central task—finding tracks worth reviewing—harder. Instead, less central fields such as valence and tempo are available in the shortlist table when someone needs them.

## Refresh frequency

This dashboard is based on a **user-uploaded historical CSV**, not a live Spotify feed. Therefore, the data should be updated **when a new, comparable export becomes available**, rather than automatically claiming that a daily or weekly refresh has occurred. For an actively managed campaign, I would check for a trustworthy updated export **weekly**, but only replace the file if the source and definitions remain consistent. Users should interpret the results as describing the uploaded snapshot, not current live trends.

## Limitations

The displayed figures depend on the uploaded file and active filters. Spotify popularity in the dataset is not the same as profit, marketing return, or future success. The scatter plot and yearly averages show associations, not causation. A manager should also consider audience fit, rights, promotion cost, and other information that this dashboard does not contain before committing to a campaign.

## Tools

Python, Streamlit, and CSV-based data exploration; deployed with Streamlit Community Cloud.
