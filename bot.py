import os
import asyncio
import logging
import traceback
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from yt_dlp import YoutubeDL
import nest_asyncio
import subprocess


def clean_reel_url(url):
    if "?" in url:
        return url.split("?")[0]
    return url


def get_reel_info(url):
    print(f"[DEBUG] get_reel_info received URL: {url}")
    ydl_opts = {
        "quiet": True,
        "cookiefile": "instagram_cookies.txt",
        "noplaylist": True,
        "cachedir": False,  # 🔥 Ye important hai!
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("id"), info.get("title")


nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))
DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")
INSTAGRAM_COOKIE = os.getenv("INSTAGRAM_COOKIE")
print("[DEBUG] Using cookie:", INSTAGRAM_COOKIE)

print("[DEBUG] Cookie file path:", os.path.abspath("cookie.txt"))
print("[DEBUG] Cookie file exists:", os.path.exists("cookie.txt"))

# Check for INSTAGRAM_COOKIE early
if not INSTAGRAM_COOKIE:
    print("[ERROR] INSTAGRAM_COOKIE not set.")
    exit("❌ Please set INSTAGRAM_COOKIE in Railway Environment Variables.")

downloaded_reel_ids = set()


def already_downloaded(video_id):
    return video_id in downloaded_reel_ids


def mark_downloaded(video_id):
    downloaded_reel_ids.add(video_id)


# Create downloads folder
if not os.path.exists("downloads"):
    os.makedirs("downloads")

from urllib.parse import urlparse


def clean_instagram_url(url):
    parsed = urlparse(url)
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return clean_url


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me an Instagram Reel link to download.")


# fallback
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👀 Bot zinda hai, but please send a valid Instagram reel link."
    )

    url = update.message.text.strip().split("?")[0]
    print("[DEBUG] Reel URL:", url)

    if not any(x in url for x in ["/reel/", "/reel"]):
        if "instagram.com/p/" in url or "instagram.com/tv/" in url:
            await update.message.reply_text(
                "❌ This is a post, not a reel. Please send a reel URL."
            )
        else:
            await update.message.reply_text("❌ Invalid Instagram Reel URL.")
        return

    await update.message.reply_text("⏬ Downloading reel...")

    if not INSTAGRAM_COOKIE:
        print("[DEBUG] Cookie missing")
        await update.message.reply_text("❌ Cookie missing.")
        return

    print("[DEBUG] Cookie length:", len(INSTAGRAM_COOKIE))
    print("[DEBUG] Starting yt-dlp process...")


# reel downloader
async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("[DEBUG] Entered download_reel")

    url = update.message.text
    url = clean_reel_url(clean_instagram_url(url))
    print(f"[DEBUG] Cleaned URL: {url}")

    await update.message.reply_text("⏳ Downloading reel, please wait...")

    with open("cookie.txt", "w", encoding="utf-8") as f:
        f.write(INSTAGRAM_COOKIE.strip())

    try:
        reel_id, title = get_reel_info(url)
    except Exception as e:
        print(f"[ERROR] Failed to fetch reel info: {e}")
        await update.message.reply_text(
            "❌ Reel ka info fetch nahi ho paya. Cookie ya link invalid ho sakta hai."
        )
        return

    # Duplicate check
    if reel_id in downloaded_reel_ids:
        await update.message.reply_text("⚠️ Ye reel pehle hi download ho chuki hai.")
        return

    downloaded_reel_ids.add(reel_id)

    try:
        ydl_opts = {
            "outtmpl": "downloads/%(title).50s.%(ext)s",
            "cookiefile": os.path.abspath("cookie.txt")
            "nocheckcertificate": True,
            "cachedir": False,
            "quiet": True,
            "noplaylist": True,
            "format": "mp4",
        }

        with YoutubeDL(ydl_opts) as ydl:
            print(f"[DEBUG] URL Received: {url}")
            info = ydl.extract_info(url, download=True)
            print("Downloaded title:", info["title"])

            video_path = ydl.prepare_filename(info)
            with open(video_path, "rb") as f:
                await update.message.reply_video(f)

    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        await update.message.reply_text("❌ Error aaya reel download/send karne me.")


# main app logic
async def main():
    print("[DEBUG] DOMAIN:", DOMAIN)
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("instagram.com/reel"), download_reel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except RuntimeError:
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    new_loop.run_until_complete(main())
