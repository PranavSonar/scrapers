# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class UniquefitnessItem(Item):
    productname = Field()
    imgurl = Field()
    description = Field()
    pass
