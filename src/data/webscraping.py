import scrapy
import os
from tqdm import tqdm

# genres = ['Comedy', 'Drama', 'Romance', 'Action', 'Crime', 'Adventure', 'Family', 'Horror', 'Fantasy', 'Musical', 'Thriller', 'Sci-Fi', 
#        'Music', 'Mystery', 'Animation', 'Documentary']

class IMDBSpider(scrapy.Spider):
    name = 'IMDBSpider'
    genre = 'Drama'
    start_urls = [f'https://www.imdb.com/search/title/?title_type=movie&genres={genre}&sort=num_votes,desc&explore=title_type,genres']
    base_url = 'https://www.imdb.com'

    def parse(self, response):
        max_pages = 1
        page = 0
        while page < max_pages:
            titles = response.xpath("*//div/h3[@class='lister-item-header']/a/text()").getall()
            years = response.xpath("//div/h3/span[@class='lister-item-year text-muted unbold']/text()").getall()
            classifications = response.xpath("//p/span[@class='certificate']/text()").getall()
            durations = response.xpath("//div/p/span[@class='runtime']/text()").getall()
            genres = response.xpath("//div/p/span[@class='genre']/text()").getall()
            ratings = response.xpath("//div[@class='inline-block ratings-imdb-rating']/strong/text()").getall()
            directors_and_stars = response.xpath("//div/p[@class='']").getall()
            gross = response.xpath("//div/p/span[@name='nv']/text()").getall()

            for item in zip(titles, years, classifications, durations, genres, ratings, directors_and_stars, gross):
                yield {
                        'title': item[0],
                        'year': item[1],
                        'classification': item[2],
                        'duration': item[3],
                        'genre': item[4],
                        'rating': item[5],
                        'director_and_stars': item[6],
                        'gross': item[7]
                    }
                    
            next_page_partial_url = response.xpath('//div/a[@class="lister-page-next next-page"]/@href').get()
            print(next_page_partial_url)
            next_page_url = self.base_url + next_page_partial_url
            start_urls = [next_page_url]
            page += 1