import logging
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=open("download.jpg", 'rb'),caption="سلام دوست عزیز\n خیلی خوش آمدی")
    
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("متن دریافت شد")

async def text_robot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(text)
    print(type(text))
    t = time.time()
    realTime = time.ctime(t)
    
    if "سلام" in text:
        await update.message.reply_text("سلام چطوری؟ من که خیلی خوبم عزیزم")
        
    if "خوبی" in text:
        await update.message.reply_text("خوبم تو خوبی عزیز؟")    

    if "ساعت" in text:
        await update.message.reply_text(realTime)     

async def image_robot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message)
    
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive("dani.jpg")
    
    
    await update.message.reply_text("عکس دریافت شد")
    

async def voice_robot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message)
    
    voice = await update.message.voice.get_file()
    await voice.download_to_drive("voice1.ogg")
    
    await update.message.reply_text("ویس دریافت شد")


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        return


def run_health_server():
    port = int(os.environ.get("PORT", 10000))

    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()



if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    
    threading.Thread(target=run_health_server, daemon=True).start()

    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    test_handler = CommandHandler('test', test)
    application.add_handler(test_handler)
    
    text_handler = MessageHandler(filters.TEXT,text_robot)
    application.add_handler(text_handler)

    image_handler = MessageHandler(filters.PHOTO,image_robot)
    application.add_handler(image_handler)
    
    voice_handler = MessageHandler(filters.VOICE,voice_robot)
    application.add_handler(voice_handler)
    
    application.run_polling()