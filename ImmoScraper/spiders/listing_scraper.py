from datetime import date
import pandas as pd
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

pd.set_option('display.max_columns', None)
df = pd.read_csv(r'C:\Users\stefa\PycharmProjects\ImmoScraper\ImmoScraper\listing_data.csv')

# takes a csv of expose IDs and scrapes the requested data
# filters out unique IDs first, to avoid double scraping
# outputs a new CSV with all listing data
# run with: scrapy crawl fairly

# fix no address given

today = date.today()
today = today.strftime("%d/%m/%Y")

city = 'berlin'
geocodes = [
    "1276003001054",  # pberg
    "1276003001017",  # fhain
    "1276003001048",  # nk
    "1276003001034",  # xberg
    "1276003001046",  # mitte
    "1276003001073",  # wedding
    "1276003001068"   # moabit
]

http = 'https://www.'
base_url = 'immobilienscout24.de'
search_url = f"/Suche/de/{city}/{city}/wohnung-mieten?geocodes={','.join(geocodes)}"

x_paths = {
    'listing_type': '//a[@class="breadcrumb__link"]/text()',
    'expose_url': '//head/link[@rel="canonical"]/@href',
    'title': '//div[@class="criteriagroup "]/h1/text()',
    'street': '//div[@class="address-block"]/div/span[@class="block font-nowrap print-hide"]/text()',
    'zipcode': '//div[@class="address-block"]/div/span[@class="zip-region-and-country"]/text()',
    'cold_rent': '//div[@class="is24qa-kaltmiete is24-value font-semibold is24-preis-value"]/text()',
    'warm_rent': '//dd[@class="is24qa-gesamtmiete grid-item three-fifths font-bold"]/text()',
    'rooms': '//div[@class="is24qa-zi is24-value font-semibold"]/text()',
    'square_meter': '//div[@class="is24qa-flaeche is24-value font-semibold"]/text()',
    'house_type': '//dd[@class="is24qa-typ grid-item three-fifths"]/text()',
    'floor': '//dd[@class="is24qa-etage grid-item three-fifths"]/text()',
    'year_built': '//dd[@class="is24qa-baujahr grid-item three-fifths"]/text()',
    'object_condition': '//dd[@class="is24qa-objektzustand grid-item three-fifths"]/text()',
    'heating_type': '//dd[@class="is24qa-heizungsart grid-item three-fifths"]/text()',
    'pets_allowed': '//dd[@class="is24qa-haustiere grid-item three-fifths"]/text()',
    'has_parking': '//dd[@class="is24qa-garage-stellplatz grid-item three-fifths"]/text()'
}

class ExposeSpider(CrawlSpider):
    name = 'fairly'
    allowed_domains = [base_url]
    start_urls = [f'{http}{base_url}{search_url}']
    rules = [
        Rule(
            LinkExtractor(
                restrict_xpaths='//a[@class="icon-arrow-forward"]'
            ),
            callback='parse_search_pages',
            follow=True
        )
    ]

    def parse_search_pages(self, response):
        url_list = response.xpath('//a[@class="result-list-entry__brand-logo-container"]/@href').getall()
        for item in url_list:
            full_url = f'{http}{base_url}{item}'
            exists = df['expose_url'].str.contains(item).any()
            if 'neubau' not in item and not exists:
                yield scrapy.Request(full_url, callback=self.parse_listing)

    def parse_listing(self, response):
        temp_dict = {
            'date_scraped': today
        }
        for var in x_paths.keys():
            if response.xpath(x_paths[var]):
                temp_dict[var] = response.xpath(x_paths[var]).extract_first()
            else:
                temp_dict[var] = None
        yield temp_dict

    parse_start_url = parse_search_pages

