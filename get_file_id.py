import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_TELEGRAM_ID = int(os.getenv("YOUR_TELEGRAM_ID"))

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def main():
    try:
        # Eng muhim o'zgartirish — FSInputFile ishlatish
        video_note_file = FSInputFile("video_note_ready.mp4")

        msg = await bot.send_video_note(
            chat_id=YOUR_TELEGRAM_ID,
            video_note=video_note_file,  # FSInputFile obyekti
            length=640,
            disable_notification=False
        )

        print("✅ Dumaloq video muvaffaqiyatli yuborildi!")
        print("File ID       →", msg.video_note.file_id)
        print("Duration      →", msg.video_note.duration, "sekund")
        print("Length        →", msg.video_note.length)
        print("\n" + "=" * 60)
        print("📋 .env fayliga quyidagicha qo'ying (nusxa ko'chiring):")
        print(f'VIDEO_NOTE_FILE_ID={msg.video_note.file_id}')
        print("=" * 60)

    except Exception as e:
        print("❌ Xatolik:", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())