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
    postBack = event.postback.data
    if re.match('咖啡廳輪盤',message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='咖啡廳輪盤',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://doqvf81n9htmm.cloudfront.net/data/Luke1226_165/2020-02/%E5%92%96%E5%95%A1%E5%BB%B3/%E5%8F%B0%E5%8C%97%E7%99%AE%E5%92%96%E5%95%A1_40a.jpg',
                        action=MessageAction(
                            label='選這個！',
                            text='我選第一張'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://wowlavie-aws.hmgcdn.com/file/article_all/%E5%A4%A7%E7%A8%BB%E5%9F%95%E3%80%8CTWATUTIA%E3%80%8D%E5%92%96%E5%95%A1%E5%BB%B31.jpg',
                        action=PostbackAction(
                            label='選這個！',
                            display_text='我選第二張',
                            data='action=喜歡B餐廳'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://live.staticflickr.com/65535/52028350813_4ec4a84ea6_c.jpg?v=pixnet-flickr-app-version',
                        action=PostbackAction(
                            label='選這個！',
                            display_text='我選第三張',
                            data='action=喜歡C餐廳'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
        
        if postBack == '我選第三張':
            buttons_template_message = TemplateSendMessage(
            alt_text='A餐廳',
            template=ButtonsTemplate(
                thumbnail_image_url='https://doqvf81n9htmm.cloudfront.net/data/Luke1226_165/2020-02/%E5%92%96%E5%95%A1%E5%BB%B3/%E5%8F%B0%E5%8C%97%E7%99%AE%E5%92%96%E5%95%A1_40a.jpg',
                title='台北癮咖啡',
                text='',
                actions=[
                    PostbackAction(
                        label='偷偷傳資料',
                        display_text='檯面上',
                        data='action=檯面下'
                    ),
                    MessageAction(
                        label='光明正大傳資料',
                        text='我就是資料'
                    ),
                    URIAction(
                        label='行銷搬進大程式',
                        uri='https://marketingliveincode.com/'
                    )
                ]
            )
        )
            line_bot_api.reply_message(event.reply_token, buttons_template_message)

    elif re.match('我選第一張',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='A餐廳',
        template=ButtonsTemplate(
            thumbnail_image_url='https://doqvf81n9htmm.cloudfront.net/data/Luke1226_165/2020-02/%E5%92%96%E5%95%A1%E5%BB%B3/%E5%8F%B0%E5%8C%97%E7%99%AE%E5%92%96%E5%95%A1_40a.jpg',
            title='台北癮咖啡',
            text='',
            actions=[
                PostbackAction(
                    label='偷偷傳資料',
                    display_text='檯面上',
                    data='action=檯面下'
                ),
                MessageAction(
                    label='光明正大傳資料',
                    text='我就是資料'
                ),
                URIAction(
                    label='行銷搬進大程式',
                    uri='https://marketingliveincode.com/'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
