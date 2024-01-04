# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import neo4j
from neo4j import GraphDatabase, RoutingControl, exceptions


class ScrapperPipeline:

    def __init__(self):
        self.uri = 'neo4j+s://b35e138c.databases.neo4j.io'
        self.auth = ("neo4j", 'VGfvQTk0VCkEzne79CGPXTKA_Eykhx0OwudLZUKG7sQ')

   
    def open_spider(self, spider):
        self.driver = GraphDatabase.driver(self.uri,auth=self.auth)

     def close_spider(self, spider):
        self.driver.close()

    def process_item(self, item, spider):
        self.driver.execute_query( "Create (a:asd {ID: $name}) ",
        name=ItemAdapter(item).asdict(),database_="neo4j",
        )
        return item
