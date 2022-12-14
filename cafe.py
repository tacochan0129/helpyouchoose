import csv
from random import sample
cf = open("cafe.csv", "r", encoding="utf-8")
csv_reader = csv.DictReader(cf)
cf_row = [row for row in csv_reader]
cf.close()

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

#print(cf_row)
#print(cafe1)
#print(name(cafe1), text(cafe1), map(cafe1), pic(cafe1))
