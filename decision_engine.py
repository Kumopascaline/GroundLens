"""
GroundLens Decision Engine (sector-agnostic core)
--------------------------------------------------
A weighted multi-criteria decision analysis (MCDA) engine. Give it any
table of options and a set of factors, and it ranks those options by a
single transparent "priority score" -- with a plain-language explanation
of why each one landed where it did.

This file is deliberately generic. It doesn't know or care whether it's
ranking communities, business initiatives, government projects, or job
offers -- that domain-specific setup lives in sectors.py. This is what
makes the "pick a sector, watch the engine reconfigure" demo possible:
one scoring engine, many configs.

Direction of each factor:
- "higher_priority": a bigger raw value pushes the score UP
  (e.g. population affected, projected ROI, urgency)
- "lower_priority": a bigger raw value pushes the score DOWN
  (e.g. cost to build, competitive risk, distance)

Run it directly for a quick sanity check against the community sector:

    python decision_engine.py
"""

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def _normalize(series: pd.Series, direction: str) -> pd.Series:
    """Rescale a column to 0-100, where 100 always means 'highest priority.'"""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([50.0] * len(series), index=series.index)
    scaled = (series - lo) / (hi - lo) * 100
    if direction == "lower_priority":
        scaled = 100 - scaled
    return scaled


def score_options(df: pd.DataFrame, factors: dict, weights: dict):
    """
    df: raw data table
    factors: {factor_key: {"column": str, "direction": "higher_priority"|"lower_priority", "label": str}}
    weights: {factor_key: number} -- any positive numbers, auto-normalized to sum to 1.0

    Returns (ranked_df, normalized_weights).
    ranked_df has one `{factor}_score` column per factor, plus `priority_score` and `rank`.
    """
    total_w = sum(weights.values()) or 1.0
    norm_weights = {k: v / total_w for k, v in weights.items()}

    out = df.copy()
    priority = pd.Series([0.0] * len(df), index=df.index)

    for key, spec in factors.items():
        score_col = f"{key}_score"
        out[score_col] = _normalize(df[spec["column"]], spec["direction"])
        priority += out[score_col] * norm_weights.get(key, 0)

    out["priority_score"] = priority.round(1)
    out = out.sort_values("priority_score", ascending=False).reset_index(drop=True)
    out.insert(0, "rank", out.index + 1)
    return out, norm_weights


def explain(ranked_df: pd.DataFrame, weights: dict, factors: dict, name_col: str, name: str) -> str:
    """Plain-language breakdown of why one option ranked where it did."""
    row = ranked_df[ranked_df[name_col] == name]
    if row.empty:
        return f"'{name}' not found."
    row = row.iloc[0]

    lines = [
        f"{name} -- ranked #{int(row['rank'])} (priority score {row['priority_score']}/100)",
        "Why:",
    ]
    contributions = []
    for key, spec in factors.items():
        val = row[f"{key}_score"]
        w = weights.get(key, 0)
        contributions.append((spec.get("label", key), val, w, val * w))

    contributions.sort(key=lambda c: c[3], reverse=True)
    for label, val, w, contrib in contributions:
        lines.append(f"  - {label}: {val:.0f}/100 x {w*100:.0f}% weight = {contrib:.1f} points")
    return "\n".join(lines)


def rank_from_sector(sector: dict, weights: dict = None):
    """Convenience wrapper driven entirely by a sector config (see sectors.py)."""
    df = load_data(sector["data_path"])
    weights = weights or {k: v["default_weight"] for k, v in sector["factors"].items()}
    return score_options(df, sector["factors"], weights)


if __name__ == "__main__":
    from sectors import SECTORS

    sector = SECTORS["community"]
    ranked, weights = rank_from_sector(sector)

    print("=" * 60)
    print(f"GROUNDLENS -- {sector['label'].upper()}")
    print("=" * 60)
    cols = [sector["name_col"], "priority_score"]
    print(ranked[["rank"] + cols].to_string(index=False))

    print("\n" + "=" * 60)
    print("EXPLAINABILITY -- top result")
    print("=" * 60)
    top_name = ranked.iloc[0][sector["name_col"]]
    print(explain(ranked, weights, sector["factors"], sector["name_col"], top_name))

    print("\nTry: from sectors import SECTORS; pick a different key")
    print("('business', 'government', 'career') and re-run to see the")
    print("same engine reconfigure for a completely different decision.")
