import requests
import json
import csv
import os

def get_comments(video_id, api_key):
    comments = []
    max_results = 100  # 一次請求最多取得的留言數量
    total_comments = 0

    # 設定請求的URL，加上maxResults參數
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults={max_results}"

    while url and total_comments < 2504:
        # 發送請求並取得回應
        response = requests.get(url)

        # 檢查回應的狀態碼是否為200，表示成功
        if response.status_code == 200:
            data = json.loads(response.text)
            # 取得留言資訊
            get_comment_info(data, comments)

            # 更新已經爬取的留言數量
            total_comments += len(comments)

            # 檢查是否有下一頁的留言
            if "nextPageToken" in data and total_comments < 2504:
                # 取得下一頁的token
                next_page_token = data["nextPageToken"]
                # 重新設定請求的URL，加上pageToken參數
                url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&pageToken={next_page_token}&maxResults={max_results}"
            else:
                url = None
        else:
            print("請求失敗")
            break

    # 將留言資訊轉換為CSV格式，並儲存到一個.csv檔案中
    csv_file_path = "comment_text63.csv"
    with open(csv_file_path, "w", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["comment_text"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for comment_info in comments:
            writer.writerow({"comment_text": comment_info["comment"]})

    print(f"留言資訊已儲存到 {csv_file_path}")

def get_comment_info(data, comments):
    items = data.get("items", [])

    for item in items:
        snippet = item.get("snippet", {})
        topLevelComment = snippet.get("topLevelComment", {})
        comment_info = {
            "comment": topLevelComment.get("snippet", {}).get("textDisplay", ""),
            "author": topLevelComment.get("snippet", {}).get("authorDisplayName", ""),
            "time": topLevelComment.get("snippet", {}).get("publishedAt", ""),
        }
        comments.append(comment_info)

        total_reply_count = snippet.get("totalReplyCount", 0)
        if total_reply_count > 0:
            replies = item.get("replies", {}).get("comments", [])
            for reply in replies:
                reply_info = {
                    "comment": reply.get("snippet", {}).get("textDisplay", ""),
                    "author": reply.get("snippet", {}).get("authorDisplayName", ""),
                    "time": reply.get("snippet", {}).get("publishedAt", ""),
                }
                comments.append(reply_info)

# 設定在Google Cloud申請的API金鑰和YouTube影片ID
api_key = "YouTube_API_KEY"  # 這邊以自己的API KEY
video_id = "ITuTTA1PpoA" #甄嬛傳第63及影片ID

# 執行函數
get_comments(video_id, api_key)

