from scrapy.item import Item, Field


class WaralbumPost(Item):
    post_link = Field()
    images = Field()
    description = Field()
    timestamp = Field()
    local_images = Field()
    images_binary = Field()