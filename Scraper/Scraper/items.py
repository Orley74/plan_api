# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Lesson(scrapy.Item):
    date = scrapy.Field()
    blok = scrapy.Field()
    id_prow = scrapy.Field()
    group = scrapy.Field()
    short = scrapy.Field()
    form = scrapy.Field()
    place = scrapy.Field()
    nr_zajec = scrapy.Field()
    full = scrapy.Field()
