# -*- coding: utf-8 -*-
"""
Pandas 数据清洗脚本
功能：
  1) 读取脏数据：data/raw/raw_data.csv
  2) 对脏数据进行清洗：
     - 缺失值处理
     - 去重处理
     - 价格统一
     - 品牌归一化
     - 日期统一
     - 评分规范化
     - 互动量清洗
  3) 保存清洗后的干净数据：data/processed/clean_data.csv

注意：
  - 该脚本假设原始数据文件已经由生成脚本生成并保存在 data/raw/raw_data.csv
  - 该脚本会严格清洗脏数据并删除无法修复的异常记录
"""

import os
import re
import numpy as np
import pandas as pd


# 1. 配置路径
RAW_PATH = "data/raw/raw_data.csv"
OUT_PATH = "data/processed/clean_data.csv"

# 确保输出目录存在
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)


# 2. 辅助函数：判断是否为空值
def is_missing_value(x):
    """判断一个值是否应该视为缺失值。"""
    if pd.isna(x):
        return True
    if isinstance(x, str):
        val = x.strip()
        if val == "" or val.lower() in {"nan", "none", "null", "n/a", "na"}:
            return True
    return False


# 3. 清洗品牌名称：统一成 4 个标准品牌
def clean_brand(x):
    """
    将品牌名统一为：
      - Sony
      - Bose
      - Apple
      - 小米
    处理内容：
      - 大小写混用
      - 缩写
      - 错别字
      - 中文/英文混用
      - 空值
    """
    if is_missing_value(x):
        return np.nan

    s = str(x).strip()
    if s == "":
        return np.nan

    # 去掉空格，统一小写便于匹配
    s = s.replace(" ", "").lower()

    # 统一处理常见噪声字符
    s = s.replace("-", "").replace("_", "").replace("·", "")
    s = s.replace("耳机", "").replace("音响", "").replace("科技", "")
    s = s.replace("audio", "")

    # 先做最常见的标准化
    alias_map = {
        "sony": "Sony",
        "索尼": "Sony",
        "索v": "Sony",
        "sony耳机": "Sony",
        "sony音响": "Sony",
        "bose": "Bose",
        "博士": "Bose",
        "bo-se": "Bose",
        "boseaudio": "Bose",
        "apple": "Apple",
        "苹果": "Apple",
        "appl": "Apple",
        "xiaomi": "小米",
        "小米": "小米",
        "小米耳机": "小米",
        "小米音响": "小米",
    }

    # 先精确匹配
    if s in alias_map:
        return alias_map[s]

    # 处理一些可能被大小写或间隔干扰的字符串
    if "sony" in s:
        return "Sony"
    if "bose" in s:
        return "Bose"
    if "apple" in s:
        return "Apple"
    if "xiaomi" in s or "小米" in s:
        return "小米"

    # 若仍无法识别，则视为异常品牌，保留 NaN
    return np.nan


# 4. 清洗价格：统一成 float
def clean_price(x):
    """
    价格清洗规则：
      - 清掉“元、￥、¥、中文汉字、千分位逗号”等
      - 修正负数价格：将负数转为正数
      - 价格必须是规范浮点数
      - 无法解析的值设为 NaN
    """
    if is_missing_value(x):
        return np.nan

    s = str(x).strip()
    if s == "":
        return np.nan

    # 去掉常见货币符号和单位
    s = s.replace("￥", "").replace("¥", "").replace("元", "").replace("约", "")
    s = s.replace("左右", "").replace(",", "").replace(" ", "")

    # 处理中文字符中的“元左右/大约”等
    # 尝试从文本中提取第一个合法数字（支持负号和小数）
    match = re.search(r"-?\d+(\.\d+)?", s)
    if match is None:
        return np.nan

    val = float(match.group(0))
    # 修正负数：价格不能为负，取绝对值
    val = abs(val)

    # 允许值为 0 但通常不合理，保留但后续可视需要过滤
    return round(val, 2)


# 5. 清洗评论：缺失补全、去除多余空白
def clean_comment(x):
    """
    评论字段清洗：
      - 缺失值填充为 "无评论"
      - 去除首尾空白
      - 将异常字符串转换为 "无评论"
    """
    if is_missing_value(x):
        return "无评论"

    s = str(x).strip()
    if s == "" or s.lower() in {"nan", "none", "null", "n/a", "na"}:
        return "无评论"

    return s


# 6. 清洗评分：统一到 1~5 的范围
def clean_rating(x):
    """
    评分清洗规则：
      - 允许类似：4.8、4.0、4、4.5分
      - 不允许：70、0、-1、五分、abc
      - 仅保留 1~5 的有效评分，其他设为 NaN
    """
    if is_missing_value(x):
        return np.nan

    s = str(x).strip()
    if s == "":
        return np.nan

    # 先尝试直接转 float（例如 4.5、4）
    try:
        val = float(s)
        if 1 <= val <= 5:
            return round(val, 1)
        return np.nan
    except:
        pass

    # 处理 "4.8分"、"5分"、"五分" 等文本
    # 先去掉“分”和空格
    s2 = s.replace("分", "").replace("评分", "").replace(" ", "")
    # 如果字符串中存在中文数字，但没有阿拉伯数字，则视为异常
    if re.search(r"[一二三四五六七八九十百千万亿]", s2):
        # 例如 "五分" 会在这里被判定为异常
        return np.nan

    match = re.search(r"\d+(\.\d+)?", s2)
    if match is None:
        return np.nan

    val = float(match.group(0))
    if 1 <= val <= 5:
        return round(val, 1)
    return np.nan


