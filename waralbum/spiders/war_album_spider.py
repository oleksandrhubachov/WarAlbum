import urllib
import uuid
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from waralbum.items import WaralbumPost
from waralbum.mongo_checker import MongoChecker


class WarAlbumSpider(CrawlSpider):
    checker = MongoChecker()
    name = 'war'
    description_xpath = '//*[@id="mcont"]/div/div[2]/div[4]/div[{0}]/div[2]/div[1]/text()'
    description_xpath0 = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/div[2]/div[1]/text()'
    image_xpath = '//*[@id="mcont"]/div/div[2]/div[4]/div[{0}]/div[2]/div[2]/div/a/img/@data-src_big'
    image_xpath0 = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/div[2]/div[2]/div/a/img/@data-src_big'
    post_link_xpath0 = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/a/@name'
    post_link_xpath = '//*[@id="mcont"]/div/div[2]/div[4]/div[{0}]/a/@name'
    page_name = 'page{0}.html'
    post_link_prefix = 'http://vk.com/waralbum?w=wall-'
    album_path = 'album'
    photo_name = 'photo{0}.jpg'
    allowed_domains = ['vk.com']
    start_urls = ['https://m.vk.com/waralbum']
    rules = [Rule
             (
                 SgmlLinkExtractor(restrict_xpaths=('//a[@class="show_more"]')),
                 callback='parse_public',
                 follow=True,
             )
    ]
    counter_pages = 1
    counter_posts = 0

    def parse_start_url(self, response):
        hxs = Selector(response)
        self.save_page(response.body)
        return self.parse_posts(5, hxs, self.description_xpath0, self.image_xpath0, self.post_link_xpath0)

    def parse_public(self, response):
        hxs = Selector(response)
        # self.save_page(response.body)
        self.counter_pages += 1
        return self.parse_posts(10, hxs, self.description_xpath, self.image_xpath, self.post_link_xpath)

    def parse_posts(self, amount, selector, description_xpath, image_xpath, post_link_xpath):
        posts = []
        for i in range(1, amount + 1):
            descr = selector.xpath(description_xpath.format(i)).extract()
            image_tmp_url = selector.xpath(image_xpath.format(i)).extract()
            description = ''
            if len(descr) > 0:
                description = descr[0]
            image_urls = []
            for img in image_tmp_url:
                image_urls.append(img.split('|')[0])
            if len(description) == 0 or len(image_urls) == 0:
                break
            post_link = self.post_link_prefix + selector.xpath(post_link_xpath.format(i)).extract()[0].split('-')[1]
            if self.checker.check(post_link):
                raise CloseSpider('Shutdown. New posts: {0}'.format(self.counter_posts))
            local_images = []
            # images_binaries = []
            for url in image_urls:
                photo_file = self.photo_name.format(uuid.uuid4())
                urllib.urlretrieve(url, self.album_path + '/' + photo_file)
                local_images.append(photo_file)
                # images_binaries.append(open(self.album_path + '/' + photo_file, 'r').read())
            post = WaralbumPost()
            post['images'] = image_urls
            post['description'] = description
            post['post_link'] = post_link
            post['local_images'] = local_images
            # post['images_binary'] = images_binaries
            posts.append(post)
            self.counter_posts += 1
            print description
            print image_urls
            print post_link
        return posts

    def save_page(self, content):
        with open(self.page_name.format(self.counter_pages), 'wb') as f:
            f.write(content)