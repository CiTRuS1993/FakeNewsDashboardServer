import scrapy
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess


class TestScrapySnops(scrapy.Spider):
    name = "snops_spider"

    start_urls = ['https://www.snopes.com/fact-check']
    pass

    def parse(self, response):
        LINK_SELECTOR = '.list-group-item a ::attr(href)'
        for href in response.css(LINK_SELECTOR):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        next_url = response.css('.btn-next ::attr(href)').extract_first()
        yield scrapy.Request(next_url, callback=self.parse)

    def parse_dir_contents(self, response):
        TITLE_SELECTOR = '.card-title ::text'
        CATERGORY_SELECTOR = '.breadcrumb-item a ::text'
        CLAIM_SELECTOR = '.claim-text ::text'
        r = response.css(CATERGORY_SELECTOR)
        RATING_SELECTOR = '.h3 ::text'
        DATE_SELECTOR = '.date-published ::text'
        t = {
            'title': response.css(TITLE_SELECTOR).extract_first(),
            'claim': response.css(CLAIM_SELECTOR).extract_first().replace('\n', '').replace('\t', ''),
            'main-category': response.css(CATERGORY_SELECTOR)[0].extract(),
            'sub-category': response.css(CATERGORY_SELECTOR)[1].extract(),
            'rating': response.css(RATING_SELECTOR).extract_first(),
            'date': response.css(DATE_SELECTOR).extract_first(),
            'ur;': response.request.url,
        }
        yield t


if __name__ == '__main__':
    # process = CrawlerProcess()
    # process.crawl(TestScrapySnops)
    # x = process.start()
    # print("")
    cmdline.execute('scrapy runspider scrapy_snopes.py -o snopes.csv -t csv --nolog'.split())
    print("")
