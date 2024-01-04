# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from w3lib.html import remove_tags
import scrapy


class Zajecia(scrapy.Item):
    date = scrapy.Field()
    nr = scrapy.Field()
    short = scrapy.Field()
    id_prow = scrapy.Field()
    group = scrapy.Field()
    full = scrapy.Field()
