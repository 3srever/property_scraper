# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from scrapy.exceptions import DropItem

# def strip_whitespace(d):
#     return {
#         key: value.strip() for key, value in d.items() if value != None
#     }
#
#
# def strip_rest(value):
#     if value != None:
#         clean = ''
#         for i in range(len(value)):
#             if value[i] in [n for n in range(10)] or value[i] == ',':
#                 clean += value[i]
#             else:
#                 continue
#         return clean

class ImmoscraperPipeline:
    def process_item(self, item, spider):
        pass

        # strip_whitespace(item)
        #
        # if item.get('cold_rent'):
        #     item['cold_rent'] = strip_rest(item['cold_rent'])
        #
        # if item.get('warm_rent'):
        #     item['warm_rent'] = strip_rest(item['warm_rent'])
        #
        # if item.get('square_meter'):
        #     item['square_meter'] = strip_rest(item['square_meter'])
        #
        # if item.get('floor'):
        #     if 'von' in item['floor']:
        #         item['floor'] = item['floor'][0]
        #
        # if item.get('year_built'):
        #     if 'unbekannt' in item['year_built']:
        #         item['year_built'] = None
        #
        # if item.get('object_condition'):
        #     if item['object_condition'] in ['Renovierungsbedürftig', 'Nach Vereinbarung']:
        #         item['object_condition'] = '0'
        #     else:
        #         item['object_condition'] = '1'
        #
        # if item.get('heating_type'):
        #     if item['heating_type'] in ['Solar-Heizung']:
        #         item['heating_type'] = '2'
        #     else:
        #         item['heating_type'] = '1'
        #
        # if item.get('pets_allowed'):
        #     if item['pets_allowed'] == 'Ja':
        #         item['heating_type'] = '1'
        #     else:
        #         item['heating_type'] = '0'
        #
        # if item.get('has_parking'):
        #     if 'arage' in item['has_parking']:
        #         item['has_parking'] = '2'
        #     else:
        #         item['has_parking'] = '1'
