# -*- coding: utf-8 -*-
"""
营销数据生成脚本（脏数据版）
目标：
  1) 生成蓝牙降噪耳机竞品分析的原始营销数据
  2) 每个品牌约100条记录，总量约300-500条
  3) 生成过程中故意注入脏数据：
     - 缺失值
     - 重复值
     - 格式不一致
     - 品牌名不一致
     - 日期格式不一致
     - 异常值
     - 数据类型混乱

输出：
  data/raw/raw_data.csv
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# 1. 固定随机种子，保证脚本每次生成的数据可复现
random.seed(42)
np.random.seed(42)

# 2. 定义输出目录
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_data.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# 3. 品牌设定（至少4个品牌）
#    这里设置了4个虚拟品牌（或品牌的不同命名形式），并故意保留品牌名不一致情况
brand_aliases = {
    "Sony": ["Sony", "索尼", "so-ny", "索v", "SONY", "索尼耳机"],
    "Bose": ["Bose", "博士", "bo-se", "Bose Audio", "Bose音响", "bo-se耳机"],
    "Apple": ["Apple", "苹果", "apple", "Appl e", "APPle", "苹果耳机"],
    "小米": ["小米", "Xiaomi", "xiaomi", "小米科技", "小米耳机", "小米音响"]
}

# 4. 每个品牌对应的产品名称，模拟真实竞品
#    让数据看起来更加像真实营销数据，而不是完全随机
brand_products = {
    "Sony": [
        "Sony WH-1000XM5",
        "Sony WH-1000XM4",
        "Sony WF-C500",
        "Sony LinkBuds S",
        "Sony WF-1000XM5",
        "Sony ULT WEAR",
    ],
    "Bose": [
        "Bose QuietComfort Ultra",
        "Bose QuietComfort Earbuds",
        "Bose Noise Cancelling Headphones 700",
        "Bose Sport Earbuds",
        "Bose QuietComfort 45",
        "Bose Ultra Open Earbuds",
    ],
    "Apple": [
        "Apple AirPods Max",
        "Apple AirPods Pro 2",
        "Apple AirPods Pro",
        "Apple AirPods 4",
        "Apple AirPods Max 2025",
        "Apple AirPods Max Titanium",
    ],
    "小米": [
        "小米 Buds 5 Pro",
        "小米 Buds 4 Lite",
        "小米 Redmi Buds 6",
        "小米 Buds 5",
        "小米 Air2 SE",
        "小米 Buds 4 Pro",
    ],
}


# 5. 评论模板：真实营销/用户评论的口吻，带一点噪声
comment_templates = [
    "降噪很强，工作和通勤时很舒服，音质也不错，续航也还行。",
    "外观设计很高级，佩戴很轻松，不过有些时候低频不够震撼。",
    "声音很清楚，适合听歌和播客，耳机包很舒服。",
    "最喜欢的是降噪效果，长时间佩戴不会胀耳，推荐给学生党。",
    "音质一般，偶尔有点闷，适合日常通勤使用，不是发烧友级别。",
    "整体体验还不错，充电很快，手感也很舒适，性价比不错。",
    "通话清晰，降噪强，音乐细节表现不错，但价格偏高。",
    "佩戴比较稳，不容易掉，音场不错，适合跑步和出门。",
    "耳机不错，但是软件连接偶尔卡顿，音量略大一点。",
    "耳机外观很有辨识度，续航满足日常需求，说明书有点简单。",
    "音质细节比较丰富，尤其是人声和钢琴，性价比还可以。",
    "降噪有提升，但在风声比较大时还会有一点漏音。",
    "整体很轻，拿在手上很舒服，适合长时间办公使用。",
    "声音很饱满，音乐层次感不错，不过包装有点普通。",
    "耳机很安静，适合睡前听音乐，通话效果也不错。",
    "佩戴舒适，但手机连接有时不稳定，偶尔需要重连。",
    "用了几天，降噪很明显，噪音明显减少，耳塞也很稳。",
    "音色挺均衡，听流行歌很舒服，低频有一点点强但不讨厌。",
    "界面上手简单，功能很多，店家服务还可以。",
    "有点偏商务风格，适合办公和会议，但不是最强运动耳机。",
]


# 6. 日期随机生成器：故意混合多种日期格式
def random_date_string():
    """
    随机生成日期字符串，包含：
      - YYYY-MM-DD
      - MM/DD/YYYY
      - YYYY年M月D日
      - DD/MM/YYYY
      - YYYY/MM/DD
    """
    start = datetime(2025, 1, 1)
    end = datetime(2026, 12, 31)
    delta_days = (end - start).days
    random_days = random.randint(0, delta_days)
    d = start + timedelta(days=random_days)

    fmt = random.choice([
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%Y年%m月%d日",
        "%d/%m/%Y",
        "%Y/%m/%d",
    ])
    return d.strftime(fmt)


# 7. 价格格式化：故意制造格式不一致、负数和中文混杂
def weird_price_string(price_value):
    """
    将数值价格转换成脏数据字符串，例如：
      - 299.00
      - 299元
      - ￥299
      - 299元左右
      - 约299元
      - -299
      - 299.00元
      - 1,234
    """
    # 让一部分价格变成负数，构成异常值
    if random.random() < 0.08:
        price_value = -abs(price_value)

    options = [
        f"{price_value:.2f}",
        f"￥{price_value:.0f}",
        f"¥{price_value:.0f}",
        f"{price_value:.0f}元",
        f"{price_value:.2f}元左右",
        f"约{price_value:.0f}元",
        f"{price_value:.2f}元",
        f"￥{price_value:.2f}",
        f"{price_value:,.2f}",
        str(price_value),
        f"{price_value:.0f}元左右",
    ]
    return random.choice(options)


# 8. 评分处理：故意制造超出正常范围的评分和字符串类型
def weird_rating_value(base_rating):
    """
    评分应该是 1~5，但这里故意制造：
      - 70
      - 0
      - 6
      - '4.8分'
      - '五分'
      - 字符串 '4.5'
    """
    # 让一部分评分变成异常值
    anomalies = [70, 0, 6, 9, 11]
    if random.random() < 0.18:
        return random.choice(anomalies)

    # 其余可能是正常值，但仍有一些字符串化、浮点化
    variants = [
        base_rating,
        round(base_rating + random.uniform(-0.5, 0.5), 1),
        f"{base_rating}分",
        f"{base_rating}.0",
        "五分",
        f"{round(base_rating + random.uniform(-0.4, 0.4), 1)}分",
    ]
    return random.choice(variants)


# 9. 互动量处理：数字字段夹杂中文字符、千分位、文本
def weird_interaction_count(value):
    """
    互动量常见情况：
      - 1234
      - 1,234
      - 1234次
      - 一二三
      - 'N/A'
      - NaN
    """
    if random.random() < 0.12:
        return np.nan

    candidates = [
        str(value),
        f"{value:,}",
        f"{value}次",
        f"{value:,}次",
        "一二三",
        "1,234",
        "123",
        "N/A",
        "9999",
    ]
    return random.choice(candidates)


# 10. 生成主数据集
def generate_raw_dataset():
    records = []

    # 每个品牌大约 100 行，4 个品牌共 400 行
    # 之后还会插入重复数据和缺失值，确保数据量在 300-500 条左右
    for brand_name, products in brand_products.items():
        for _ in range(100):
            product_name = random.choice(products)
            price_raw = round(random.uniform(180, 1599), 2)

            # 构造一个看似合理，但会被随机污染的记录
            record = {
                "product_name": product_name,
                "price": weird_price_string(price_raw),
                "comment": random.choice(comment_templates),
                "rating": weird_rating_value(random.randint(1, 5)),
                "time": random_date_string(),
                "interaction_count": weird_interaction_count(random.randint(120, 8000)),
                # 品牌字段故意使用别名、大小写混用、缩写
                "brand": random.choice(brand_aliases[brand_name]),
            }
            records.append(record)

    # 11. 故意引入缺失值（NaN）
    #     让部分 price / comment / time 为空
    missing_indices = random.sample(range(len(records)), 30)
    for idx in missing_indices:
        if random.random() < 0.5:
            records[idx]["price"] = np.nan
        if random.random() < 0.7:
            records[idx]["comment"] = np.nan
        if random.random() < 0.5:
            records[idx]["time"] = np.nan

    # 12. 故意引入完全重复记录
    #     让一部分数据完全相同
    exact_dup_count = 12
    duplicate_indices = random.sample(range(len(records)), exact_dup_count)
    for idx in duplicate_indices:
        records.append(records[idx].copy())

    # 13. 故意引入“部分字段相同”的重复记录
    #     例如品牌、产品名和时间相同，但评论不同，属于“近似重复”
    partial_dup_count = 15
    for _ in range(partial_dup_count):
        base_record = random.choice(records).copy()
        dup_record = base_record.copy()
        # 保持关键字段相同，但做轻微修改
        dup_record["comment"] = base_record["comment"]
        dup_record["brand"] = base_record["brand"]
        dup_record["product_name"] = base_record["product_name"]
        dup_record["time"] = base_record["time"]
        # 让它在部分字段上保持一致
        records.append(dup_record)

    # 14. 进一步制造品牌名称不一致
    #     例如同一品牌，出现大小写、拼写错误、缩写等
    for idx in range(len(records)):
        brand_value = records[idx]["brand"]
        if not pd.isna(brand_value):
            if random.random() < 0.25:
                variations = [
                    brand_value.upper(),
                    brand_value.lower(),
                    brand_value.replace("o", "0"),
                    "索v",
                    "so-ny",
                    "SONY",
                    "apple",
                    "xiaomi",
                    "Bose",
                    "博士",
                ]
                records[idx]["brand"] = random.choice(variations)

    # 15. 进一步制造日期格式不一致和异常值
    for idx in range(len(records)):
        # 让一部分日期变成异常字符串
        if random.random() < 0.12:
            records[idx]["time"] = random.choice([
                "2026-05-01",
                "05/01/2026",
                "2026年5月1日",
                "01/05/2026",
                "2026/05/01",
                "2026-13-99",
                "N/A",
                np.nan,
            ])

    # 16. 让评分和价格出现极端值
    for idx in range(len(records)):
        if random.random() < 0.08:
            records[idx]["rating"] = random.choice([70, 99, -1, "999", "5分", "4.8分", np.nan])
        if random.random() < 0.05:
            # 价格有可能是明显异常的字符串
            records[idx]["price"] = random.choice([
                "-299",
                "￥-299",
                "99999",
                "一二三",
                "五千",
                "abc",
                np.nan,
            ])

    # 17. 让互动量出现中文和异常文本
    for idx in range(len(records)):
        if random.random() < 0.06:
            records[idx]["interaction_count"] = random.choice([
                "一二三",
                "N/A",
                "abc",
                np.nan,
                "123",
                "1234次",
                "1,234",
            ])

    # 18. 将记录转成 DataFrame
    df = pd.DataFrame(records)

    # 19. 设定字段顺序，确保明确的“原始营销数据”结构
    df = df[[
        "product_name",
        "price",
        "comment",
        "rating",
        "time",
        "interaction_count",
        "brand",
    ]]

    # 20. 去掉危险索引，确保CSV保存时最后一列有完整数据
    df = df.reset_index(drop=True)

    # 21. 写出 CSV
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"已生成原始营销数据：{len(df)} 条，保存到 {OUTPUT_FILE}")
    print("字段包含：product_name, price, comment, rating, time, interaction_count, brand")
    print("已故意注入缺失值、重复值、异常值、格式不一致、品牌名不一致和日期不一致等脏数据。")


if __name__ == "__main__":
    generate_raw_dataset()