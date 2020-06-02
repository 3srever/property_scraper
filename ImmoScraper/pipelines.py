# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from scrapy.exceptions import DropItem

nums = [str(n) for n in range(10)]

def strip_whitespace(d):
    return {
        key: (value.strip() if value is not None else value) for key, value in d.items()
    }

def strip_nums(value):
    clean = ''
    for i in value:
        if i in nums or i == ',':
            clean += i
    return clean

class ImmoscraperPipeline:
    def process_item(self, item, spider):

        temp_dict = strip_whitespace(item)

        if item.get('cold_rent'):
            temp_dict['cold_rent'] = strip_nums(item['cold_rent'])

        if item.get('warm_rent'):
            temp_dict['warm_rent'] = strip_nums(item['warm_rent'])

        if item.get('square_meter'):
            temp_dict['square_meter'] = strip_nums(item['square_meter'])

        if item.get('year_built'):
            if 'unbekannt' in item['year_built']:
                temp_dict['year_built'] = None

        return temp_dict
