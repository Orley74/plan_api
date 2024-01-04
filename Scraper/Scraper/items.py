# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Lesson(scrapy.Item):
    date = scrapy.Field()
    blok = scrapy.Field()
    id_prow = scrapy.Field()
    group = scrapy.Field()
    short = scrapy.Field()
    form = scrapy.Field()
    nr_zajec = scrapy.Field()
    full = scrapy.Field()
