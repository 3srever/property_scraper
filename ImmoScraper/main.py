from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

script = CrawlerProcess(get_project_settings())
script.crawl('fairly')
script.start()
