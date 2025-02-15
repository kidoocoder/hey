from pyrogram import Client, filters
from pyrogram.types import Message

# Replace these with your own values
API_ID = '21265409'  # Your Telegram API ID
API_HASH = '34c826fd1b989c35e338248d07ad3665'  # Your Telegram API HASH
BOT_TOKEN = "7169013424:AAGQ_khyW-4hcOiPqIYoSkau_ZtYmC2vTq0"
# Initialize the Pyrogram Client for the bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token="your_bot_token")

# Function to clone a Telegram account
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
