import random
import os
import codecs
import logging
import traceback
from urllib.parse import urlparse
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

nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
IG_COOKIE = os.getenv("IG_COOKIE")
proxy_list_raw = os.getenv("ALL_PROXIES", "")
proxy_list = proxy_list_raw.split(",") if proxy_list_raw else []

SOCKS5_PROXY = random.choice(proxy_list) if proxy_list else None
print("🌀 Using proxy:", SOCKS5_PROXY)  # Debug line

if not IG_COOKIE:
    exit("❌ Please set IG_COOKIE in Railway Environment Variables.")

cookie_content = codecs.decode(IG_COOKIE, "unicode_escape")
with open("cookie.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(cookie_content)

downloaded_reel_ids = set()


def clean_reel_url(url):
    return url.split("?")[0] if "?" in url else url


def clean_instagram_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def get_reel_info(url):
    print(f"[DEBUG] Getting reel info: {url}")
    ydl_opts = {
        "quiet": True,
        "cookiefile": os.path.abspath("cookie.txt"),
        "noplaylist": True,
        "nocheckcertificate": True,
        "cachedir": False,
        "proxy": SOCKS5_PROXY,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("id"), info.get("title")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me an Instagram Reel link to download.")


async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = clean_reel_url(clean_instagram_url(update.message.text.strip()))
    await update.message.reply_text("⏳ Downloading reel, please wait...")

    try:
        reel_id, title = get_reel_info(url)
    except Exception as e:
        print("[ERROR] Info fetch failed:", e)
        await update.message.reply_text(
            "❌ Failed to fetch reel info. Cookie ya link invalid ho sakta hai."
        )
        return

    if reel_id in downloaded_reel_ids:
        await update.message.reply_text("⚠️ Ye reel pehle hi download ho chuki hai.")
        return

    downloaded_reel_ids.add(reel_id)

    try:
        ydl_opts = {
            "outtmpl": "downloads/%(title).50s.%(ext)s",
            "cookiefile": os.path.abspath("cookie.txt"),
            "nocheckcertificate": True,
            "cachedir": False,
            "quiet": True,
            "noplaylist": True,
            "format": "mp4",
            "proxy": SOCKS5_PROXY,
            "socket_timeout": 10,
            "force_ipv4": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, "rb") as f:
            await update.message.reply_video(f)

    except Exception as e:
        print("[ERROR] Download/send failed:", e)
        await update.message.reply_text("❌ Error aaya reel download/send karne me.")


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com/reel/" not in url:
        if "instagram.com/p/" in url or "instagram.com/tv/" in url:
            await update.message.reply_text(
                "❌ This is a post, not a reel. Please send a reel URL."
            )
        else:
            await update.message.reply_text("❌ Invalid Instagram Reel URL.")
        return

    await download_reel(update, context)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("instagram.com/reel"), download_reel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
