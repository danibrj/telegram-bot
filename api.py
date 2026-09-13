from fastapi import FastAPI, Request
from pydantic import BaseModel

from bott import start, test, text_robot, image_robot, voice_robot
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
import os
from contextlib import asynccontextmanager


telegram_app = ApplicationBuilder().token(
    os.getenv("BOT_TOKEN")
).build()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await telegram_app.initialize()
    await telegram_app.start()

    yield

    await telegram_app.stop()
    await telegram_app.shutdown()


app = FastAPI(lifespan=lifespan)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("test", test))

telegram_app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, text_robot)
)

telegram_app.add_handler(
    MessageHandler(filters.PHOTO, image_robot)
)

telegram_app.add_handler(
    MessageHandler(filters.VOICE, voice_robot)
)


class ChatRequest(BaseModel):
    text: str
    


@app.get("/")
async def root():
    return {"message": "Telegram Bot API is running!"}


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    text = request.text
    
    if "سلام" in text:
        response = "سلام چطوری؟"

    elif "خوبی" in text:
        response = "خوبم تو خوبی؟"

    elif "ساعت" in text:
        import time
        response = time.ctime()

    else:
        response = "متوجه نشدم."

    return {
        "response": response
    }
    

@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    update = Update.de_json(data, telegram_app.bot)

    await telegram_app.update_queue.put(update)

    return {"ok": True}