import scrapy
from scrapy import Selector


class PetMarketSpider(scrapy.Spider):
    name = "odissey"
    fields = {
        'product': '//div[@id="spec_prod"]',
        'price': '//div[@class="pprice"]/text()',
        'name': '//a[@class="pnameh"]/text()',
        'img': '//a[@class="relativehome"]/img/@src',
        'product_link': '//a[@class="pnameh"]/@href'
    }
    start_urls = [
        'https://odissey.kiev.ua/'
    ]
    allowed_domains = [
        'odissey.kiev.ua'
    ]
    items_number = 20

    def parse(self, response):
        for product in response.xpath(self.fields["product"]).getall()[:self.items_number]:
            selector = Selector(text=product)
            yield {
                'link': selector.xpath(self.fields['product_link']).extract(),
                'price': selector.xpath(self.fields['price']).get().strip(),
                'img': selector.xpath(self.fields['img']).extract(),
                'name': ''.join(selector.xpath(self.fields['name']).extract())
            }
