from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import requests
from bs4 import BeautifulSoup
import jaconv
import datetime

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'YEPHlreofhkVJBUR4qDa8eHD0HNUD7wJnDU/sfLz4QMrmeBwQqWZQuaHYOmttEMDSXr8Eh9zbu9hPu+gUFmON4VwIDPnW0htxVEAQq1zAiHvdzMObvIz+j7Izt+SJzx+xguQuKZ3bUdyarywkcQFLgdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '757702293991cb4716b5008469b54707'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


def waittime_sea(word):
    word = jaconv.hira2kata(word)

    url = 'https://tokyodisneyresort.info/realtime.php?park=sea'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    attraction = []
    wait_time = []
    for attraction_temp in soup.find_all(class_="realtime-attr-name"):
        attraction.append(attraction_temp.text.strip())

    for wait_time_temp in soup.find_all(class_="realtime-attr-condition"):
        wait_time_treat = wait_time_temp.text.split("分")[0].strip()
        if wait_time_treat.isdecimal():
            wait_time_treat += "分"

        if "案内終了" in wait_time_treat:
            wait_time_treat = '案内終了'

        wait_time.append(wait_time_treat)

    temp_list = list(zip(attraction, wait_time))
    s = ''
    for i, _ in enumerate(temp_list):
        tup1 = (temp_list[i][0], temp_list[i][1])
        line = ':'.join(tup1)
        line += '\n'
        if line.startswith(word):
            s += line
    return s


@app.route("/")
def hello_world():
    return 'hello yutaro'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if len(event.message.text) == 1:
        previous_time = datetime.datetime.now()
        word = event.message.text
        line = waittime_sea(word)
        line += 'loop(1)'
        interval = datetime.timedelta(seconds=2)
        current_time = datetime.datetime.now()
        if previous_time + interval < current_time:
            ar_time = datetime.datetime.now()
            line = waittime_sea(word)
            line += 'loop(2)'
            inte = datetime.timedelta(seconds=2)
            nw_time = datetime.datetime.now()
            if ar_time + inte < nw_time:
                line = waittime_sea(word)
                line += 'loop(3)'

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=line))

    elif event.message.text == 'チクタク':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='スミー助けてくれ'))

    elif event.message.text == 'モビリス！':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='モビリ!'))

    elif event.message.text == 'なにしてるんですか':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='夢のカケラ拾ってるんです！'))

    elif event.message.text == 'フォースとともにあらんことを':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='フォースとともにあらんことを'))


if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=port)
