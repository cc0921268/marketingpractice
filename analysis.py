import pandas as pd
import jieba
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from wordcloud import WordCloud

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("sim_reviews.csv", encoding="utf-8-sig")
print("数据预览：")
print(df.head())

# 统计好评中评差评
count = df["score_type"].value_counts()
print("\n评论分类统计：")
print(count)

# 画饼图
plt.figure(figsize=(6,6))
plt.pie(count.values, labels=count.index, autopct="%.1f%%")
plt.title("好评/中评/差评占比")
plt.savefig("pie.png", dpi=300)
plt.close()

# 合并所有文本，分词
all_text = " ".join(df["content"].tolist())
words = jieba.lcut(all_text)
stopwords = {"的", "了", "很", "比较", "这", "这个", "就是", "还", "也"}
clean_words = [w for w in words if len(w)>=2 and w not in stopwords]
text_cut = " ".join(clean_words)

# 生成词云
wc = WordCloud(font_path="C:/Windows/Fonts/simhei.ttf", width=800, height=600, background_color="white")
wc.generate(text_cut)
wc.to_file("wordcloud.png")

print("\n✅ 分析完成！已生成 pie.png（饼图） 和 wordcloud.png（词云）")