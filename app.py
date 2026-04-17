from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AmoCRM Dumaloq Video Service")

BOT_TOKEN = os.getenv("BOT_TOKEN")
VIDEO_NOTE_FILE_ID = os.getenv("VIDEO_NOTE_FILE_ID")

if not BOT_TOKEN or not VIDEO_NOTE_FILE_ID:
    raise ValueError("BOT_TOKEN yoki VIDEO_NOTE_FILE_ID .env faylida yo'q!")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

@app.post("/send_dumaloq")
async def send_dumaloq_video(request: Request):
    try:
        data = await request.json()
        logger.info(f"Webhook keldi: {data}")

        # chat_id ni turli joylardan izlash (AmoCRM + Pact.im uchun)
        chat_id = (
            data.get("chat_id") or
            data.get("telegram_id") or
            data.get("user_id") or
            data.get("contact", {}).get("telegram_id") or
            data.get("message", {}).get("chat", {}).get("id")
        )

        if not chat_id:
            logger.error("chat_id topilmadi!")
            raise HTTPException(status_code=400, detail="chat_id required")

        await bot.send_video_note(
            chat_id=int(chat_id),
            video_note=VIDEO_NOTE_FILE_ID,
            length=640
        )

        logger.info(f"✅ Dumaloq video yuborildi → {chat_id}")
        return {"status": "success", "message": "Video note sent"}

    except Exception as e:
        logger.error(f"Xatolik: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)