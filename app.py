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

#讀取先前抓取的咖啡廳資料
import csv
from random import sample
cf = open("cafe.csv", "r", encoding="utf-8")
csv_reader = csv.DictReader(cf)
cf_row = [row for row in csv_reader]
cf.close()

        
# 放上自己的Channel Access Token
line_bot_api = LineBotApi('YeDTarsdKiytdqoOC7qQIl/JjhRCNK3UTSj5rUT4vguYoCgASBdMutqc/2yQUdgWf68PJSrqegY9JRm9p97kKu0e3M3BgyTqiWBFdnY5Ugl0huQrHvUbGRqUKa/xhJAJjTMO3rD/rYOcbl5IyKunvAdB04t89/1O/w1cDnyilFU=')
# 放上自己的Channel Secret
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
    #隨機抽取三家店
    cf_random = sample(cf_row,3)
    cafe1 = cf_random[0]
    cafe2 = cf_random[1]
    cafe3 = cf_random[2]        
    
    #將名稱、敘述、GoogleMaps連結、圖片存進functions
    def name(cafe_num) :
       return cafe_num['咖啡廳名稱']
    def text(cafe_num):
        return cafe_num['敘述']
    def gmap(cafe_num):
        return cafe_num['GoogleMaps']
    def pic(cafe_num):
        return cafe_num['圖片1']
    def thumb(cafe_num):
        return cafe_num['封面']
    if re.match('咖啡廳輪盤',message):
#        #將名稱、敘述、GoogleMaps連結、圖片存進變數
#         name1 = cafe1['咖啡廳名稱']
#         name2 = cafe2['咖啡廳名稱']
#         name3 = cafe3['咖啡廳名稱']
        
#         text1 = cafe1['敘述']
#         text2 = cafe2['敘述']
#         text3 = cafe3['敘述']
        
#         map1 = cafe1['GoogleMaps']
#         map2 = cafe2['GoogleMaps']
#         map3 = cafe3['GoogleMaps']
        
#         pic1 = cafe1['圖片1']
#         pic2 = cafe2['圖片1']
#         pic3 = cafe3['圖片1']
        
#         thumb1 = cafe1['封面']
#         thumb2 = cafe2['封面']
#         thumb3 = cafe3['封面']

        image_carousel_template_message = TemplateSendMessage(
            alt_text='咖啡廳輪盤',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url= pic(cafe1),#cafe1['圖片1']
                        action=MessageAction(
                            label='選這個！',
                            text='我選第一張'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url= pic(cafe2),#cafe2['圖片1']
                        action=MessageAction(
                            label='選這個！',
                            text='我選第二張'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url= pic(cafe3),#cafe3['圖片1']
                        action=MessageAction(
                            label='選這個！',
                            text='我選第三張'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
                
    elif re.match('我選第一張',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='就決定是你了！',
        template=ButtonsTemplate(
            thumbnail_image_url=thumb(cafe1),#cafe1['封面']
            title=name(cafe1),#cafe1['咖啡廳名稱']
            text=text(cafe1),#cafe1['敘述']
            actions=[
                URIAction(
                    label='現在就過去吧！',
                    uri=gmap(cafe1)#cafe1['GoogleMaps']
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    elif re.match('我選第二張',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='就決定是你了！',
        template=ButtonsTemplate(
            thumbnail_image_url=thumb(cafe2),#cafe2['封面']
            title=name(cafe2),#cafe2['咖啡廳名稱']
            text=text(cafe2),#cafe2['敘述']
            actions=[
                URIAction(
                    label='現在就過去吧！',
                    uri=gmap(cafe2)#cafe2['GoogleMaps']
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    elif re.match('我選第三張',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='就決定是你了！',
        template=ButtonsTemplate(
            thumbnail_image_url=thumb(cafe3),#cafe3['封面']
            title=name(cafe3),#cafe3['咖啡廳名稱']
            text=text(cafe3),#cafe3['敘述']
            actions=[
                URIAction(
                    label='現在就過去吧！',
                    uri=gmap(cafe3)#cafe3['GoogleMaps']
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    elif re.match('隨便一家都可以啦',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='隨便啦',
        template=ButtonsTemplate(
            thumbnail_image_url=thumb(cafe3),#cafe3['封面']
            title=name(cafe3),#cafe3['咖啡廳名稱']
            text=text(cafe3),#cafe3['敘述']
            actions=[
                URIAction(
                    label='現在就過去吧！',
                    uri=gmap(cafe3)#cafe3['GoogleMaps']
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('不要再猶豫不決了！'))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
