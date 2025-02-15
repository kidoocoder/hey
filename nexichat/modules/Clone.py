import logging
import os
import asyncio
import base64
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.errors import AccessTokenExpired, AccessTokenInvalid, SessionPasswordNeeded, PhoneCodeInvalid
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

def is_valid_base64(s):
    try:
        # Check if the string is a valid Base64 string
        base64.b64decode(s, validate=True)
        return True
    except:
        return False

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


@app.on_message(filters.command("delallclone") & filters.user(int(OWNER_ID)))
async def delete_all_cloned_bots(client, message):
    try:
        await clonebotdb.delete_many({})
        CLONES.clear()
        await message.reply_text("**Aʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
    except Exception as e:
        logging.exception(e)
        await message.reply_text(f"**Error clearing all bots:** `{e}`")


@app.on_message(filters.command("idclone"))
async def id_clone(client, message):
    if len(message.command) < 2:
        await message.reply_text("**Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.**")
        return

    session_string = message.text.split("/idclone", 1)[1].strip()
    mi = await message.reply_text("➥ Cʜᴇᴄᴋɪɴɢ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ↺......")

    # Validate the session string
    if not is_valid_base64(session_string):
        await mi.edit_text("**Invalid session string. Please provide a valid Base64 session string.**")
        return

    try:
        ai = Client(":memory:", API_ID, API_HASH, session_string=session_string, plugins=dict(root="nexichat/mplugin"))
        await ai.start()
        user = await ai.get_me()
        user_id = message.from_user.id
        CLONE_OWNERS[user.id] = user_id
    except (SessionPasswordNeeded, PhoneCodeInvalid):
        await mi.edit_text("**Invalid session string. Please provide a valid one.**")
        return
    except Exception as e:
        logging.error(f"Session string: {session_string}")
        logging.exception("Error cloning session.")
        await mi.edit_text(
            f"⚠️ **Error:**\n\n`{e}`\n\n**Cᴏɴᴛᴀᴄᴛ [Sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/+OL6jdTL7JAJjYzVl) ғᴏʀ ʜᴇʟᴘ.**"
        )
        return

    await mi.edit_text("**➥ Cʟᴏɴɪɴɢ ɪs �ʀᴏɢʀᴇss ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ↺...**")
    try:
        details = {
            "user_id": user.id,
            "is_bot": False,
            "name": user.first_name,
            "username": user.username,
            "session_string": session_string,
        }

        await app.send_message(
            OWNER_ID, f"**#New_Clone**\n\n**User:** @{user.username}\n\n**Details:**\n{details}"
        )

        await clonebotdb.insert_one(details)
        await save_clonebot_owner(user.id, user_id)
        CLONES.add(user.id)

        await mi.edit_text(
            f"**➥ Usᴇʀ @{user.username} sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴀʀᴛᴇᴅ ✅.**\n\n"
            "➥ Tᴏ ʀᴇᴍᴏᴠᴇ ᴛʜɪs ᴄʟᴏɴᴇ: `/delclone`\n"
            "➠ Kᴇᴇᴘ sᴜᴘᴘᴏʀᴛ 🙂 ||@BABY09_WORLD||"
        )

        # Add a message handler for the cloned user account to act like a chatbot
        @ai.on_message(filters.text & filters.private)
        async def chatbot_response(client, message):
            # Respond to any text message in private chats
            await message.reply_text(f"Hello! You said: {message.text}")

    except Exception as e:
        logging.exception("Error cloning session.")
        await mi.edit_text(
            f"⚠️ **Error:**\n\n`{e}`\n\n**Cᴏɴᴛᴀᴄᴛ [Sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/+OL6jdTL7JAJjYzVl) ғᴏʀ ʜᴇʟᴘ.**"
        )
