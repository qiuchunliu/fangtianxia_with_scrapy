# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewhouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    # 小区名字
    name = scrapy.Field()
    price = scrapy.Field()
    # 几居室
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 原始链接
    origin_url = scrapy.Field()


class EsfItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    origin_url = scrapy.Field()
