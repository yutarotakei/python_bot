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

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'YEPHlreofhkVJBUR4qDa8eHD0HNUD7wJnDU/sfLz4QMrmeBwQqWZQuaHYOmttEMDSXr8Eh9zbu9hPu+gUFmON4VwIDPnW0htxVEAQq1zAiHvdzMObvIz+j7Izt+SJzx+xguQuKZ3bUdyarywkcQFLgdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '757702293991cb4716b5008469b54707'


line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=post)