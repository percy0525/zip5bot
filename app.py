from flask import Flask, request, abort
from config import DevConfig
from getdata import get_zip
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
app.config.from_object(DevConfig)

#def hello():
    #return "<h1 style='color:blue'>Hello World!</h1>"

# Channel Access Token
line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
# Channel Secret
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

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
         abort(400)
     return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if type(get_zip(event.message.text)) == list:
        msg_reply = get_zip(event.message.text)
        msg_str = ""
        for msg in msg_reply:
            msg_str += (msg + '\n') 
        # del msg_str[-1]
        message = TextSendMessage(text=msg_str)
        line_bot_api.reply_message(event.reply_token, message)

    else:
        msg_reply = (get_zip(event.message.text))
        message = TextSendMessage(text=msg_reply)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
