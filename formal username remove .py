from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from instagrapi import Client as InstaClient
import time
import random

BOT_TOKEN = "7880452969:AAGE42lYLbqh41ttMXqxiy_wF7PEeHIJelE"  # Replace with your bot token

# List of profile pictures
profile_pics = ["1.jpg", "2.jpg", "3.jpg"]

# Dictionary to store users' session IDs
user_sessions = {}

# Create Telegram Bot Client
bot = Client("instagram_bot", bot_token=BOT_TOKEN)


@bot.on_message(filters.command("start"))
async def start_command(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛑 Remove Former Username", callback_data="remove_former")]
    ])
    await message.reply_text(
        "👋 Welcome to the Instagram Former Username Remover Bot!\n\n"
        "Click the button below to start removing your former username.",
        reply_markup=keyboard
    )


@bot.on_callback_query(filters.regex("remove_former"))
async def request_session(client, callback_query):
    await callback_query.message.edit_text("📌 Please send your Instagram Session ID to proceed.")


@bot.on_message(filters.text & ~filters.command)
async def process_session_id(client, message):
    user_id = message.from_user.id
    session_id = message.text.strip()
    user_sessions[user_id] = session_id

    await message.reply_text("✅ Session ID received! Starting the process now...")

    await remove_former_username(user_id, message)


async def remove_former_username(user_id, message):
    session_id = user_sessions.get(user_id)
    if not session_id:
        await message.reply_text("⚠️ No session ID found. Please send it again.")
        return

    insta_client = InstaClient()
    insta_client.set_settings({"sessionid": session_id})

    try:
        insta_client.get_timeline_feed()
        await message.reply_text("✅ Logged in successfully!")
    except Exception as e:
        await message.reply_text("❌ Invalid or expired session ID. Please try again.")
        return

    for i in range(100):
        try:
            new_pic = profile_pics[i % len(profile_pics)]
            insta_client.account_change_picture(new_pic)
            await message.reply_text(f"🔄 Changed profile picture to {new_pic} ({i+1}/100)")

            time.sleep(random.randint(10, 14))

        except Exception as e:
            await message.reply_text(f"⚠️ Error changing picture: {e}")
            time.sleep(30)

    await message.reply_text("🎉 Former Username Removal Completed!")


bot.run()