from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import random
import time
from datetime import datetime
import pytz
from dateutil import tz

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot thuộc quyền sở hữu của <b>Tải Tiền Trên Mạng 💸</b>. Liên hệ @iamnxa để sử dụng!", parse_mode=constants.ParseMode.HTML)


def convertToLocalDate(date):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Ho_Chi_Minh')
    utc = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    return str(utc.astimezone(to_zone))[11:16]

async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    print(chat_id)

    if chat_id not in [-1001749552228, -1001813759468]:
        if username not in ['minatabar']:
            text = "Bot thuộc quyền sở hữu của <b>Tải Tiền Trên Mạng 💸</b>. Liên hệ @iamnxa để sử dụng!"
            await context.bot.send_message(chat_id, text, parse_mode=constants.ParseMode.HTML)
            return

    if "/funding" in update.message.text:

        res = requests.get("https://contract.mexc.com/api/v1/contract/funding_rate")
        list = sorted(res.json()['data'],
                      key=lambda x: x['fundingRate'], reverse=False)

        top_list = [x for x in list if abs(x['fundingRate']) >= 0.005]
        text = "<b>🔥 TOP FUNDING FEE 🔥</b>\n"

        tokens = requests.get(
            'https://contract.mexc.com/api/v1/contract/detail')

        for index, token in enumerate(tokens.json()['data']):
            for index, item in enumerate(top_list):
                if token['symbol'] == item['symbol']:
                    rate = item['fundingRate']*100
                    margin_max = token['maxLeverage']
                    date  = datetime.fromtimestamp(item['nextSettleTime']/1000.0)
                    text += f"\n<b>{index+1}. {item['symbol']} | x{margin_max} | {convertToLocalDate(date)} | {round(rate, 2)}</b>\n"

                    if(margin_max >= 50 and 50*abs(rate)-100 > 0):
                        text += f"👉 x50 lãi {round(50*abs(rate)-100, 2)}%\n"
                    if(margin_max >= 75 and 75*abs(rate)-100 > 0):
                        text += f"👉 x75 lãi {round(75*abs(rate)-100, 2)}%\n"
                    if(margin_max >= 100 and 100*abs(rate)-100 > 0):
                        text += f"👉 x100 lãi {round(100*abs(rate)-100, 2)}%\n"
                    if(margin_max >= 125 and 125*abs(rate)-100 > 0):
                        text += f"👉 x125 lãi {round(125*abs(rate)-100, 2)}%\n"
                    if(margin_max >= 150 and 150*abs(rate)-100 > 0):
                        text += f"👉 x150 lãi {round(150*abs(rate)-100, 2)}%\n"
                    if(margin_max >= 200 and 200*abs(rate)-100 > 0):
                        text += f"👉 x200 lãi {round(200*abs(rate)-100, 2)}%\n"
        text += "\n<b>Lưu ý:</b>\n<i>- Phí Funding âm => Long 🟢\n- Phí Funding dương => Short 🔴</i>\n\n/funding"

        await context.bot.send_message(chat_id, text, parse_mode=constants.ParseMode.HTML)

app = ApplicationBuilder().token(
    "6661657439:AAHaAC4xGJKbVT6xFXMTt9oP5dDwHhzhXgg").build()


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()
