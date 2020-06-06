import re

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from scrapy.exceptions import DropItem

nums = [str(n) for n in range(10)]
pattern = r'^\d{1,5}.?\d{0,2}$'

def strip_whitespace(d):
    return {
        key: (value.strip() if value is not None else value) for key, value in d.items()
    }

def strip_currency(value):
    clean = ''
    for i in value:
        if i in nums or i == ',':
            clean += i
    clean = clean.replace(',', '.')
    return clean

def strip_deposit(value):
    reverse = value[::-1]
    clean = ''
    separator = True
    for i in reverse:
        if i in nums:
            clean += i
        elif i == ',' or i == '.' and separator:
            separator = False
            clean += i
    clean = clean.replace(',', '.')
    return clean[::-1]

class ImmoscoutPipeline:
    def process_item(self, item, spider):

        temp_dict = strip_whitespace(item)

        if item.get('cold_rent'):
            temp_dict['cold_rent'] = strip_currency(item['cold_rent'])

        if item.get('warm_rent'):
            temp_dict['warm_rent'] = strip_currency(item['warm_rent'])

        if item.get('square_meter'):
            temp_dict['square_meter'] = strip_currency(item['square_meter'])

        if item.get('year_built'):
            if 'unbekannt' in item['year_built']:
                temp_dict['year_built'] = None

        if item.get('parking_rent'):
            temp_dict['parking_rent'] = strip_currency(item['parking_rent'])

        if item.get('floor'):
            if 'von' in item['floor']:
                temp_dict['floor'] = temp_dict['floor'][0]

        if item.get('rooms'):
            temp_dict['rooms'] = temp_dict['rooms'].replace(',', '.')

        if item.get('deposit'):
            deposit = strip_deposit(item['deposit'])
            match = re.match(pattern, deposit)
            if match and (len(item['deposit']) < 25) and ('-' not in item['deposit']):
                if len(deposit) <= 3:
                    temp_dict['deposit'] = str(
                        round(
                            (float(deposit) * float(temp_dict['cold_rent'])),
                            2
                        )
                    )
                else:
                    temp_dict['deposit'] = deposit
            else:
                temp_dict['deposit'] = None

        return temp_dict