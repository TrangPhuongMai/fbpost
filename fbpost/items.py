# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import logging
import datetime

def parse_date (vn_time):
    vn_time = vn_time[0]
    logging.info("==================== <++{}++> ====================".format(vn_time))
    vn_array = vn_time.split(' ')
    l = len(vn_array)

    # sanity check
    if l == 0:
        return '0000000000000000000'

    elif  l == 1:
        return '0000000000000000000'

    # 20 giờ, 15 phut
    elif l == 2:
        if vn_array[1] == 'giờ':
            formated_time = datetime.datetime.now() - datetime.timedelta(hours=int(vn_array[0]))
            return formated_time.strftime("%Y-%m-%d %H:%M:%S")
        elif vn_array[1] == 'phút':
            formated_time = datetime.datetime.now() - datetime.timedelta(minutes=int(vn_array[0]))
            return formated_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return '0000000000000000000'

    elif l == 3:
        return 0

    # Hôm qua lúc 11:15
    elif l == 4:
        return str(datetime.datetime.now().date() - datetime.timedelta(days=1)) + ' ' + vn_array[3] + ':00'

    # 9 tháng 11, lúc 17:29
    elif l == 5:
        year = datetime.datetime.now().year
        formated_time = datetime.datetime(year,int(vn_array[2].replace(',','')),int(vn_array[0])).strftime("%Y-%m-%d") + ' ' + vn_array[-1] + ':00'
        return formated_time

    # 9 tháng 11, 2018 lúc 17:29
    elif l == 6:
        formated_time = datetime.datetime(int(vn_array[3]),int(vn_array[2].replace(',','')),int(vn_array[0])).strftime("%Y-%m-%d") + ' ' + vn_array[-1] + ':00'
        return formated_time
    else:
        return '0000000000000000000'


class FbpostItem(scrapy.Item):
    post_id = scrapy.Field()
    date = scrapy.Field(
        output_processor = parse_date
    )
    reactions = scrapy.Field()
    like = scrapy.Field()
    # pass
