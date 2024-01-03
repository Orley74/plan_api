import scrapy
import neo4j
from neo4j import GraphDatabase, RoutingControl, exceptions

class LessonsSpider(scrapy.Spider):
    name = 'lessons'

    def parse(self, response):
        lessons = response.xpath('//div[@class="lesson"]')

        for lesson in lessons:
            date = lesson.xpath('.//span[@class="date"]/text()').get()
            name = lesson.xpath('.//span[@class="name"]/text()').getall()
            full = lesson.xpath('.//span[@class="info"]/text()').get()
            instructor = lesson.xpath('.//span[@class="sSkrotProwadzacego"]/text()').get()
            block = lesson.xpath('.//span[@class="block_id"]/text()').get()[-1:]

            yield {
                'date': date,
                    'blok': block,
                        'short': name,
                        'instructor': instructor,
                        'full': full
            }