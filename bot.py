from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import yt_dlp
import asyncio
import os 
from moviepy import *
BOT_TOKEN = "7522103470:AAEBucojxmPxeXel3zAlk4TDhM4v0k9MvvQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("ссылочку")

@dp.message(lambda message: message.text.lower().startswith(('https://youtu.be', 'https://www.youtube.com')))
async def video_download(message: Message):
    url = message.text
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'video.%(ext)s',
    }

    try:
        await message.answer("уловил ссылочку щас будет видео")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
        if os.path.exists(file_path):
            await message.answer_video(FSInputFile(file_path))
            builder = ReplyKeyboardBuilder()
            builder.button(text="да")
            builder.button(text="нет")
            await message.answer('скинуть звук отдельно от видео?',reply_markup=builder.as_markup(resize_keyboard=True))
        else:
            await message.answer("не удалось загрузить видео")
    
    except Exception as e:
        await message.answer(f"произошла ошибка: {e}")

@dp.message(lambda message: message.text == "да")
async def mp4_to_mp3(message:Message):
    with VideoFileClip('video.mp4') as video:
        video.audio.write_audiofile("audio.mp3")
    await message.answer_audio(FSInputFile("audio.mp3"))
    mp3_file = 'audio.mp3'
    os.remove(mp3_file)
    mp4_file = 'video.mp4'
    os.remove(mp4_file)

@dp.message(lambda message: message.text == "нет")
async def net(message:Message):
    os.remove('video.mp4')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
<<<<<<< HEAD
=======

>>>>>>> 4a291fc (fix vid format bug)
