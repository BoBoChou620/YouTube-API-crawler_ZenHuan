import re
import emoji
import jieba
jieba.case_sensitive = True # 可控制對於詞彙中的英文部分是否為case sensitive, 預設False
import csv
import pandas as pd
import emoji

filename=r"C:\Users\wonde\OneDrive - 高雄師範大學\文件\GitHub\Python YouTube API 爬蟲\comment_text63.csv"

def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def remove_html_tags(data):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', data)

def remove_emoji(data):
    data = emoji.demojize(data)
    data = re.sub(r':[a-zA-Z_&]+:', '', data)
    return emoji.demojize(data)

def remove_time_marks(data):
    # 定義要移除的時間標記的正則表達式
    time_pattern = r'\d{1,2}:\d{2}'
    return re.sub(time_pattern, '', data)

# 使用上述函數來清理文本
clean_text = remove_time_marks(remove_emoji(remove_html_tags(filename)))

# 寫入新的 CSV 檔案
def write_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

# 主程式
def main():
    # 讀取原始資料檔案
    data = read_csv(filename)
    # 清理資料
    cleaned_data = []
    for row in data:
        cleaned_row = [remove_time_marks(remove_emoji(remove_html_tags(item))) for item in row]
        cleaned_data.append(cleaned_row)
    # 寫入新的 CSV 檔案
    write_csv('context63_clean.csv', cleaned_data)

if __name__ == '__main__':
    main()


# =============================================================================
# seg_list = jieba.cut(clean_text, cut_all=False)
# print(" ".join(seg_list))
# 
# # 假設 seg_list 是一個包含所有詞語的列表
# df = pd.DataFrame(seg_list, columns=['Word'])
# =============================================================================
