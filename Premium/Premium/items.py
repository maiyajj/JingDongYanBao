# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PremiumItem(scrapy.Item):
    # define the fields for your item here like:
    origin = scrapy.Field()

    category = scrapy.Field()

    name = scrapy.Field()

    model = scrapy.Field()

    price = scrapy.Field()

    premium = scrapy.Field()

    url = scrapy.Field()

    name_id = scrapy.Field()

    other = scrapy.Field()
