from __future__ import print_function, unicode_literals
import sys
import pandas as pd
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 設定 Jieba 相關參數
jieba.case_sensitive = True
jieba.load_userdict("dict.txt")

# 讀取清理過後的文字資料.csv檔案
file_path1 = r"C:\Users\wonde\OneDrive - 高雄師範大學\文件\GitHub\Python YouTube API 爬蟲\context63_clean.csv"
file_path2 = r"C:\Users\wonde\OneDrive - 高雄師範大學\文件\GitHub\Python YouTube API 爬蟲\context64_clean.csv"
df1 = pd.read_csv(file_path1, encoding='utf-8')
df2 = pd.read_csv(file_path2, encoding='utf-8')
merged_df = pd.concat([df1, df2], ignore_index=True)


# 創建一個包含 NaN 值的 DataFrame
data = {'comment_text': [ pd.NA]}
df = pd.DataFrame(merged_df)

# 處理缺失值，將 NaN 替換為空字符串
df['comment_text'] = df['comment_text'].fillna('')

# 斷詞並統計詞頻
def cut_text(text):
    words = jieba.cut(text)
    return " ".join(words)

df["cut_text"] = df["comment_text"].apply(cut_text)
all_words = " ".join(df["cut_text"])
word_count = Counter(all_words.split())

# 製作詞頻統計長條圖
top_words = word_count.most_common(20)
top_words_df = pd.DataFrame(top_words, columns=["詞彙", "詞頻"])

# 繪製長條圖
plt.figure(figsize=(12, 6))
plt.bar(top_words_df["詞彙"], top_words_df["詞頻"])
plt.title("詞頻統計長條圖")
plt.xlabel("詞彙")
plt.ylabel("詞頻")
plt.xticks(rotation=45, ha="right")  # 避免詞彙過多時文字重疊
plt.tight_layout()

# 顯示圖片
plt.show()

# 儲存圖片
plt.savefig("Char-詞頻分析長條圖.png")

# 顯示圖片
plt.show()

# 關閉圖片
plt.close()


# # 生成文字雲
# wordcloud = WordCloud(font_path="Noto Sans TC.ttf", background_color="BlacK", width=800, height=400).generate(all_words)
# plt.figure(figsize=(12, 6))
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.title("繁體中文文字雲")
# plt.savefig("文字雲.png")
# plt.show()
# plt.close()
# # ==========================================================================================================================================================
