import random
import os
import json
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

BOT_TOKEN = os.getenv("BOT_TOKEN")
IG_COOKIE = os.getenv("IG_COOKIE")
proxy_list_raw = os.getenv("ALL_PROXIES", "")
proxy_list = proxy_list_raw.split(",") if proxy_list_raw else []
SOCKS5_PROXY = random.choice(proxy_list) if proxy_list else None
print("🌀 Using proxy:", SOCKS5_PROXY)

PROXY_LIST = [
    "socks5://ZZbPYzrL77t:ewQw8Y0C2h36@mel.socks.ipvanish.com:1080",
    "socks5://ZZbPYzrL77t:ewQw8Y0C2h36@lon.socks.ipvanish.com:1080",
    "socks5://ZZbPYzrL77t:ewQw8Y0C2h36@ams.socks.ipvanish.com:1080",
    "socks5://ZZbPYzrL77t:ewQw8Y0C2h36@dal.socks.ipvanish.com:1080",
    "socks5://ZZbPYzrL77t:ewQw8Y0C2h36@nyc.socks.ipvanish.com:1080",
    "socks5://ZZbPYzrL77t:ewQw8Y0C2h36@phx.socks.ipvanish.com:1080",
]

CURRENT_PROXY = {"value": PROXY_LIST[0]}  # Default proxy


def set_random_proxy():
    CURRENT_PROXY["value"] = random.choice(PROXY_LIST)
    os.environ["SOCKS5_PROXY"] = CURRENT_PROXY["value"]


def get_current_proxy():
    return CURRENT_PROXY["value"]


async def cmd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠️ *Available Commands:*\n\n"
        "/start - Bot ko start kare\n"
        "/proxy - Current proxy dikhaye\n"
        "/cmd - Yeh command list dikhaye\n"
        "/rotate - Naya random proxy set kare\n"
        "/switch <index> - Specific proxy lagaye (index 0 se shuru)\n"
        "/allproxies - Sabhi proxy list dikhaye\n"
        "(reel link) - Instagram reel ka video bheje\n\n"
        "🌀 Proxy auto-rotate ho raha hai har 3 minute me.",
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def rotate_proxy_every(interval_seconds: int):
    while True:
        set_random_proxy()
        print(f"🔁 Proxy rotated to: {get_current_proxy()}")
        await asyncio.sleep(interval_seconds)


async def proxy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = get_current_proxy()
    await update.message.reply_text(
        f"🛰️ Current Proxy in use:\n`{current}`", parse_mode="Markdown"
    )


async def switch_proxy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_random_proxy()
    current = get_current_proxy()
    await update.message.reply_text(
        f"🔀 Proxy switched!\n\nNew Proxy: `{current}`", parse_mode="Markdown"
    )


nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

if not IG_COOKIE:
    exit("❌ Please set IG_COOKIE in Railway Environment Variables.")

cookie_path = "session_data.bin"

if not os.path.exists(cookie_path):
    print("🔐 Writing cookie from IG_COOKIE (header-style)...")
    cookie_content = codecs.decode(IG_COOKIE, "unicode_escape")
    with open(cookie_path, "w", encoding="utf-8", newline="\n") as f:
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
        "cookiefile": "session_data.bin",
        "format": "bestvideo+bestaudio/best",
        "noplaylist": True,
        "nocheckcertificate": True,
        "cachedir": False,
        "proxy": SOCKS5_PROXY,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("id"), info.get("title")


def download_from_url(url, title):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        "outtmpl": "downloads/%(title).50s.%(ext)s",
        "cookiefile": "session_data.bin",
        "nocheckcertificate": True,
        "cachedir": False,
        "quiet": True,
        "noplaylist": True,
        "format": "bestvideo+bestaudio/best",
        "proxy": SOCKS5_PROXY,
        "socket_timeout": 10,
        "force_ipv4": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info)
    return video_path


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me an Instagram Reel link to download.")


async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = clean_reel_url(clean_instagram_url(update.message.text.strip()))
    msg = await update.message.reply_text("⏳ Downloading reel, please wait...")

    try:
        reel_id, title = get_reel_info(url)
        if reel_id in downloaded_reel_ids:
            await update.message.reply_text("⚠️ Ye reel pehle hi download ho chuki hai.")
            return

        downloaded_reel_ids.add(reel_id)
        video_path = download_from_url(url, title)

        with open(video_path, "rb") as f:
            await update.message.reply_video(f)

        await msg.delete()

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
    app.add_handler(CommandHandler("proxy", proxy_command))
    app.add_handler(CommandHandler("cmd", cmd_command))
    app.add_handler(MessageHandler(filters.Regex("instagram.com/reel"), download_reel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    asyncio.create_task(rotate_proxy_every(180))  # 180 seconds = 3 minutes

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
