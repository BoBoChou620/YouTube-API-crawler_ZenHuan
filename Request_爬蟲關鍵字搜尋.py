import requests
import pandas as pd

url=input("請輸入欲搜尋的網址：")
response=requests.get(url)

if response.status_code == requests.codes.ok:
    print("取得網頁內容成功")
    
    # 使用splitlines()將字串做成list
    data =response.text.splitlines()
    total= 0
    #設置關鍵字
    keyword=input("請輸入要搜尋的關鍵字：")
    for row in data:
        if keyword in row: #將Keyword在list一行一行找
          total+=row.count(keyword)
    print("「%s」在網頁中找到的資料筆數總共為 %d 筆資料"%(keyword,total))
else:
    print("取得網頁內容失效")    