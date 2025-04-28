import datetime
import holidays
import pytz
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.messaging.models import TextMessage, PushMessageRequest
import os

# 環境変数からアクセストークン・グループID取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
GROUP_ID = os.environ["GROUP_ID"]

# 日本の祝日設定
jp_holidays = holidays.Japan()

# 除外する特別休暇日リスト
excluded_dates = {
    datetime.date(2025, 12, 30),
    datetime.date(2025, 12, 31),
    datetime.date(2026, 1, 2),
    datetime.date(2026, 1, 3),
    datetime.date(2026, 1, 4)
}

def is_business_day():
    # 日本時間の現在日時を取得
    now_japan = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    today = now_japan.date()
    # 平日かつ祝日・特別休暇ではないか判定
    return today.weekday() < 5 and today not in jp_holidays and today not in excluded_dates

if is_business_day():
    print("📤 朝メッセージ送信")
    configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=GROUP_ID,
                messages=[TextMessage(
                    text=(
                        "[勤怠自動投稿]\n"
                        "おはようございます！皆様お元気でしょうか！？\n"
                        "本日も1日、for your Success!! で宜しくお願いします！\n"
                        "出勤の打刻、以下から宜しくお願いします！！\n"
                        "https://ssl.jobcan.jp/login/mb-employee?client_id=GFAM20040121&lang_code=ja"
                    )
                )]
            )
        )
else:
    print("⛔ 朝：非営業日のため送信なし")
