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

app = Flask(__name__)

line_bot_api = LineBotApi('m7GPbYTn3474e6Q+Jk8okm1RbjZvGVZXxVP6Sz7aiRey4DTFkyJUiclR08+RcSTtB38n90qwEmy+IMgomL6M24Gszqg3oIaM29SB3Ol1GvZ4a5CxNDsZQogusSLBQaWFZlR6VlHN9/35yrKS2sOx9AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0a8f1bab47f5fcbcc11fd8249a5c588e')


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
    app.run()