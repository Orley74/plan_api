# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import neo4j
from neo4j import GraphDatabase, RoutingControl, exceptions

from itemadapter import ItemAdapter


class JsonWriterPipeline:
    uri = 'neo4j+s://b35e138c.databases.neo4j.io'
    auth = ("neo4j", 'VGfvQTk0VCkEzne79CGPXTKA_Eykhx0OwudLZUKG7sQ')

    def open_spider(self, spider):
        self.driver = GraphDatabase.driver(self.uri, auth= self.auth)


    def close_spider(self, spider):
        self.driver.close()
    

    def process_item(self, item, spider):
      
        self.driver.execute_query(
        "Create (p:asdasd) ",
        database_="neo4j")
        # line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        # print(line)
        return item



# class JsonWriterPipeline:
#     def open_spider(self, spider):
#         self.file = open("items.jsonl", "w")

#     def close_spider(self, spider):
#         self.file.close()

#     def process_item(self, item, spider):
#         line = json.dumps(ItemAdapter(item).asdict()) + "\n"
#         self.file.write(line)
#         return item