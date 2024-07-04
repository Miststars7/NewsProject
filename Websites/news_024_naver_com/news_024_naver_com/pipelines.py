# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class News024NaverComPipeline:

    def __init__(self):
        super().__init__()
        # 链接数据库
        if settings['CURRENT_ENVIRONMENT'] == 'live':
            uri = 'mongodb://{0}:{1}@{2}:{3}'.format(settings['MONGO_USER'], settings['MONGO_PASSWORD'], settings['MONGO_HOST'], settings['MONGO_PORT'])
        else:
            uri = 'mongodb://{0}:{1}/{2}'.format(settings['MONGO_HOST'], settings['MONGO_PORT'], settings['MONGO_DB'])
        client = pymongo.MongoClient(uri)
        self.db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        news_item = dict(item)
        self.coll.insert_one(news_item)
        # return item
