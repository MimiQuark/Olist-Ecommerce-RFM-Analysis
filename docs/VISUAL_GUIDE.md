# 项目可视化与可解释性指南

本页用思维导图、数据流、指标口径、RFM 决策逻辑、业务结论图和现有分析图表解释 PySpark 电商项目。

## 图 1：项目能力思维导图

```mermaid
flowchart TD
    ROOT((Olist 电商分析))
    ROOT --> DATA[六表数据]
    ROOT --> SPARK[PySpark 链路]
    ROOT --> METRIC[指标口径]
    ROOT --> RFM[RFM 分层]
    ROOT --> INSIGHT[业务结论]

    DATA --> D1[订单]
    DATA --> D2[商品]
    DATA --> D3[客户]
    DATA --> D4[支付]
    DATA --> D5[品类翻译]

    SPARK --> S1[清洗与类型转换]
    SPARK --> S2[数据关联]
    SPARK --> S3[窗口函数]
    SPARK --> S4[CSV 输出]

    METRIC --> M1[区域 GMV]
    METRIC --> M2[月度趋势]
    METRIC --> M3[品类排名]
    METRIC --> M4[客单价]

    RFM --> R1[Recency]
    RFM --> R2[Frequency]
    RFM --> R3[Monetary]
    RFM --> R4[客户分层]

    INSIGHT --> I1[三州营收集中]
    INSIGHT --> I2[黑五峰值]
    INSIGHT --> I3[复购率约 3.0%]
```

## 图 2：六表关联与双层宽表

```mermaid
flowchart LR
    ORD[订单表] --> JOIN[六表关联]
    ITEM[订单商品表] --> JOIN
    PROD[商品表] --> JOIN
    CUST[客户表] --> JOIN
    PAY[支付表] --> JOIN
    CAT[品类翻译表] --> JOIN

    JOIN --> ORDER[订单级宽表]
    JOIN --> ITEMROW[商品行级宽表]
    ORDER --> REGION[区域分析]
    ORDER --> MONTH[月度趋势]
    ORDER --> RFM[RFM]
    ITEMROW --> CATEGORY[品类 GMV]
```

关键解释：区域、趋势和 RFM 以订单为粒度；品类 GMV 以商品行为粒度。两张表可以共享清洗逻辑，但不能混用金额。

## 图 3：GMV 口径决策树

```mermaid
flowchart TD
    Q[需要计算什么指标] --> Q1{订单级还是商品行级}
    Q1 -->|订单级| ORDER[聚合每个订单的支付金额]
    Q1 -->|商品行级| ROW[price + freight_value]
    ORDER --> REGION[区域 GMV / 月度趋势 / RFM]
    ROW --> CATEGORY[品类 GMV / 件均价]
    REGION --> CHECK1[避免多商品订单重复累加]
    CATEGORY --> CHECK2[保留商品明细口径]
```

## 图 4：RFM 打分与分层逻辑

```mermaid
flowchart TD
    CUSTOMER[customer_unique_id] --> R[最近一次购买 recency]
    CUSTOMER --> F[购买频次 frequency]
    CUSTOMER --> M[累计消费 monetary]

    R --> RN[ntile 4 分]
    M --> MN[ntile 4 分]
    F --> FT{frequency}
    FT -->|≥4| F4[4 分]
    FT -->|≥3| F3[3 分]
    FT -->|≥2| F2[2 分]
    FT -->|1| F1[1 分]

    RN --> SCORE[R + F + M]
    F4 --> SCORE
    F3 --> SCORE
    F2 --> SCORE
    F1 --> SCORE
    MN --> SCORE
    SCORE --> SEG[高价值 / 重要 / 一般 / 低价值]
```

Frequency 不能直接 `ntile` 的原因是大量客户同为 1 次购买，强制分箱会把相同行为随机拆开。

## 图 5：业务结论与证据地图

```mermaid
flowchart LR
    ROOT((分析结论))
    ROOT --> C1[区域集中]
    ROOT --> C2[品类集中]
    ROOT --> C3[增长趋势]
    ROOT --> C4[复购偏低]

    C1 --> E1[SP 约 585 万 BRL，约 4.1 万单]
    C2 --> E2[health_beauty 约 144 万 BRL]
    C3 --> E3[2017-11 单月约 116.7 万 BRL]
    C4 --> E4[复购率约 3.0% / 高价值客户约 603 人]

    C1 --> A1[物流与营销优先资源]
    C2 --> A2[品类结构和客单价分析]
    C3 --> A3[检查促销与大促节奏]
    C4 --> A4[区分一次性品类和留存策略]
```

## 既有分析图表

### 区域 GMV Top 10

![各州 GMV](../output/charts/01_state_sales.png)

解释：识别营收集中在哪些州，以及平均客单价和订单规模是否存在区域差异。

### 月度趋势

![月度趋势](../output/charts/02_monthly_trend.png)

解释：观察大促、季节性和环比波动，重点区分真实增长和低基数噪声。

### 品类排名

![品类排名](../output/charts/03_category_ranking.png)

解释：图表展示商品行级 GMV 排名；配套 CSV 另含 `avg_item_value`（price + freight，非纯商品单价），用于识别高客单品类。

### RFM 客户分层

![RFM](../output/charts/04_rfm_segmentation.png)

解释：识别高价值、重要、一般和低价值客户的数量与消费贡献。

## 视觉阅读顺序

1. 图 1 了解项目模块。
2. 图 2 理解六表关联和双层宽表。
3. 图 3 解释 GMV 口径。
4. 图 4 说明 RFM 为什么采用混合打分。
5. 图 5 和四张图表用于解释结论、指标和行动建议。