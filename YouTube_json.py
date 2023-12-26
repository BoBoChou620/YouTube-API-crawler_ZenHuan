import requests
import json
import csv
import os

def get_comments(video_id, api_key):
    comments = []

    # 設定請求的URL，加上maxResults參數
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100"

    while url:
        # 發送請求並取得回應
        response = requests.get(url)

        # 檢查回應的狀態碼是否為200，表示成功
        if response.status_code == 200:
            data = json.loads(response.text)
            # 取得留言資訊
            get_comment_info(data, comments)

            # 檢查是否有下一頁的留言
            if "nextPageToken" in data:
                # 取得下一頁的token
                next_page_token = data["nextPageToken"]
                # 重新設定請求的URL，加上pageToken參數
                url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&pageToken={next_page_token}"
            else:
                url = None
        else:
            print("請求失敗")
            break

    # 將留言資訊轉換為JSON格式的字串，並儲存到一個.json檔案中
    with open("theYouTubecomments-2.json", "w", encoding="utf-8") as json_file:
        json.dump(comments, json_file, ensure_ascii=False, indent=4)

    # 將留言資訊轉換為CSV格式，並儲存到一個.csv檔案中
    csv_file_path = "theYouTubecomments-2.csv"
    with open(csv_file_path, "w", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["comment", "author", "time"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comments)

    print(f"留言資訊已儲存到 {json_file.name} 和 {csv_file_path}")

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
api_key = "AIzaSyByF6bH5zI9SRTr26Pg-6PLqM8dgNn2LRA"  # 這邊以自己的API KEY
video_id = "ITuTTA1PpoA"

# 執行函數
get_comments(video_id, api_key)