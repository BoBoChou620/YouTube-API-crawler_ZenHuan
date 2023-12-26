import csv
import re
from bs4 import BeautifulSoup
import emoji


filename=r"C:\Users\wonde\OneDrive - 高雄師範大學\文件\GitHub\Python YouTube API 爬蟲\comment_text64.csv"

# 讀取 原始 資料CSV 檔案
def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# 移除 HTML 語法、超連結和 emoji
def clean_data(data):
    cleaned_data = []
    for row in data:
        # 使用列表生成式來簡化程式碼
        cleaned_row = [clean_item(item) for item in row]
        cleaned_data.append(cleaned_row)
    return cleaned_data

# 移除一個項目中的 HTML 語法、超連結、emoji 和時間標記
def clean_item(item):
    # 移除 HTML 語法
    soup = BeautifulSoup(item, 'html.parser')
    text = soup.get_text()
    # 移除超連結
    text = re.sub(r'http\S+|www.\S+', '', text)
    # 移除 emoji
    text = emoji.demojize(text)
    text = re.sub(r':[a-zA-Z_&]+:', '', text)
    # 移除時間標記
    text = re.sub(r'\d{1,2}:\d{2}', '', text)
    return text

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
    cleaned_data = clean_data(data)
    # 寫入新的 CSV 檔案
    write_csv('context64_clean.csv', cleaned_data)

if __name__ == '__main__':
    main()
