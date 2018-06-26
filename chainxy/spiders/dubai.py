# -*- coding: utf-8 -*-
import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
import re
from PIL import Image
import base64
import pytesseract
import cStringIO



class DubaiSpider(scrapy.Spider):
    name = 'dubai'
    start_urls = ['https://dubai.dubizzle.com/en/property-for-sale/residential/?filters=(listed_by.value%3A"LA")']
    request_urls = ['https://qbfzmmnba6-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.29.0%3BJS%20Helper%202.19.0&x-algolia-application-id=QBFZMMNBA6&x-algolia-api-key=$$api_key$$', 'https://qbfzmmnba6-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.29.0%3BJS%20Helper%202.19.0&x-algolia-application-id=QBFZMMNBA6&x-algolia-api-key=$$api_key$$']
    base_url = "https://dubai.dubizzle.com"

    params = [{"requests":[{"indexName":"property-for-rent-residential.com","params":"facets=%5B%22furnished%22%2C%22language%22%2C%22listed_by.value%22%2C%22agent.name.en%22%2C%22property_reference%22%5D&page=1&hitsPerPage=500&filters=(city.id%3D2)%20AND%20(categories.ids%3D1743)%20AND%20(listed_by.value%3A%22LA%22)&attributesToRetrieve=%5B%22_geoloc%22%2C%22360_tour%22%2C%22absolute_url%22%2C%22active%22%2C%22added%22%2C%22agent%22%2C%22amenities%22%2C%22bathrooms%22%2C%22bedrooms%22%2C%22building%22%2C%22categories%22%2C%22category_id%22%2C%22city%22%2C%22feed_id%22%2C%22furnished%22%2C%22highlighted_ad%22%2C%22id%22%2C%22landmarks%22%2C%22language%22%2C%22listed_by%22%2C%22name.en%22%2C%22neighborhoods%22%2C%22objectID%22%2C%22photo%22%2C%22photos_count%22%2C%22price%22%2C%22promoted%22%2C%22property_reference%22%2C%22rent_is_paid%22%2C%22size%22%2C%22uri%22%2C%22user_id%22%2C%22is_verified%22%5D&attributesToHighlight=%5B%5D"},{"indexName":"property-for-rent-residential.com","params":"facets=%5B%22furnished%22%2C%22language%22%2C%22listed_by.value%22%2C%22agent.name.en%22%2C%22property_reference%22%5D&hitsPerPage=1000&filters=(city.id%3D2)%20AND%20(categories.ids%3D1743)%20AND%20(listed_by.value%3A%22LA%22)%20AND%20(promoted%3A%22true%22)&attributesToRetrieve=%5B%22objectID%22%5D&attributesToHighlight=%5B%5D"},{"indexName":"property-for-rent-residential.com","params":"facets=%5B%22furnished%22%2C%22language%22%2C%22listed_by.value%22%2C%22agent.name.en%22%2C%22property_reference%22%5D&hitsPerPage=1000&filters=(city.id%3D2)%20AND%20(categories.ids%3D1743)%20AND%20(listed_by.value%3A%22LA%22)%20AND%20(featured_listing%3A%22true%22)&attributesToRetrieve=%5B%22objectID%22%5D&attributesToHighlight=%5B%5D"}]}, {"requests":[{"indexName":"property-for-sale-residential.com","params":"facets=%5B%22language%22%2C%22is_verified%22%2C%22listed_by.value%22%2C%22agent.name.en%22%2C%22property_reference%22%5D&page=1&hitsPerPage=300&filters=(city.id%3D2)%20AND%20(categories.ids%3D1742)%20AND%20(listed_by.value%3A%22LA%22)&attributesToRetrieve=%5B%22_geoloc%22%2C%22360_tour%22%2C%22absolute_url%22%2C%22active%22%2C%22added%22%2C%22agent%22%2C%22amenities%22%2C%22bathrooms%22%2C%22bedrooms%22%2C%22building%22%2C%22categories%22%2C%22category_id%22%2C%22city%22%2C%22feed_id%22%2C%22furnished%22%2C%22highlighted_ad%22%2C%22id%22%2C%22landmarks%22%2C%22language%22%2C%22listed_by%22%2C%22name.en%22%2C%22neighborhoods%22%2C%22objectID%22%2C%22photo%22%2C%22photos_count%22%2C%22price%22%2C%22promoted%22%2C%22property_reference%22%2C%22rent_is_paid%22%2C%22size%22%2C%22uri%22%2C%22user_id%22%2C%22is_verified%22%5D&attributesToHighlight=%5B%5D"},{"indexName":"property-for-sale-residential.com","params":"facets=%5B%22language%22%2C%22is_verified%22%2C%22listed_by.value%22%2C%22agent.name.en%22%2C%22property_reference%22%5D&hitsPerPage=1000&filters=(city.id%3D2)%20AND%20(categories.ids%3D1742)%20AND%20(listed_by.value%3A%22LA%22)%20AND%20(promoted%3A%22true%22)&attributesToRetrieve=%5B%22objectID%22%5D&attributesToHighlight=%5B%5D"},{"indexName":"property-for-sale-residential.com","params":"facets=%5B%22language%22%2C%22is_verified%22%2C%22listed_by.value%22%2C%22agent.name.en%22%2C%22property_reference%22%5D&hitsPerPage=1000&filters=(city.id%3D2)%20AND%20(categories.ids%3D1742)%20AND%20(listed_by.value%3A%22LA%22)%20AND%20(featured_listing%3A%22true%22)&attributesToRetrieve=%5B%22objectID%22%5D&attributesToHighlight=%5B%5D"}]}]


    def parse(self, response):
        body = response.body
        api_key = body[body.find('"apiKey":"')+10: body.find('","locationIndex"')]
        # pdb.set_trace()
        yield Request(url=self.request_urls[0].replace('$$api_key$$', api_key), method='POST', body=json.dumps(self.params[0]), headers={'Content-Type':'application/x-www-form-urlencoded'} , callback=self.parse_list)
        
        yield Request(url=self.request_urls[1].replace('$$api_key$$', api_key), method='POST', body=json.dumps(self.params[1]), headers={'Content-Type':'application/x-www-form-urlencoded'} , callback=self.parse_list)

    def parse_list(self, response):
        data = json.loads(response.body)

        urls = []
        for url in data['results'][0]['hits']:
            # pdb.set_trace()
            name = url['name']['en']
            location = ''
            try:
                location = ', '.join(url['neighborhoods']['name']['en']) + ', ' + url['building']['name']['en']
            except:
                location = ', '.join(url['neighborhoods']['name']['en'])

            yield Request(url=url['absolute_url']['en'], callback=self.parse_row, meta={'name': name, 'location': location, 'row': json.dumps(url)})
            break

    def parse_row(self, response):
        row = json.loads(response.meta['row'])
        item = ChainItem()

        item['name'] = response.meta['name']        
        item['location'] = response.meta['location']
        item['item_id'] = row['id']
        
        try:
            item['building'] = row['building']['name']['en']
        except:
            item['building'] = ''

        item['bedroom'] = row['bedrooms']
        item['bathroom'] = row['bathrooms']
        item['size'] = row['size']
        try:
            item['title_deep_number'] = response.xpath('//div[@class="lister-info"]/strong/text()').extract_first()
        except:
            item['title_deep_number'] = ''

        try:
            item['description'] = ' '.join(response.xpath('//span[@id="description-box"]/text()').extract()).strip()
        except:
            item['description'] = ''
        try:
            item['date'] = response.xpath('//div[@class="posted-on fnt-12-grey"]/text()').extract_first().split(':')[1]
        except:
            item['date'] = ''

        item['link'] = response.xpath('//div[@class="report-ad"]//a/@href').extract_first() 

        if item['link'] == '' or item['link'] is None:
            item['link'] = response.xpath('//div[@id="listing-controls"]//input/@value').extract_first()
        else:
            item['link'] = self.base_url + item['link']

        item['photo'] = ' | '.join(response.xpath('//div[@class="new-property fotorama"]/img/@src').extract())

        try:
            imgstring = response.xpath('//img[@class="phone-num-img"]/@src').extract_first()
            imgstring = imgstring.split('base64,')[-1].strip()
            pic = cStringIO.StringIO()
            image_string = cStringIO.StringIO(base64.b64decode(imgstring))
            image = Image.open(image_string)

            bg = Image.new("RGB", image.size, (255,255,255))
            bg.paste(image,image)

            # pdb.set_trace()
            item['number'] = pytesseract.image_to_string(bg)
        except:
            item['number'] = ''

        yield item
