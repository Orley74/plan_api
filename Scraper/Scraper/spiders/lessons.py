import scrapy
from scrapy.loader import ItemLoader
from ..items import Lesson

class LessonsSpider(scrapy.Spider):
    name = 'lessons'
    group = str()
    def parse(self, response):
        lessons = response.xpath('//div[@class="lesson"]')
        group = str()
        for lesson in lessons:
            date = lesson.xpath('.//span[@class="date"]/text()').get()
            name = lesson.xpath('.//span[@class="name"]/text()').getall()
            full = lesson.xpath('.//span[@class="info"]/text()').get()
            id_prow = lesson.xpath('.//span[@class="sSkrotProwadzacego"]/text()').get()
            block = lesson.xpath('.//span[@class="block_id"]/text()').get()[-1:]
            short = name[0]
            form = name[1]
            place = name[2]
            nr_zajec = name[3].split('[')[1][:-1]

            l = ItemLoader(Lesson())
            l.add_value("date", date)
            l.add_value("block", block)
            l.add_value("id_prow", id_prow)
            l.add_value("group", group)
            l.add_value("short", short)
            l.add_value("form", form)
            l.add_value("nr_zajec", nr_zajec)
            l.add_value("full", full)
            self.log(f'Item values: {l.load_item()}')

            yield l.load_item()
        