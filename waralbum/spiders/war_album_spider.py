from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.selector import Selector


class WarAlbumSpider(CrawlSpider):
    name = 'war'
    description_xpath = '//*[@id="mcont"]/div/div[2]/div[4]/div[{0}]/div[2]/div[1]/text()'
    image_xpath = '//*[@id="mcont"]/div/div[2]/div[4]/div[{0}]/div[2]/div[2]/div/a/img/@data-src_big'
    page_name = 'page{0}.html'
    allowed_domains = ['vk.com']
    start_urls = ['https://m.vk.com/waralbum?offset=0&own=1']
    rules = [Rule
             (
                 SgmlLinkExtractor(restrict_xpaths=('//a[@class="show_more"]')),
                 callback='parse_public',
                 follow=True,
             )
    ]
    counter = 1

    def parse_public(self, response):
        hxs = Selector(response)
        # self.save_page(response.body)
        self.counter += 1
        for i in range(1, 11):
            description = hxs.xpath(self.description_xpath.format(i)).extract()[0]
            image_tmp_url = hxs.xpath(self.image_xpath.format(i)).extract()
            image_urls = []
            for i in image_tmp_url:
                image_urls.append(i.split('|')[0])
            print description
            print image_urls
            # with open("1.txt", 'wb') as f:
            #     f.write(repr(description))
            # break



    def save_page(self, content):
        with open(self.page_name.format(self.counter), 'wb') as f:
            f.write(content)