"""
GroundLens -- multi-sector decision board.

Run with:
    streamlit run app.py

The person using this picks WHAT KIND of decision they're making
(community resources, a business bet, a public project, a personal
choice). The same scoring engine reconfigures itself around that choice
-- different data, different factors, different framing -- which is the
whole "one platform, many decisions" pitch, shown live instead of told.
"""

import streamlit as st
import pandas as pd
import altair as alt

from decision_engine import load_data, score_options, explain
from sectors import SECTORS

st.set_page_config(page_title="GroundLens Decision Board", layout="wide")

if "sector_key" not in st.session_state:
    st.session_state.sector_key = None


def go_to(key):
    st.session_state.sector_key = key


# ---------------------------------------------------------------------
# SCREEN 1 -- sector picker
# ---------------------------------------------------------------------
if st.session_state.sector_key is None:
    st.title("GroundLens")
    st.caption("One decision engine. Point it at whatever you're deciding.")
    st.write("")
    st.subheader("What kind of decision are you making?")
    st.write("")

    sector_items = list(SECTORS.items())
    for row_start in range(0, len(sector_items), 2):
        row_items = sector_items[row_start:row_start + 2]
        cols = st.columns(2)
        for col, (key, sector) in zip(cols, row_items):
            with col:
                with st.container(border=True):
                    st.markdown(f"### {sector['icon']} {sector['label']}")
                    st.write(sector["tagline"])
                    st.caption(sector["user_line"])
                    st.button("Choose this", key=f"btn_{key}", on_click=go_to, args=(key,), use_container_width=True)
        st.write("")

    st.write("")
    st.info(
        "This is the same idea whether you're an NGO, a founder, a government "
        "office, or a person facing a hard choice: turn the real factors into a "
        "transparent, adjustable priority ranking instead of a guess."
    )

# ---------------------------------------------------------------------
# SCREEN 2 -- live dashboard for the chosen sector
# ---------------------------------------------------------------------
else:
    sector = SECTORS[st.session_state.sector_key]

    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.title(f"{sector['icon']} {sector['label']}")
        st.caption(sector["tagline"])
    with top_right:
        st.write("")
        st.button("Change sector", on_click=go_to, args=(None,))

    df = load_data(sector["data_path"])

    st.sidebar.header("Set your priorities")
    st.sidebar.caption("Drag to change what matters most. The ranking updates live.")
    weights = {}
    for key, spec in sector["factors"].items():
        weights[key] = st.sidebar.slider(
            spec["label"], 0, 100, spec["default_weight"], help=spec["help"]
        )

    ranked, used_weights = score_options(df, sector["factors"], weights)
    name_col = sector["name_col"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Priority ranking")
        chart = (
            alt.Chart(ranked)
            .mark_bar()
            .encode(
                x=alt.X("priority_score:Q", title="Priority score"),
                y=alt.Y(f"{name_col}:N", sort="-x", title=None),
                color=alt.Color("priority_score:Q", legend=None, scale=alt.Scale(scheme="tealblues")),
                tooltip=[name_col, "priority_score"],
            )
            .properties(height=420)
        )
        st.altair_chart(chart, use_container_width=True)

    with col2:
        st.subheader("Why the top pick ranked #1")
        top_name = ranked.iloc[0][name_col]
        st.markdown(f"**{top_name}**")
        explanation = explain(ranked, used_weights, sector["factors"], name_col, top_name)
        st.text("\n".join(explanation.split("\n")[2:]))

    st.divider()
    st.subheader("Full ranked table")
    display_cols = [name_col, "priority_score"]
    st.dataframe(ranked[display_cols], use_container_width=True, hide_index=True)

    st.caption(
        "Priority score = weighted sum of normalized factors (0-100 scale) -- "
        "multi-criteria decision analysis (MCDA), the same approach used in real "
        "resource-allocation and policy planning. Change sector above to see the "
        "same engine run on a completely different kind of decision."
    )
