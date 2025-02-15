from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "6435225"
# -------------------------------------------------------------
API_HASH = "4e984ea35f854762dcde906dce426c2d"
# --------------------------------------------------------------
BOT_TOKEN = getenv("BOT_TOKEN", "7169013424:AAGQ_khyW-4hcOiPqIYoSkau_ZtYmC2vTq0")
OPENAI = getenv("OPENAI", "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")
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(getenv("OWNER_ID", "8182605117"))
SUPPORT_GRP = "PURVI_UPDATES"
UPDATE_CHNL = "PURVI_SUPPORT"
OWNER_USERNAME = "ll_ALPHA_BABY_lll"

# Messages
WELCOME_MSG = "Welcome to the Bot Cloner! Use /idclone <session_string> to clone a bot."
INVALID_SESSION_MSG = "❌ Invalid session string provided. Please check and try again."
SUCCESS_MSG = "✅ Bot successfully cloned! You can now use the account."
ERROR_MSG = "❌ An error occurred while cloning the bot: {}"


# Random Start Images
IMG = [
    "https://files.catbox.moe/4q7c4w.jpg",
    "https://files.catbox.moe/90z6sq.jpg",
    "https://files.catbox.moe/rdfi4z.jpg",
    "https://files.catbox.moe/6f9rgp.jpg",
    "https://files.catbox.moe/99wj12.jpg",
    "https://files.catbox.moe/ezpnd2.jpg",
    "https://files.catbox.moe/e7q55f.jpg",
]
