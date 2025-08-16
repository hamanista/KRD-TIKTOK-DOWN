from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup
import os

# کارەساتی scraping لە snaptik
def get_tiktok_video_url(tiktok_url):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        page = session.get("https://snaptik.app", headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        token = soup.find("input", {"id": "token"}).get("value")

        data = {
            "url": tiktok_url,
            "token": token
        }

        res = session.post("https://snaptik.app/abc2.php", data=data, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        download_link = soup.find("a", href=True)
        return download_link['href']
    except Exception as e:
        print("Error:", e)
        return None

# ڕیسپۆنس بۆ ناردنی لینکی TikTok
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "tiktok.com" in text:
        await update.message.reply_text("⏳ تکایە چاوبکە، ڤیدیۆکە دێتەوە...")
        video_url = get_tiktok_video_url(text)
        if video_url:
            await update.message.reply_video(video_url)
        else:
            await update.message.reply_text("❌ ببورە، ناتوانم ڤیدیۆکە دابەزێنم.")
    else:
        await update.message.reply_text("👋 تکایە لینکی ڤیدیۆی TikTok بنێرە.")

# فرمانی /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو 👋\nلینکی هەر ڤیدیۆیەک لە TikTok بنێرە بۆ دابەزاندنی بێ واتەرمارک 🎥")

# دامەزراندنی بۆتەکە
def main():
    TOKEN = os.environ.get("8185077536:AAGJNU9xZJVMCPLV7McY6HBm_zrB_392jgI")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ بۆتەکە دامەزرا...")
    app.run_polling()

if __name__ == "__main__":
    main()
