#!/usr/bin/env python
# coding: utf-8


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

# 將咖啡廳輪盤每次抽出的結果，存在list中
name_list, text_list = [], []
map_list, pic_list = [], []
thumb_list = []

# 附近店家功能
from gps import *
import rungps

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
         
    def clear_list():
        name_list.clear()
        text_list.clear()
        map_list.clear()
        pic_list.clear()
        thumb_list.clear()
    
    #隨機抽取三家店
    cf_random = sample(cf_row,3)
    cafe1 = cf_random[0]
    cafe2 = cf_random[1]
    cafe3 = cf_random[2]   

    if re.match('咖啡廳輪盤',message):
        #將名稱、敘述、GoogleMaps連結、圖片存進變數
        name1, name2, name3 = cafe1['咖啡廳名稱'], cafe2['咖啡廳名稱'], cafe3['咖啡廳名稱']
        text1, text2, text3 = cafe1['敘述'], cafe2['敘述'], cafe3['敘述']
        map1, map2, map3 = cafe1['GoogleMaps'], cafe2['GoogleMaps'], cafe3['GoogleMaps']
        pic1, pic2, pic3 = cafe1['圖片1'], cafe2['圖片1'], cafe3['圖片1']
        thumb1, thumb2, thumb3 = cafe1['封面'], cafe2['封面'], cafe3['封面']
        
        name_list.extend([name1, name2, name3])
        text_list.extend([text1, text2, text3])
        map_list.extend([map1, map2, map3])
        pic_list.extend([pic1, pic2, pic3])
        thumb_list.extend([thumb1, thumb2, thumb3])
        
        image_carousel_template_message = TemplateSendMessage(
            alt_text='咖啡廳輪盤',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url= pic1,#cafe1['圖片1']
                        action=MessageAction(
                            label='選這間！',
                            text='我選第一張'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url= pic2,#cafe2['圖片1']
                        action=MessageAction(
                            label='選這間！',
                            text='我選第二張'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url= pic3,#cafe3['圖片1']
                        action=MessageAction(
                            label='選這間！',
                            text='我選第三張'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
#     if re.match('附近店家',message):
#         line_bot_api.reply_message(event.reply_token, TextSendMessage('此功能尚未完善唷！\n敬請期待🤗'))
    
    if re.match('我選第一張',message):
        if name_list == []:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('不能反悔唷😥\n若要重新一輪，請點選"咖啡廳輪盤"以開啟新的一輪喔！'))
        else:
            buttons_template_message = TemplateSendMessage(
            alt_text='就決定是你了！',
            template=ButtonsTemplate(
                thumbnail_image_url=thumb_list[0],#cafe1['封面']
                title=name_list[0],#cafe1['咖啡廳名稱']
                text=text_list[0],#cafe1['敘述']
                actions=[
                    URIAction(
                        label='現在就過去吧！',
                        uri=map_list[0]#cafe1['GoogleMaps']
                    )
                ]
            )
        )
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
            clear_list()
        
    elif re.match('我選第二張',message):
        if name_list == []:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('不能反悔唷😥\n若要重新一輪，請點選"咖啡廳輪盤"以開啟新的一輪喔！'))
        else:
            buttons_template_message = TemplateSendMessage(
            alt_text='就決定是你了！',
            template=ButtonsTemplate(
                thumbnail_image_url=thumb_list[1],#cafe2['封面']
                title=name_list[1],#cafe2['咖啡廳名稱']
                text=text_list[1],#cafe2['敘述']
                actions=[
                    URIAction(
                        label='現在就過去吧！',
                        uri=map_list[1]#cafe2['GoogleMaps']
                    )
                ]
            )
        )
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
            clear_list()
        
    elif re.match('我選第三張',message):
        if name_list == []:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('不能反悔唷😥\n若要重新一輪，請點選"咖啡廳輪盤"以開啟新的一輪喔！'))
        else:
            buttons_template_message = TemplateSendMessage(
            alt_text='就決定是你了！',
            template=ButtonsTemplate(
                thumbnail_image_url=thumb_list[2], #cafe3['封面']
                title=name_list[2], #cafe3['咖啡廳名稱']
                text=text_list[2], #cafe3['敘述']
                actions=[
                    URIAction(
                        label='現在就過去吧！',
                        uri=map_list[2] #cafe3['GoogleMaps']
                    )
                ]
            )
        )
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
            clear_list()
        
    if re.match('隨便啦',message):
         #隨機抽取三家店
        cf_random = sample(cf_row,3)
        cafe_r = cf_random[0]

        buttons_template_message = TemplateSendMessage(
        alt_text='隨便啦',
        template=ButtonsTemplate(
            thumbnail_image_url=cafe_r['封面'],
            title=cafe_r['咖啡廳名稱'],
            text=cafe_r['敘述'],
            actions=[
                URIAction(
                    label='現在就過去吧！',
                    uri=cafe_r['GoogleMaps']
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    # 附近店家功能
    if re.match('附近店家',message):
#         line_bot_api.reply_message(event.reply_token, TextSendMessage('請傳送指定的位置喔~'))
#     if event.message.type == 'location':
#         address = event.message.address

#         near_coffee_shop_location = 
#         near_coffee_shop_dic = get_nearest_coffee_shop(near_coffee_shop_location)
#         lat = near_coffee_shop_dic['lat']
#         lng = near_coffee_shop_dic['lng']        
#         # set
#         radius = 100
#         keyword = 'coffee'
#         nearby_coffee = get_nearby_places(lat, lng, radius, keyword)

#         if nearby_coffee:
#             nearest_coffee_shop = nearby_coffee[0]
#             photo_ref = nearest_coffee_shop['photos'][0]['photo_reference']
#             photo_width = nearest_coffee_shop['photos'][0]['width']
#             thumbnail_image_url = f"https://maps.googleapis.com/maps/api/place/photo?key={GOOGLE_API_KEY}&photoreference={photo_ref}&maxwidth={photo_width}"
#             nearest_coffee_details = get_place_details(nearest_coffee_shop['place_id'])
#             coffee_name = nearest_coffee_details['name']
#             coffee_rating = nearest_coffee_details['rating']
#             maps_url = f'https://www.google.com/maps/search/?api=1&query={lat},{lng}&query_place_id={nearest_coffee_shop["place_id"]}'
        coffee_shop = nearest_coffee("新北市新莊區民樂街39號")
        coffee_name = coffee_shop[0]
        coffee_rating = str(coffee_shop[1])
        maps_url = coffee_shop[2]
        thumbnail_url = coffee_shop[3]
#         coffee_name = "Cafefe Libero"
#         coffee_rating = "4.2"
#         thumbnail_image_url = "https://play-lh.googleusercontent.com/Kf8WTct65hFJxBUDm5E-EpYsiDoLQiGGbnuyP6HBNax43YShXti9THPon1YKB6zPYpA"
#         maps_url = "https://www.google.com.tw/maps/place/SECOND+FLOOR+CAFE+%E8%B2%B3%E6%A8%93%E4%BB%81%E6%84%9B/@25.0379115,121.5236378,15z/data=!3m1!5s0x3442a97ebf47ca7b:0x6fe70de6eeb4a6e4!4m6!3m5!1s0x3442a97ebf69e67b:0xf06276ea3de8b70!8m2!3d25.0379126!4d121.5323917!16s%2Fg%2F12hk8x73m"
        buttons_template_message = TemplateSendMessage(
        alt_text = '附近店家',
        template=ButtonsTemplate(
            thumbnail_image_url = thumbnail_url,
            title = coffee_name,
            text = "評分：" + coffee_rating,
            actions = [
                URIAction(
                    label = '現在就過去吧！',
                    uri = maps_url
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(coffee_name))
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(maps_url))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('感謝您的使用❤️'))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
