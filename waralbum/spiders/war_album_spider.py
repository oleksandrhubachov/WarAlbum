from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.selector import Selector


class WarAlbumSpider(CrawlSpider):
    name = 'war'
    description_xpath = '//*[@id="mcont"]/div/div[2]/div[4]/div[{0}]/div[2]/div[1]/text()'
    description_xpath0 = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/div[2]/div[1]/text()'
    image_xpath = '//*[@id="mcont"]/div/div[2]/div[4]/div[{0}]/div[2]/div[2]/div/a/img/@data-src_big'
    image_xpath0 = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/div[2]/div[2]/div/a/img/@data-src_big'
    page_name = 'page{0}.html'
    allowed_domains = ['vk.com']
    start_urls = ['https://m.vk.com/waralbum']
    rules = [Rule
             (
                 SgmlLinkExtractor(restrict_xpaths=('//a[@class="show_more"]')),
                 callback='parse_public',
                 follow=True,
             )
    ]
    counter = 1

    def parse_start_url(self, response):
        hxs = Selector(response)
        self.save_page(response.body)
        self.parse_posts(5, hxs, self.description_xpath0, self.image_xpath0)

    def parse_public(self, response):
        hxs = Selector(response)
        # self.save_page(response.body)
        self.counter += 1
        self.parse_posts(10, hxs, self.description_xpath, self.image_xpath)

    def parse_posts(self, amount, selector, description_xpath, image_xpath):
        for i in range(1, amount+1):
            descr = selector.xpath(description_xpath.format(i)).extract()
            image_tmp_url = selector.xpath(image_xpath.format(i)).extract()
            description = ''
            if len(descr) > 0:
                description = descr[0]
            image_urls = []
            for img in image_tmp_url:
                image_urls.append(img.split('|')[0])
            if len(description) > 0 and len(image_urls) > 0:
                print description
                print image_urls

    def save_page(self, content):
        with open(self.page_name.format(self.counter), 'wb') as f:
            f.write(content)