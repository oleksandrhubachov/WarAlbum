BOT_NAME = 'waralbum'

SPIDER_MODULES = ['waralbum.spiders']
NEWSPIDER_MODULE = 'waralbum.spiders'

ITEM_PIPELINES = ['waralbum.pipelines.WarAlbum',]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "waralbum"
MONGODB_COLLECTION = "waralbum_posts"