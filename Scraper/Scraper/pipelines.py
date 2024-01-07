# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("items.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        uri = 'neo4j+s://b35e138c.databases.neo4j.io'
        auth = ("neo4j", 'VGfvQTk0VCkEzne79CGPXTKA_Eykhx0OwudLZUKG7sQ')
        with GraphDatabase.driver(uri,auth=auth) as bd:
                # add_date(bd,resoult,user_group)
                
                driver.execute_query(
                "Create (p:asdasd {a:a}) ",
                database_="neo4j")
        # line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        # self.file.write("xd")

        return item
