from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    script = CrawlerProcess(get_project_settings())
    script.crawl('immoscout')
    script.start()