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

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'YEPHlreofhkVJBUR4qDa8eHD0HNUD7wJnDU/sfLz4QMrmeBwQqWZQuaHYOmttEMDSXr8Eh9zbu9hPu+gUFmON4VwIDPnW0htxVEAQq1zAiHvdzMObvIz+j7Izt+SJzx+xguQuKZ3bUdyarywkcQFLgdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '757702293991cb4716b5008469b54707'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


def waittime_sea():
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

        wait_time.append(wait_time_treat)

    temp_list = []
    for i, _ in enumerate(attraction):
        temp_list.append({attraction[i]: wait_time[i]})
    return '\n'.join(map(str, temp_list))


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
    if event.message.text == 'あ':
        line = waittime_sea()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=line))

    elif event.message.text == '':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=port)
