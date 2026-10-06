import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "facebook.com" in url or "fb.watch" in url:
        await update.message.reply_text("⏳ ဗီဒီယိုကို ရယူနေပါပြီ၊ ခဏစောင့်ပါ...")
        output_filename = "fb_video.mp4"
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_filename,
            'quiet': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            await update.message.reply_video(video=open(output_filename, 'rb'))
            if os.path.exists(output_filename):
                os.remove(output_filename)
        except Exception as e:
            await update.message.reply_text(f"❌ ဗီဒီယိုဒေါင်းလုပ်ဆွဲရာတွင် အမှားအယွင်းရှိနေပါသည်။")
            if os.path.exists(output_filename):
                os.remove(output_filename)
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ မှန်ကန်သော Facebook ဗီဒီယိုလင့်ခ်ကို ပို့ပေးပါ။")

def main():
    # Render က Environment Variable ကနေ Token ကို ယူပါမယ်
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable is missing!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    application.run_polling()

if __name__ == '__main__':
    main()