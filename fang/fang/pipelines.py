# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter


class FangPipeline(object):

    def __init__(self):
        self.newhouse_fp = open('newhouse.json', 'wb')
        self.esfhouse_fp = open('esf.json', 'wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp,
                                                       ensure_ascii=False
                                                       )
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp,
                                                       ensure_ascii=False
                                                       )

    def process_item(self, item, spider):
        if 'esf' not in item['origin_url']:
            self.newhouse_exporter.export_item(item)
        else:
            self.esfhouse_exporter.export_item(item)
        # 都是导入的item 所以需要判断一下，是要导入到newhouse还是esfhouse
        return item

    def close_spider(self):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()
