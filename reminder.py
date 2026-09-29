import json
import os
import resend
from datetime import datetime

resend.api_key = os.environ.get("RESEND_API_KEY")
TO_EMAIL = os.environ.get("TO_EMAIL")
FROM_EMAIL = "onboarding@resend.dev"

def load_conferences():
    if not os.path.exists("conferences.json"):
        return []
    with open("conferences.json", "r", encoding="utf-8") as f:
        return json.load(f)

def days_until(date_str):
    if not date_str:
        return None
    today = datetime.now().date()
    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (event_date - today).days

def send_email(conf, days):
    subject = f"🔔 {days} روز تا همایش {conf['name']}"
    html = f"""
    <div style="font-family: Tahoma, sans-serif; direction: rtl; max-width: 600px; margin: auto; padding: 20px; background: #f5f7fa; border-radius: 16px;">
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 24px; border-radius: 12px; color: white; text-align: center;">
            <h1 style="margin: 0; font-size: 22px;">🔔 یادآوری همایش</h1>
            <p style="margin: 8px 0 0; opacity: 0.9; font-size: 15px;">فقط {days} روز مونده!</p>
        </div>
        <div style="background: white; padding: 24px; border-radius: 12px; margin-top: 16px;">
            <h2 style="color: #4a3f8a; margin: 0 0 16px; font-size: 18px;">📌 {conf['name']}</h2>
            <p style="color: #555; margin: 8px 0; font-size: 14px;"><strong>📅 تاریخ برگزاری:</strong> {conf['event_date']}</p>
            {f'<p style="color: #555; margin: 8px 0; font-size: 14px;"><strong>🌐 سایت:</strong> <a href="{conf["url"]}" style="color: #667eea;">{conf["url"]}</a></p>' if conf.get('url') else ''}
            {f'<p style="color: #555; margin: 8px 0; font-size: 14px;"><strong>📍 مکان:</strong> {conf["location"]}</p>' if conf.get('location') else ''}
            <p style="color: #555; margin: 8px 0; font-size: 14px;"><strong>وضعیت مقاله:</strong> {'✅ ارسال شده' if conf.get('paper_submitted') else '⏳ هنوز ارسال نشده'}</p>
            {f'<p style="background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 13px; color: #666; margin-top: 16px;"><strong>📒 یادداشت:</strong> {conf["notes"]}</p>' if conf.get('notes') else ''}
        </div>
    </div>
    """
    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [TO_EMAIL],
            "subject": subject,
            "html": html,
        })
        print(f"✅ ایمیل ارسال شد: {subject}")
        return True
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

def check_and_notify():
    conferences = load_conferences()
    today = datetime.now().date()
    print(f"🔍 بررسی - {today}")
    count = 0
    for conf in conferences:
        days = days_until(conf.get("event_date"))
        if days == 3:  # فقط ۳ روز قبل
            if send_email(conf, days):
                count += 1
    print(f"✅ {count} ایمیل ارسال شد." if count else "📭 یادآوری‌ای نبود.")

if __name__ == "__main__":
    check_and_notify()