# 7. 清洗日期：统一为 YYYY-MM-DD
def clean_time(x):
    """
    日期清洗规则：
      - 支持格式：2026-05-01、05/01/2026、2026年5月1日、2026/05/01
      - 无法解析的日期视为 NaN
      - 统一输出为 YYYY-MM-DD
    """
    if is_missing_value(x):
        return pd.NaT

    s = str(x).strip()
    if s == "":
        return pd.NaT

    # 常见格式候选
    format_candidates = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y年%m月%d日",
        "%m-%d-%Y",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
    ]

    # 尝试按候选格式解析
    dt = pd.NaT
    for fmt in format_candidates:
        try:
            dt = pd.to_datetime(s, format=fmt)
            break
        except:
            pass

    # 若前面格式没命中，再尝试 pandas 自动推断
    if pd.isna(dt):
        try:
            dt = pd.to_datetime(s, errors="raise")
        except:
            return pd.NaT

    # 如果解析成功，统一输出 YYYY-MM-DD
    return pd.Timestamp(dt).strftime("%Y-%m-%d")


# 8. 清洗互动量：仅保留纯数字
def clean_interaction_count(x):
    """
    互动量清洗规则：
      - "1234" -> 1234
      - "1,234次" -> 1234
      - "一二三" -> NaN
      - "N/A" -> NaN
      - 非法文本 -> NaN
    """
    if is_missing_value(x):
        return np.nan

    s = str(x).strip()
    if s == "":
        return np.nan

    # 去掉空格、千分位、单位
    s = s.replace(" ", "").replace(",", "").replace("次", "").replace("互动量", "")

    # 如果含有中文数字（如“一二三”），视为异常
    if re.search(r"[一二三四五六七八九十百千万亿]", s):
        return np.nan

    # 提取数字
    match = re.search(r"\d+", s)
    if match is None:
        return np.nan

    val = int(match.group(0))
    return val


# 9. 读取原始数据
def main():
    try:
        df = pd.read_csv(RAW_PATH, encoding="utf-8-sig")
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到原始文件：{RAW_PATH}，请先生成脏数据。")

    # 统一列名，去掉空格
    df.columns = [str(col).strip() for col in df.columns]

    # 只保留需要的核心字段，若原数据中字段名称不一致，则尽量覆盖
    expected_cols = ["product_name", "price", "comment", "rating", "time", "interaction_count", "brand"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = np.nan

    # ---- 1. 缺失值处理 ----
    # 对 comment 缺失值统一补 "无评论"
    df["comment"] = df["comment"].apply(clean_comment)

    # ---- 2. 去重处理（完全重复）----
    # 去除整行完全重复
    df = df.drop_duplicates().reset_index(drop=True)

    # ---- 3. 数据清洗 ----
    df["product_name"] = df["product_name"].apply(
        lambda x: str(x).strip() if not is_missing_value(x) else np.nan
    )
    df["price"] = df["price"].apply(clean_price)
    df["comment"] = df["comment"].apply(clean_comment)
    df["rating"] = df["rating"].apply(clean_rating)
    df["time"] = df["time"].apply(clean_time)
    df["interaction_count"] = df["interaction_count"].apply(clean_interaction_count)
    df["brand"] = df["brand"].apply(clean_brand)

    # ---- 4. 删除无效记录 ----
    # product_name 为空或 brand 为空或 time 为空等，视为异常，删除
    df = df.dropna(subset=["product_name", "brand", "time"], how="any").reset_index(drop=True)

    # 价格、评分、互动量不合法的记录也要删除
    df = df.dropna(subset=["price", "rating", "interaction_count"], how="any").reset_index(drop=True)

    # ---- 5. 再次做“核心字段近似重复”去重 ----
    # 近似重复判定：产品名 + 品牌 + 时间 + 价格 + 评分
    # 这可以剔除“完全一致或核心字段近似重复”的记录
    # 以保留第一条有效记录
    df["dup_key"] = (
        df["product_name"].astype(str).str.strip()
        + "|"
        + df["brand"].astype(str).str.strip()
        + "|"
        + df["time"].astype(str)
        + "|"
        + df["price"].astype(str)
        + "|"
        + df["rating"].astype(str)
    )
    df = df.drop_duplicates(subset=["dup_key"], keep="first").reset_index(drop=True)
    df = df.drop(columns=["dup_key"])

    # ---- 6. 结果排序 ----
    # 可按时间从早到晚排序
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.sort_values(by=["time", "brand", "product_name"]).reset_index(drop=True)
    df["time"] = df["time"].dt.strftime("%Y-%m-%d")

    # ---- 7. 重新整理列顺序 ----
    df = df[["product_name", "price", "comment", "rating", "time", "interaction_count", "brand"]]

    # ---- 8. 保存清洗结果 ----
    df.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")

    print(f"清洗完成！总记录数：{len(df)}")
    print(f"已保存到：{OUT_PATH}")
    print("字段：product_name, price, comment, rating, time, interaction_count, brand")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()