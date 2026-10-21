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
    # 连续月份骨架：2016-09..2018-09 共 25 行，缺失的 2016-11 保留为空行
    assert len(frame) == 25
    gap = frame[frame["order_month"] == "2016-11"].iloc[0]
    assert gap["order_count"] == 0
    assert pd.isna(gap["monthly_gmv"]) and pd.isna(gap["mom_growth_pct"])
    # 跨缺失月份的 2016-12 不应把 2016-10 当成上月
    dec = frame[frame["order_month"] == "2016-12"].iloc[0]
    assert pd.isna(dec["mom_growth_pct"])


def test_category_ranking_top_items():
    frame = _read("category_ranking.csv")
    assert frame.iloc[0]["product_category_name_english"] == "health_beauty"
    assert round(frame.iloc[0]["total_gmv"] / 10000, 1) == 143.6
    assert frame.iloc[1]["product_category_name_english"] == "watches_gifts"
    assert frame.iloc[2]["product_category_name_english"] == "bed_bath_table"
    assert round(frame.iloc[2]["total_gmv"] / 10000, 2) == 123.97
    # 翻译缺失的类目归入 unknown，不再产生空名称行
    assert frame["product_category_name_english"].notna().all()
    assert frame["product_category_name_english"].str.strip().ne("").all()


def test_rfm_segments_are_complete():
    frame = _read("rfm_segmentation.csv")
    assert frame["customer_count"].sum() == 94695
    assert len(frame) == 4
    high = frame[frame["customer_segment"].str.contains("高价值")].iloc[0]
    low = frame[frame["customer_segment"].str.contains("低价值")].iloc[0]
    assert high["customer_count"] == 603
    assert round(high["avg_purchase_amount"], 2) == 435.52
    assert low["customer_count"] == 18013
    assert round(low["avg_purchase_amount"], 2) == 57.23
    assert high["avg_purchase_amount"] / low["avg_purchase_amount"] > 7
