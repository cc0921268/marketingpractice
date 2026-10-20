import csv
import random

reviews = [
    ("这个商品太棒了，质量很好，推荐购买！", "好评"),
    ("发货很快，包装完好，满意", "好评"),
    ("用起来不错，性价比很高", "好评"),
    ("一般般吧，没有想象那么好", "中评"),
    ("质量一般，勉强能用", "中评"),
    ("不太满意，有点小瑕疵", "差评"),
    ("物流太慢了，等了好久", "差评"),
    ("物超所值，下次还来", "好评"),
    ("手感不错，值得入手", "好评"),
    ("不推荐，和图片差距大", "差评"),
    ("还行，中规中矩", "中评"),
    ("非常好用，已经安利朋友了", "好评"),
    ("做工粗糙，不太喜欢", "差评"),
    ("配送快，客服态度好", "好评"),
    ("价格合适，品质普通", "中评")
]

with open("sim_reviews.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["content", "score_type"])
    for _ in range(300):
        text, label = random.choice(reviews)
        w.writerow([text, label])

print("✅ 模拟评论文件 sim_reviews.csv 生成完成！")