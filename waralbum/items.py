from scrapy.item import Item, Field


class WaralbumPost(Item):
    post_link = Field()
    img_links = Field()
    description = Field()
    local_images = Field()
    data_chunk_id = Field()