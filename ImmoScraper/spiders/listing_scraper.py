from time import sleep
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd

#takes a csv of expose IDs and scrapes the requested data
#filters out unique IDs first, to avoid double scraping
#outputs a new CSV with all listing data
#run with: scrapy runspider -o listing_data.csv listing_scraper.py

#to do, add item pipeline
#remove headers from output
#remove empty rows from csv

city = 'berlin'
geocodes = [
    "1276003001054", #pberg
    "1276003001017", #fhain
    "1276003001048", #nk
    "1276003001034", #xberg
    "1276003001046", #mitte
    "1276003001073", #wedding
    "1276003001068"  #moabit
]

http = 'https://www.'
base_url = 'immobilienscout24.de'
expose_url = '/expose'
search_url = f"/Suche/de/{city}/{city}/wohnung-mieten?geocodes={','.join(geocodes)}"


# expose_ids = pd.read_csv('../../data/expose_ids.csv')
# expose_ids = expose_ids.drop_duplicates()
# expose_ids['expose_url'] = expose_ids.agg(lambda x: f"{expose_addon}/{x['expose_id']}", axis=1)
#
# listing_ids = pd.read_csv('../../data/listing_data.csv')
# grouped = pd.concat([expose_ids,listing_ids], axis=0, ignore_index=True)
#
# sorted = grouped.sort_values('cold_rent')
# cleaned = sorted.drop_duplicates(subset="expose_url")
# to_scrape = cleaned[(cleaned.cold_rent.isnull() == True)].reset_index()

x_paths = {
    'expose_url': '//head/link[@rel="canonical"]/@href',
    'title': '//div[@class="criteriagroup "]/h1/text()', #.replace(",", "")
    'street': '//div[@class="address-block"]/div/span[@class="block font-nowrap print-hide"]/text()', #[1:-1].replace(",", "")
    'zipcode': '//div[@class="address-block"]/div/span[@class="zip-region-and-country"]/text()', #.replace(",", "")
    'cold_rent': '//div[@class="is24qa-kaltmiete is24-value font-semibold is24-preis-value"]/text()', #[1:-3].replace(".", "").replace(",", ".")
    'warm_rent': '//dd[@class="is24qa-gesamtmiete grid-item three-fifths font-bold"]/text()', #[1:-3].replace(".", "").replace(",", ".")
    'rooms': '//div[@class="is24qa-zi is24-value font-semibold"]/text()', #[1:-1]
    'square_meter': '//div[@class="is24qa-flaeche is24-value font-semibold"]/text()', #[1:-4].replace(",", ".")
    'house_type': '//dd[@class="is24qa-typ grid-item three-fifths"]/text()', #[1:-1].replace(",", "")
    'floor': '//dd[@class="is24qa-etage grid-item three-fifths"]/text()', #[1:2]
    'year_built': '//dd[@class="is24qa-baujahr grid-item three-fifths"]/text()',
    'object_condition': '//dd[@class="is24qa-objektzustand grid-item three-fifths"]/text()', #[1:-1].replace(",", "")
    'heating_type': '//dd[@class="is24qa-heizungsart grid-item three-fifths"]/text()', #[1:-1].replace(",", "")
    'pets_allowed': '//dd[@class="is24qa-haustiere grid-item three-fifths"]/text()', #[1:-1].replace(",", "")
    'has_parking': '//dd[@class="is24qa-garage-stellplatz grid-item three-fifths"]/text()' #[1:-1].replace(",", "")
}

class ExposeSpider(CrawlSpider):
    name = 'fairly'
    allowed_domains = [base_url]
    start_urls = [http + base_url + search_url]
    print(f"Running 'fairly' on {start_urls}")
    rules = [
        Rule(
            LinkExtractor(
                allow='/expose/',
                restrict_xpaths='//a[@class="result-list-entry__brand-logo-container"]'
            ),
            follow=True,
            callback='parse_listing'
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//a[@class="icon-arrow-forward"]'),
            follow=True
        )
    ]

    def parse_listing(self, response):
        temp_dict = {}
        for var in x_paths.keys():
            temp_dict[var] = response.xpath(x_paths[var]).extract_first()
        yield temp_dict