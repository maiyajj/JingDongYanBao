# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .sql import Sql
from Premium.items import PremiumItem

class PremiumPipeline(object):
    sql = Sql()
    def process_item(self, item, spider):
        db = spider.name
        if isinstance(item, PremiumItem):
            name_id = item['name_id']
            origin = item['origin']
            category = item['category']
            name = item['name']
            model = item['model']
            price = item['price']
            premium = item['premium']
            url = item['url']
            other = item['other']
            ret = self.sql.select_name(db, name_id)
            if ret[0] == 1:
                # pass
                self.sql.update_data(db, 'premium', premium, name_id)
            else:
                self.sql.insert_data(db, origin, category, name, model, price, premium, url, name_id)

            if other:
                self.sql.update_special_items(db, url)
        return item
