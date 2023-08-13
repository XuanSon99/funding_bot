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

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hãy /funding để kiểm tra <b>Danh Sách Top Funding Fee</b>", parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if "/funding" in update.message.text:

        res = requests.get("https://contract.mexc.com/api/v1/contract/funding_rate")
        list = sorted(res.json()['data'],
                      key=lambda x: x['fundingRate'], reverse=False)

        top_list = [x for x in list if abs(x['fundingRate']) >= 0.005]
        text = "<b>🔥 DANH SÁCH TOP FUNDING FEE 🔥</b>\n"

        tokens = requests.get(
            'https://contract.mexc.com/api/v1/contract/detail')

        for index, token in enumerate(tokens.json()['data']):
            for index, item in enumerate(top_list):
                if token['symbol'] == item['symbol']:
                    rate = item['fundingRate']*100
                    margin_max = token['maxLeverage']
                    text += f"\n<b>{index+1}. {item['symbol']} | x{margin_max} | {str(datetime.fromtimestamp(item['nextSettleTime']/1000.0))[11:16]} | {round(rate, 2)}</b>\n"

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
    "6594323853:AAG4ktQv-t2rD8knKyKc2AGIeU2_lh-j8sw").build()


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()
