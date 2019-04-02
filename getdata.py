import pandas as pd
import numpy as np
import jieba

def get_zip(address):
    seg_list = jieba.cut(address)
    if address == "help":
        return  "請輸入您的地址，並按照以下格式:XX市XX區XX路XX號，例如:桃園市中壢區中大路123號(!)若您的門牌有\"X之X號\"，如\"145-3號\"請填入145號即可\n(!)若您的地址路名有分段，如\"中華路二段\"，請輸入\"中華路2段\"\n若需要幫助，請輸入help"
    else:
        try:
            addr_token = list(seg_list)
            addr_city = addr_token[0]
            addr_area = addr_token[1]
            addr_road = addr_token[2]
            addr_munber = addr_token[-2]
            if addr_city == "台北市":
                addr_city = "臺北市"
            if addr_city == "台中市":
                addr_city = "臺中市"
            if addr_city == "台南市":
                addr_city = "臺南市"
            if addr_city == "台東線" or addr_area == "台東市":
                addr_city = "臺東縣"
                addr_area == "臺東市"
            search = number_df[(number_df['City'] == addr_city) & (number_df['Area'] == addr_area) & (number_df['Road'] == addr_road)]
            if search.empty:
                return "請檢查是否有輸入錯誤"
            else:
                msg = []
                result_len = len(list(search.iterrows()))
                for index, row in search.iterrows():
                    msg.append("門牌範圍 : " + row.Scope + " -> " + str(row.Zip5))
                return msg
        except IndexError:
            return "請檢查是否有輸入錯誤"


# def hasDigit(road):
#     hasDigit = False
#     road_list = list(road)
#     for i in range(len(road_list)):
#         if road_list[i].isDigit():
#             hasDigit = True

#         else:
#             pass
#     return hasDigit


number_df = pd.read_csv('number.csv')
city_list = list(set(number_df['City']))
area_list = list(set(number_df['Area']))
road_list = list(set(number_df['Road']))
NewToken = city_list + area_list + road_list
# print(NewToken)
with open('jieba/user_dict.txt', 'w', encoding='utf-8') as f:
    for word in NewToken:
        f.write(word + '\n')
jieba.load_userdict('jieba/user_dict.txt')
# 使用 suggest_freq(segment, tune=True)

