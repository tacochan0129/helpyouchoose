#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('YeDTarsdKiytdqoOC7qQIl/JjhRCNK3UTSj5rUT4vguYoCgASBdMutqc/2yQUdgWf68PJSrqegY9JRm9p97kKu0e3M3BgyTqiWBFdnY5Ugl0huQrHvUbGRqUKa/xhJAJjTMO3rD/rYOcbl5IyKunvAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('da402173412195ab0d896ecc377c7354')

line_bot_api.push_message('U260423b736b8f83bfc9ae5196a8b20a5', TextSendMessage(text='想喝杯咖啡嗎'))

# 監聽所有來自 /callback 的 Post Request
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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('有不錯的咖啡廳嗎',message):
        carousel_template_message = TemplateSendMessage(
             alt_text='免費教學影片',
             template=CarouselTemplate(
                 columns=[
                     CarouselColumn(
                         thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
                         title='Python基礎教學',
                         text='萬丈高樓平地起',
                         actions=[
                             MessageAction(
                                 label='教學內容',
                                 text='拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
                             ),
                             URIAction(
                                 label='馬上查看',
                                 uri='https://marketingliveincode.com/?page_id=270'
                             )
                         ]
                     ),
                     CarouselColumn(
                         thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
                         title='Line Bot聊天機器人',
                         text='台灣最廣泛使用的通訊軟體',
                         actions=[
                             MessageAction(
                                 label='教學內容',
                                 text='Line Bot申請與串接'
                             ),
                             URIAction(
                                 label='馬上查看',
                                 uri='https://marketingliveincode.com/?page_id=2532'
                             )
                         ]
                     ),
                     CarouselColumn(
                         thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
                         title='Telegram Bot聊天機器人',
                         text='唯有真正的方便，能帶來意想不到的價值',
                         actions=[
                             MessageAction(
                                 label='教學內容',
                                 text='Telegrame申請與串接'
                             ),
                             URIAction(
                                 label='馬上查看',
                                 uri='https://marketingliveincode.com/?page_id=2648'
                             )
                         ]
                     )
                 ]
             )
         )
         line_bot_api.reply_message(event.reply_token, carousel_template_message)
     else:
         line_bot_api.reply_message(event.reply_token, TextSendMessage("收到囉!"))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

