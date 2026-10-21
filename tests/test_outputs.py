from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"


def _read(name):
    return pd.read_csv(OUT / name)


def test_state_analysis_schema_and_top_state():
    frame = _read("state_analysis.csv")
    assert {"customer_state", "total_gmv", "order_count", "avg_order_value"} <= set(frame.columns)
    assert len(frame) == 27
    assert frame.iloc[0]["customer_state"] == "SP"
    assert round(frame.iloc[0]["total_gmv"] / 10000, 1) == 584.7
    assert round(frame.head(3)["total_gmv"].sum() / frame["total_gmv"].sum() * 100, 1) == 62.5


def test_monthly_trend_has_expected_range():
    frame = _read("monthly_sales.csv")
    assert frame["order_month"].min() == "2016-09"
    assert frame["order_month"].max() == "2018-09"
    assert len(frame) == 24


def test_category_ranking_top_items():
    frame = _read("category_ranking.csv")
    assert frame.iloc[0]["product_category_name_english"] == "health_beauty"
    assert round(frame.iloc[0]["total_gmv"] / 10000, 1) == 143.6
    assert frame.iloc[1]["product_category_name_english"] == "watches_gifts"


def test_rfm_segments_are_complete():
    frame = _read("rfm_segmentation.csv")
    assert frame["customer_count"].sum() == 94695
    high = frame[frame["customer_segment"].str.contains("高价值")].iloc[0]
    assert high["customer_count"] == 603
    assert round(high["avg_purchase_amount"], 2) == 435.75
