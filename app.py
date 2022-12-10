-- coding: utf-8 --
 """
 Created on Wed Jun  2 21:16:35 2021
 @author: Ivan
 版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
 Line Bot聊天機器人
 第四章 選單功能
 多樣版組合按鈕CarouselTemplate
 """
 載入LineBot所需要的套件
 from flask import Flask, request, abort
 from linebot import (
     LineBotApi, WebhookHandler
 )
 from linebot.exceptions import (
     InvalidSignatureError
 )
 from linebot.models import *
 import re
 app = Flask(name)
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
 # get request body as text body = request.get_data(as_text=True) app.logger.info("Request body: " + body) # handle webhook body try:     handler.handle(body, signature) except InvalidSignatureError:     abort(400) return 'OK'
 # 訊息傳遞區塊
 # 基本上程式編輯都在這個function
 @handler.add(MessageEvent, message=TextMessage)
 def handle_message(event):
     message = text=event.message.text
if re.match('告訴我秘密',message):
        image_message = ImageSendMessage(
            original_content_url='https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-bluehost-v1-0-9%2F659%2F790659%2FAtmP8Pmy%2F9c8c1e647eb14e01898043c0c60bf03a&methods=resize%2C1000%2C5000',
            preview_image_url='https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-bluehost-v1-0-9%2F659%2F790659%2FAtmP8Pmy%2Ffd2258c5ea6c43f591e8d9930d152b94&methods=resize%2C1000%2C5000'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
 # 主程式
 import os
 if name == "main":
     port = int(os.environ.get('PORT', 5000))
     app.run(host='0.0.0.0', port=port)
