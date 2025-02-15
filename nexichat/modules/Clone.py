import logging
import os
import asyncio
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import AccessTokenExpired, AccessTokenInvalid
import config
from config import API_HASH, API_ID, OWNER_ID
from nexichat import CLONE_OWNERS
from nexichat import nexichat as app
from nexichat import db as mongodb

CLONES = set()
cloneownerdb = mongodb.cloneownerdb
clonebotdb = mongodb.clonebotdb

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.insert_one({"bot_id": bot_id, "user_id": user_id})

@app.on_message(filters.command(["clone", "host", "deploy"]))
async def clone_txt(client, message):
    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("➥ Cʜᴇᴄᴋɪɴɢ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ↺......")
        try:
            ai = Client(bot_token, API_ID, API_HASH, bot_token=bot_token, plugins=dict(root="nexichat/mplugin"))
            await ai.start()
            bot = await ai.get_me()
            bot_id = bot.id
            user_id = message.from_user.id
            CLONE_OWNERS[bot_id] = user_id
        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text("**Invalid bot token. Please provide a valid one.**")
            return
        except Exception:
            cloned_bot = await clonebotdb.find_one({"token": bot_token})
            if cloned_bot:
                await mi.edit_text("**🤖 Tʜɪs ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ✅.**")
                return

        await mi.edit_text("**➥ Cʟᴏɴɪɴɢ ɪs ᴘʀᴏɢʀᴇss ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ↺...**")
        try:
            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": user_id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
            }

            await app.send_message(
                OWNER_ID, f"**#New_Clone**\n\n**Bot:** @{bot.username}\n\n**Details:**\n{details}"
            )

            await clonebotdb.insert_one(details)
            await save_clonebot_owner(bot.id, user_id)
            CLONES.add(bot.id)

            await mi.edit_text(
                f"**➥ Bᴏᴛ @{bot.username} sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴀʀᴛᴇᴅ ✅.**\n\n"
                "➥ Tᴏ ʀᴇᴍᴏᴠᴇ ᴛʜɪs ᴄʟᴏɴᴇ: `/delclone`\n"
                "➠ Kᴇᴇᴘ sᴜᴘᴘᴏʀᴛ 🙂 ||@BABY09_WORLD||"
            )
        except Exception as e:
            logging.exception("Error cloning bot.")
            await mi.edit_text(
                f"⚠️ **Error:**\n\n`{e}`\n\n**Cᴏɴᴛᴀᴄᴛ [Sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/+OL6jdTL7JAJjYzVl) ғᴏʀ ʜᴇʟᴘ.**"
            )
    else:
        await message.reply_text("**Pʀᴏᴠɪᴅᴇ ᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀғᴛᴇʀ `/clone` ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ @BotFather.**")


@app.on_message(filters.command("cloned"))
async def list_cloned_bots(client, message):
    try:
        cloned_bots = clonebotdb.find()
        cloned_bots_list = await cloned_bots.to_list(length=None)
        if not cloned_bots_list:
            await message.reply_text("No cloned bots found.")
            return
        total_clones = len(cloned_bots_list)
        text = f"**Total Cloned Bots:** {total_clones}\n\n"
        for bot in cloned_bots_list:
            text += f"**Bot ID:** `{bot['bot_id']}`\n"
            text += f"**Name:** {bot['name']}\n"
            text += f"**Username:** @{bot['username']}\n\n"
        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("**Error fetching cloned bots list.**")


@app.on_message(filters.command(["delclone", "deleteclone"]))
async def delete_cloned_bot(client, message):
    if len(message.command) < 2:
        await message.reply_text("**Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.**")
        return

    bot_token = " ".join(message.command[1:])
    ok = await message.reply_text("Cʜᴇᴄᴋɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ...")
    try:
        cloned_bot = await clonebotdb.find_one({"token": bot_token})
        if cloned_bot:
            await clonebotdb.delete_one({"token": bot_token})
            CLONES.remove(cloned_bot["bot_id"])
            await ok.edit_text("**🤖 Bᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ☠️.**")
        else:
            await message.reply_text("**Bᴏᴛ ᴛᴏᴋᴇɴ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴄʟᴏɴᴇᴅ ʙᴏᴛs.**")
    except Exception as e:
        logging.exception(e)
        await ok.edit_text(f"**Error removing bot:** `{e}`")


async def restart_bots():
    plugins_root = "nexichat/mplugin"
    if not os.path.isdir(plugins_root):
        logging.error(f"Plugins directory not found: {plugins_root}")
        return

    bots = [bot async for bot in clonebotdb.find()]
    for bot in bots:
        bot_token = bot["token"]
        ai = Client(bot_token, API_ID, API_HASH, bot_token=bot_token, plugins=dict(root=plugins_root))
        try:
            await ai.start()
            bot_info = await ai.get_me()
            CLONES.add(bot_info.id)
        except (AccessTokenExpired, AccessTokenInvalid):
            await clonebotdb.delete_one({"token": bot_token})

# Function to clone a chatbot
"""@app.on_message(filters.command("idclone"))
async def clone_chatbot(client: Client, message: Message):
    try:
        # Extract the target chatbot ID from the command
        target_chatbot_id = int(message.command[1])
        
        # Get the target chatbot's information
        target_chatbot = await client.get_chat(target_chatbot_id)
        
        # Clone the chatbot (this is a placeholder, you need to implement the actual cloning logic)
        # For example, you might want to copy the chatbot's name, description, etc.
        cloned_chatbot_name = f"Cloned {target_chatbot.title}"
        
        # Send a message confirming the cloning
        await message.reply_text(f"Chatbot '{target_chatbot.title}' has been cloned as '{cloned_chatbot_name}'.")
    
    except IndexError:
        await message.reply_text("Please provide a valid chatbot ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")"""


@app.on_message(filters.command("delallclone") & filters.user(int(OWNER_ID)))
async def delete_all_cloned_bots(client, message):
    try:
        await clonebotdb.delete_many({})
        CLONES.clear()
        await message.reply_text("**Aʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
    except Exception as e:
        logging.exception(e)
        await message.reply_text(f"**Error clearing all bots:** `{e}`")

async def clone_telegram_account(client: Client, message: Message, session_string: str):
    try:
        # Initialize the original account client using the provided session string
        original_client = Client("original_account", api_id=API_ID, api_hash=API_HASH, session_string=session_string)

        # Start the original account client
        await original_client.start()

        # Get the original account's profile information
        original_me = await original_client.get_me()
        original_first_name = original_me.first_name
        original_last_name = original_me.last_name
        original_bio = (await original_client.get_chat(original_me.id)).bio
        original_photo = await original_client.download_media(original_me.photo.big_file_id) if original_me.photo else None

        # Initialize the clone account client (the bot itself)
        clone_client = client

        # Update the clone account's profile information
        await clone_client.update_profile(
            first_name=original_first_name,
            last_name=original_last_name,
            bio=original_bio
        )

        # Set the clone account's profile picture
        if original_photo:
            await clone_client.set_profile_photo(photo=original_photo)

        # Notify the user that cloning is complete
        await message.reply_text(f"Telegram account '{original_first_name} {original_last_name}' has been cloned successfully.")

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
    finally:
        # Stop the original client
        await original_client.stop()

# Handler for the /idclone command
@app.on_message(filters.command("idclone"))
async def idclone_command(client: Client, message: Message):
    try:
        # Extract the session string from the command
        session_string = message.command[1]
        
        # Call the clone function
        await clone_telegram_account(client, message, session_string)
    
    except IndexError:
        await message.reply_text("Please provide a session string. Usage: /idclone <session_string>")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
