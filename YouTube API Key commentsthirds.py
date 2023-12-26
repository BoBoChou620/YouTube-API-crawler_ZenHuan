import requests
import json

# 設定在Goolge Cloud申請的API金鑰和YouTube影片ID
# 這邊用甄嬛傳第63集滴血驗親來當示範，影片ID記得點選右鍵影片資訊就可以看到

api_key = "AIzaSyByF6bH5zI9SRTr26Pg-6PLqM8dgNn2LRA" # 這邊以自己的API KEY
video_id = "ITuTTA1PpoA"

# 設定請求的URL
url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}"

# 發送請求並取得回應
response = requests.get(url)

# 檢查回應的狀態碼是否為200，表示成功
if response.status_code == 200:
    print("請求成功")
else:
    print("請求失敗")
    # 解析回應的JSON格式的資料
    data = json.loads(response.text)
    # 準備一個空的列表，用來儲存留言資訊
    comments = []
    # 定義一個函數，用來遞迴地取得留言資訊
    def get_comments(data):
    # 取得留言討論串的列表
        items = data["items"]
    # 遍歷每個留言討論串
        for item in items:
        # 取得留言的內容
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        # 取得留言的作者
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        # 取得留言的時間
            time = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        # 將留言的資訊以字典的形式儲存到列表中
            comments.append({"comment": comment, "author": author, "time": time})
        # 檢查是否有回覆的留言
        if item["snippet"]["totalReplyCount"] > 0:
            # 取得回覆的留言列表
            replies = item["replies"]["comments"]
            # 遍歷每個回覆的留言
            for reply in replies:
                # 取得回覆的內容
                comment = reply["snippet"]["textDisplay"]
                # 取得回覆的作者
                author = reply["snippet"]["authorDisplayName"]
                # 取得回覆的時間
                time = reply["snippet"]["publishedAt"]
                # 將回覆的資訊以字典的形式儲存到列表中
                comments.append({"comment": comment, "author": author, "time": time})
    # 檢查是否有下一頁的留言
        if "nextPageToken" in data:
        # 取得下一頁的token
            next_page_token = data["nextPageToken"]
        # 重新設定請求的URL，加上pageToken參數
            url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&pageToken={next_page_token}"
        # 發送請求並取得回應
            response = requests.get(url)
        # 解析回應的JSON格式的資料
            data = json.loads(response.text)
        # 遞迴地取得下一頁的留言資訊
            get_comments(data)
    # 將留言資訊轉換為JSON格式的字串，並儲存到一個.json檔案中
    with open("theYouTubecomments.json", "w", encoding="utf-8") as file:
            json.dump(comments, file, ensure_ascii=False, indent=4)

    

