import scrapy
import neo4j
from neo4j import GraphDatabase, RoutingControl, exceptions
from scrapy.loader import ItemLoader
from ..items import Zajecia


class LessonsSpider(scrapy.Spider):
    name = 'lessons'
    group = str()
    def parse(self, response):
        lessons = response.xpath('//div[@class="lesson"]')


        for lesson in lessons:
            l = ItemLoader(item=Zajecia(), response=lesson)
            # date = lesson.xpath('.//span[@class="date"]/text()').get()
            # name = lesson.xpath('.//span[@class="name"]/text()').getall()
            # full = lesson.xpath('.//span[@class="info"]/text()').get()
            # instructor = lesson.xpath('.//span[@class="sSkrotProwadzacego"]/text()').get()
            # block = lesson.xpath('.//span[@class="block_id"]/text()').get()[-1:]
            l.add_xpath('date', './/span[@class="date"]/text()')
            l.add_xpath('nr', './/span[@class="block_id"]/text()')
            l.add_xpath('short', './/span[@class="name"]/text()')
            l.add_xpath('id_prow', './/span[@class="sSkrotProwadzacego"]/text()')
            l.add_value('group',self.group)
            l.add_xpath('full', './/span[@class="info"]/text()')
            
            yield l.load_item()