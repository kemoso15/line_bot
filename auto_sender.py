import schedule
import time
import datetime
import holidays
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.messaging.models import TextMessage, PushMessageRequest
import os

CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
GROUP_ID = os.environ["GROUP_ID"]

# 日本の祝日＋除外したい特定日
jp_holidays = holidays.Japan()
excluded_dates = {
    datetime.date(2025, 12, 30),
    datetime.date(2025, 12, 31),
    datetime.date(2026, 1, 2),
    datetime.date(2026, 1, 3),
    datetime.date(2026, 1, 4)
}

# LINE SDK 設定
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# 平日＆祝日・除外日チェック
def is_business_day():
    today = datetime.date.today()
    return today.weekday() < 5 and today not in jp_holidays and today not in excluded_dates

# メッセージ①（朝8:30）
def send_morning_message():
    if is_business_day():
        print("📤 朝メッセージ送信")
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

# メッセージ②（夕方17:30）
def send_evening_message():
    if is_business_day():
        print("📤 夕方メッセージ送信")
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.push_message(
                PushMessageRequest(
                    to=GROUP_ID,
                    messages=[TextMessage(
                        text=(
                            "[勤怠自動投稿]\n"
                            "本日も1日お疲れ様でした！\n"
                            "退勤の打刻、忘れず宜しくお願いします！！\n"
                            "https://ssl.jobcan.jp/login/mb-employee?client_id=GFAM20040121&lang_code=ja"
                        )
                    )]
                )
            )
    else:
        print("⛔ 夕方：非営業日のため送信なし")

# 平日（曜日ごと）に送信設定
for day in [schedule.every().monday,
            schedule.every().tuesday,
            schedule.every().wednesday,
            schedule.every().thursday,
            schedule.every().friday]:
    day.at("08:30").do(send_morning_message)
    day.at("17:30").do(send_evening_message)

# 実行ループ
print("⏳ 勤怠メッセージBot 起動中...")
while True:
    schedule.run_pending()
    time.sleep(1)
