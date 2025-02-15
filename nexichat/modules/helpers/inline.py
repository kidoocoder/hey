from pyrogram.types import InlineKeyboardButton

from config import SUPPORT_GRP, UPDATE_CHNL
from nexichat import OWNER, nexichat


START_BOT = [
    [
        InlineKeyboardButton(
            text="❖ ᴛᴧᴘ тᴏ sᴇᴇ ᴍᴧɢɪᴄ ❖",
            url="https://t.me/Purvi_Chat_bot?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="˹ ❍ᴡɴᴇꝛ ˼", user_id=OWNER),
        InlineKeyboardButton(text="˹ 𝖴ᴘᴅᴀᴛᴇ ˼", url=f"https://t.me/{UPDATE_CHNL}"),
    ],
    [
       # InlineKeyboardButton(text="˹ 𝖴ᴘᴅᴀᴛᴇ ˼", url=f"https://t.me/{UPDATE_CHNL}"),
        InlineKeyboardButton(text="˹ 𝖧ᴇʟᴘ ᴧηᴅ 𝖢ᴏϻϻᴧηᴅs ˼", callback_data="HELP"),
    ],
]


PNG_BTN = [
    [
        InlineKeyboardButton(text="˹ 𝛅ᴜᴘᴘᴏʀᴛ ˼", url="https://t.me/+_GRtGAB9AY1jN2Fl"),
        InlineKeyboardButton(text="⌯ ᴄʟσsє ⌯", callback_data="CLOSE"),
    ],
]


BACK = [
    [
        InlineKeyboardButton(text="⌯ ᴄʟσsє ⌯", callback_data="CLOSE"),
    ],
]


HELP_BTN = [
    [
        InlineKeyboardButton(text="⌯ 𝖢ʜᴀᴛʙᴏᴛ ⌯", callback_data="CHATBOT_CMD"),
        InlineKeyboardButton(text="⌯ 𝖳ᴏᴏʟs ⌯", callback_data="TOOLS_DATA"),
    ],
    [
        InlineKeyboardButton(text="˹ 𝛅ᴜᴘᴘᴏʀᴛ ˼", url="https://t.me/+_GRtGAB9AY1jN2Fl"),
    ],
    [
        InlineKeyboardButton(text="⌯ 𝖡ᴀᴄᴋ ⌯", callback_data="HOME_BACK"),
    ],
]


HELP_BTON = [
    [
        InlineKeyboardButton(text="⌯ 𝖢ʜᴀᴛʙᴏᴛ ⌯", callback_data="CHATBOT_CMD"),
        InlineKeyboardButton(text="⌯ 𝖳ᴏᴏʟs ⌯", callback_data="TOOLS_DATA"),
    ],
    [
        InlineKeyboardButton(text="⌯ ᴄʟσsє ⌯", callback_data="CLOSE"),
    ],
]

CLOSE_BTN = [
    [
        InlineKeyboardButton(text="⌯ ᴄʟσsє ⌯", callback_data="CLOSE"),
    ],
]



MUSIC_BACK_BTN = [
    [
        InlineKeyboardButton(text="sᴏᴏɴ", callback_data=f"soom"),
    ],
]

S_BACK = [
    [
        InlineKeyboardButton(text="⌯ ʙᴀᴄᴋ ⌯", callback_data="SBACK"),
        InlineKeyboardButton(text="⌯ ᴄʟσsє ⌯", callback_data="CLOSE"),
    ],
]


CHATBOT_BACK = [
    [
        InlineKeyboardButton(text="⌯ ʙᴀᴄᴋ ⌯", callback_data="CHATBOT_BACK"),
        InlineKeyboardButton(text="⌯ ᴄʟσsє ⌯", callback_data="CLOSE"),
    ],
]


HELP_START = [
    [
        InlineKeyboardButton(text="⌯ 𝖧ᴇʟᴘ ᴧηᴅ 𝖢ᴏϻϻᴧηᴅs ⌯", callback_data="HELP"),
        InlineKeyboardButton(text="⌯ ᴄʟσsє ⌯", callback_data="CLOSE"),
    ],
]


HELP_BUTN = [
    [
        InlineKeyboardButton(text="➥ ᴏᴘᴇɴ ɪɴ ᴘʀɪᴠɪᴛᴇ", url="https://t.me/RADHIKA_CHAT_RROBOT?start=help"),
    ],
]
