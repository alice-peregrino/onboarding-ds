import scrapy
import os
from tqdm import tqdm

# drama, action, family, crime
class IMDBSpider(scrapy.Spider):
    ## identifies the spider
    name = 'IMDBSpider' 
    genre = 'Crime'
    start_urls = [f'https://www.imdb.com/search/title/?title_type=movie&genres={genre}&sort=num_votes,desc&explore=title_type,genres']
    base_url = 'https://www.imdb.com'

    def parse(self, response):
        """
        Extracts the scraped data as dicts and find new URLS to follow and create new
        requests from them.
        """
        max_pages = 60
        page = 0

        while page < max_pages:
            next_page = True
            iterator = response.xpath('//div[@class="lister-item mode-advanced"]')
            for r in iterator:
                yield {
                    'title': r.xpath(".//h3[@class='lister-item-header']/a/text()").get(),
                    'year': r.xpath(".//h3/span[@class='lister-item-year text-muted unbold']/text()").get(),
                    'classification': r.xpath(".//p/span[@class='certificate']/text()").get(),
                    'duration': r.xpath(".//span[@class='runtime']/text()").get(),
                    'genre': r.xpath(".//p/span[@class='genre']/text()").get(),
                    'rating': r.xpath(".//div[@class='inline-block ratings-imdb-rating']/strong/text()").get(),
                    'directors': r.xpath(".//p[@class='']").get().split('|')[0],
                    'stars': r.xpath(".//p[@class='']").get().split('|')[1],
                    'gross': r.xpath(".//p/span[@name='nv']/text()").get()
                }

            if next_page:
                next_page_partial_url = response.xpath('//div/a[@class="lister-page-next next-page"]/@href').get()
                next_page_url = self.base_url + next_page_partial_url
                # start_urls = [next_page_url]
                request = scrapy.Request(url=next_page_url)
                yield request
                page += 1
