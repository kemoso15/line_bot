import datetime
import holidays
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.messaging.models import TextMessage, PushMessageRequest
import os

CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
GROUP_ID = os.environ["GROUP_ID"]

jp_holidays = holidays.Japan()
excluded_dates = {
    datetime.date(2025, 12, 30),
    datetime.date(2025, 12, 31),
    datetime.date(2026, 1, 2),
    datetime.date(2026, 1, 3),
    datetime.date(2026, 1, 4)
}

def is_business_day():
    today = datetime.date.today()
    return today.weekday() < 5 and today not in jp_holidays and today not in excluded_dates

if is_business_day():
    print("📤 夕方メッセージ送信")
    configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
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
