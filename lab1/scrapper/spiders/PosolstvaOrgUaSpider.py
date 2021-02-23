import scrapy


def isNotEmptyString(str):
    return len(str) > 0


class PosolstvaOrgUaSpider(scrapy.Spider):
    name = "posolstva"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapper.pipelines.NewsXmlPipeline': 300,
        }
    }
    fields = {
        'img': '//img/@src',
        'text': '//*[not(self::script)]/text()',
        'link': '//a/@href'
    }
    start_urls = [
        'http://www.posolstva.org.ua'
    ]
    allowed_domains = [
        'posolstva.org.ua'
    ]
    pages_read = 0

    def parse(self, response):
        text = filter(isNotEmptyString,
                      map(lambda str: str.strip(),
                          [text.extract() for text in response.xpath(self.fields["text"])]))
        images = map(lambda url: ((response.url + url) if url.startswith('/') else url),
                     [img_url.extract() for img_url in response.xpath(self.fields["img"])])
        yield {
            'text': text,
            'images': images,
            'url': response.url
        }
        for link_url in response.css("li.pager-next a").xpath(self.fields['link']):
            if self.pages_read > 20:
                return
            self.pages_read += 1
            print("url and page num: ", link_url, "|", self.pages_read)

            yield response.follow(link_url.extract(), callback=self.parse)
