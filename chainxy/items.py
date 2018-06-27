# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):
    item_id = Field()
    item_type = Field()
    name = Field()
    number = Field()
    location = Field()
    building = Field()
    bedroom = Field()
    bathroom = Field()
    size = Field()
    title_deep_number = Field()
    description = Field()
    price = Field()
    date = Field()
    link = Field()
    photo = Field()
