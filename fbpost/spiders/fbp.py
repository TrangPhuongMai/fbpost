# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.http import Request
import pandas as pd
from scrapy.loader import ItemLoader
from fbpost.items import FbpostItem

class FbpSpider(scrapy.Spider):
    name = 'fbp'
    urls = pd.read_csv('/home/nero/PycharmProjects/fbpost/mbasic.csv')
    start_urls = urls['URL'][:10].array
    def __init__(self, *args, **kwargs):
        self.cookies = {
            'xs': '41%3Atzu2RO5kFIM5WQ%3A2%3A1577019585%3A8613%3A5755',
            'c_user': '100041368987839',
            'datr': 'aSHpXZB1y6WSztrUuQox29_Z',
            'fr': '13DlBHb6iVc5WPK9J.AWUS_ATrbYXgHnK9JI836eoxcxI.BddYQf.ev.F4H.0.0.BeEjY9.AWV7z1Xg'
        }

    def parse(self, response):
        for url in self.start_urls:
            l = ItemLoader(item=FbpostItem(),response=response)
            l.add_value('post_id',url)
            yield Request(url, cookies=self.cookies, meta={'item': l,'proxy': "http://103.143.206.17:443"},callback=self.parse_p)
    
    def parse_p(self,response):

        # logging.info(response.xpath('//div//text()').extract())
        check_reactions = response.xpath("//a[contains(@href,'reaction/profile')]//text()").get()
        # logging.info("check reactions {}".format(check_reactions))
        date = response.xpath("//div[@id='m_story_permalink_view']//abbr/text()").extract()
        l = ItemLoader(item=FbpostItem(), response=response, parent=response.meta['item'])
        try:
            l.add_xpath('date',"//div[@id='m_story_permalink_view']//abbr/text()")
        except:
            pass

        if not check_reactions:
            logging.info("yield new.load_item()")
        else:
            # new.add_xpath('reactions', "//a[contains(@href,'reaction/profile')]/div/div/text()")
            reactions = response.xpath("//div[contains(@id,'sentence')]/a[contains(@href,'reaction/profile')]/@href").extract()
            reactions = response.urljoin(reactions[0])
            logging.info(reactions)
            yield scrapy.Request(reactions,cookies=self.cookies, callback=self.parse_reactions,meta={'item':l})


    def parse_reactions(self, response):
        # logging.info("============= parse_reactions ==============")
        l = ItemLoader(item=FbpostItem(), response=response, parent=response.meta['item'])
        s = response.xpath("//a[contains(@href,'total_count') and not(contains(@href,'reaction_type'))]/@href").get()
        logging.info(type(s))
        if s is not None:
            l.add_value('reactions', s.split('total_count=')[-1].split('&')[0])
        else:
            logging.info("============= nonetype ==============")
            l.add_value('reactions', 0)
        s = response.xpath("//a[contains(@href,'reaction_type=1')]/@href").get()
        # logging.info("============= {} ==============".format())
        if s is not None:
            l.add_value('like', s.split('total_count=')[-1].split('&')[0])
        else:
            l.add_value('like', 0)


        return l.load_item()
