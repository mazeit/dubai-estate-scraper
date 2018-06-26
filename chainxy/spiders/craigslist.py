import scrapy
import json
import requests
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

from chainxy.items import ChainItem
import pdb
from lxml import etree

class CraigslistSpider(scrapy.Spider):
    name = "crag"
    uid_list = []
    proxy_url = 'http://falcon.proxyrotator.com:51337/proxy-list/'
    params = dict(
        apiKey='vCDnEaRTrgq2czLQMJkVo7ubUA8fHtWe'       
    )
    proxy_list = []
    count = 0
    ind = 0

    request_urls = ['https://tampa.craigslist.org/search/cta?&sort=date&nearbyArea=125&nearbyArea=186&nearbyArea=20&nearbyArea=205&nearbyArea=219&nearbyArea=237&nearbyArea=238&nearbyArea=330&nearbyArea=331&nearbyArea=332&nearbyArea=333&nearbyArea=353&nearbyArea=376&nearbyArea=39&nearbyArea=427&nearbyArea=467&nearbyArea=557&nearbyArea=562&nearbyArea=570&nearbyArea=635&nearbyArea=637&nearbyArea=638&nearbyArea=639&nearbyArea=80&searchNearby=2&srchType=T', 'https://richmond.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=460&nearbyArea=34&nearbyArea=290&nearbyArea=705&nearbyArea=367&nearbyArea=193&nearbyArea=335&nearbyArea=444&nearbyArea=328&nearbyArea=273&nearbyArea=633&nearbyArea=457&nearbyArea=61&nearbyArea=166&nearbyArea=447&nearbyArea=279&nearbyArea=366&nearbyArea=291&nearbyArea=48&nearbyArea=336&nearbyArea=36&nearbyArea=289&nearbyArea=286&nearbyArea=556&nearbyArea=10&nearbyArea=194&nearbyArea=329&nearbyArea=711&nearbyArea=272&nearbyArea=357', 'https://jackson.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=372&nearbyArea=199&nearbyArea=264&nearbyArea=127&nearbyArea=644&nearbyArea=645&nearbyArea=560&nearbyArea=559&nearbyArea=230&nearbyArea=374&nearbyArea=643&nearbyArea=231&nearbyArea=558&nearbyArea=425&nearbyArea=283&nearbyArea=284&nearbyArea=100&nearbyArea=46&nearbyArea=641&nearbyArea=200&nearbyArea=563&nearbyArea=207&nearbyArea=31&nearbyArea=375&nearbyArea=640&nearbyArea=203&nearbyArea=206&nearbyArea=642&nearbyArea=359&nearbyArea=371', 'https://cincinnati.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=438&nearbyArea=229&nearbyArea=342&nearbyArea=439&nearbyArea=701&nearbyArea=42&nearbyArea=131&nearbyArea=674&nearbyArea=227&nearbyArea=226&nearbyArea=442&nearbyArea=45&nearbyArea=672&nearbyArea=360&nearbyArea=133&nearbyArea=437&nearbyArea=58&nearbyArea=436&nearbyArea=629&nearbyArea=361&nearbyArea=673&nearbyArea=441&nearbyArea=671&nearbyArea=573&nearbyArea=228&nearbyArea=632&nearbyArea=348&nearbyArea=204&nearbyArea=703&nearbyArea=702', 'https://columbia.craigslist.org/search/cta?sort=date&srchType=T&nearbyArea=171&nearbyArea=258&nearbyArea=14&nearbyArea=256&nearbyArea=446&nearbyArea=570&nearbyArea=128&nearbyArea=41&nearbyArea=367&nearbyArea=335&nearbyArea=273&nearbyArea=464&nearbyArea=61&nearbyArea=253&nearbyArea=462&nearbyArea=353&nearbyArea=634&nearbyArea=202&nearbyArea=257&nearbyArea=254&nearbyArea=291&nearbyArea=636&nearbyArea=36&nearbyArea=289&nearbyArea=205&nearbyArea=712&nearbyArea=635&nearbyArea=323&nearbyArea=274&nearbyArea=272&searchNearby=2', 'https://detroit.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=251&nearbyArea=172&nearbyArea=700&nearbyArea=628&nearbyArea=626&nearbyArea=434&nearbyArea=484&nearbyArea=27&nearbyArea=275&nearbyArea=259&nearbyArea=226&nearbyArea=129&nearbyArea=426&nearbyArea=261&nearbyArea=214&nearbyArea=212&nearbyArea=437&nearbyArea=234&nearbyArea=436&nearbyArea=706&nearbyArea=629&nearbyArea=555&nearbyArea=260&nearbyArea=573&nearbyArea=486&nearbyArea=627&nearbyArea=204&nearbyArea=703&nearbyArea=235&nearbyArea=252', 'https://springfield.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=222&nearbyArea=293&nearbyArea=358&nearbyArea=558&nearbyArea=425&nearbyArea=423&nearbyArea=30&nearbyArea=696&nearbyArea=695&nearbyArea=347&nearbyArea=100&nearbyArea=428&nearbyArea=46&nearbyArea=650&nearbyArea=54&nearbyArea=690&nearbyArea=691&nearbyArea=689&nearbyArea=566&nearbyArea=345&nearbyArea=225&nearbyArea=694&nearbyArea=29&nearbyArea=433&nearbyArea=359&nearbyArea=280&nearbyArea=70&nearbyArea=697&nearbyArea=377&nearbyArea=99', 'https://sanantonio.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=364&nearbyArea=15&nearbyArea=264&nearbyArea=266&nearbyArea=326&nearbyArea=265&nearbyArea=21&nearbyArea=645&nearbyArea=647&nearbyArea=470&nearbyArea=23&nearbyArea=327&nearbyArea=271&nearbyArea=263&nearbyArea=408&nearbyArea=268&nearbyArea=646&nearbyArea=449&nearbyArea=648&nearbyArea=308&nearbyArea=564&nearbyArea=270&nearbyArea=365', 'https://albuquerque.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=269&nearbyArea=511&nearbyArea=653&nearbyArea=210&nearbyArea=132&nearbyArea=568&nearbyArea=244&nearbyArea=288&nearbyArea=334&nearbyArea=267&nearbyArea=315&nearbyArea=420&nearbyArea=218&nearbyArea=651&nearbyArea=320', 'https://denver.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=319&nearbyArea=210&nearbyArea=713&nearbyArea=568&nearbyArea=287&nearbyArea=288&nearbyArea=668&nearbyArea=688&nearbyArea=315&nearbyArea=218&nearbyArea=669&nearbyArea=687&nearbyArea=320&nearbyArea=197', 'https://phoenix.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=244&nearbyArea=506&nearbyArea=455&nearbyArea=26&nearbyArea=565&nearbyArea=209&nearbyArea=419&nearbyArea=8&nearbyArea=651&nearbyArea=468&nearbyArea=352&nearbyArea=57&nearbyArea=370', 'https://ogden.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=52&nearbyArea=424&nearbyArea=652&nearbyArea=288&nearbyArea=448&nearbyArea=292&nearbyArea=56&nearbyArea=352&nearbyArea=469&nearbyArea=320&nearbyArea=197', 'https://fresno.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=373&nearbyArea=709&nearbyArea=104&nearbyArea=26&nearbyArea=7&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=103&nearbyArea=209&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=1&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456', 'https://eugene.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=233&nearbyArea=187&nearbyArea=350&nearbyArea=322&nearbyArea=189&nearbyArea=324&nearbyArea=675&nearbyArea=216&nearbyArea=655&nearbyArea=466&nearbyArea=321&nearbyArea=9&nearbyArea=188&nearbyArea=459&nearbyArea=232&nearbyArea=2&nearbyArea=708&nearbyArea=461&nearbyArea=707&nearbyArea=177&nearbyArea=325&nearbyArea=246', 'https://eastidaho.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=657&nearbyArea=52&nearbyArea=658&nearbyArea=661&nearbyArea=322&nearbyArea=652&nearbyArea=660&nearbyArea=659&nearbyArea=654&nearbyArea=448&nearbyArea=656&nearbyArea=351&nearbyArea=292&nearbyArea=56&nearbyArea=469', 'https://rmn.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=445&nearbyArea=243&nearbyArea=664&nearbyArea=340&nearbyArea=98&nearbyArea=362&nearbyArea=255&nearbyArea=242&nearbyArea=693&nearbyArea=241&nearbyArea=339&nearbyArea=553&nearbyArea=363&nearbyArea=698&nearbyArea=165&nearbyArea=421&nearbyArea=692&nearbyArea=47&nearbyArea=19&nearbyArea=631&nearbyArea=307&nearbyArea=223&nearbyArea=571&nearbyArea=341&nearbyArea=679&nearbyArea=691&nearbyArea=665&nearbyArea=369&nearbyArea=567&nearbyArea=458', 'https://clarksville.craigslist.org/search/cta?sort=date&srchType=T&nearbyArea=127&nearbyArea=229&nearbyArea=342&nearbyArea=190&nearbyArea=220&nearbyArea=670&nearbyArea=569&nearbyArea=560&nearbyArea=559&nearbyArea=231&nearbyArea=558&nearbyArea=425&nearbyArea=202&nearbyArea=133&nearbyArea=58&nearbyArea=699&nearbyArea=32&nearbyArea=375&nearbyArea=673&nearbyArea=566&nearbyArea=345&nearbyArea=29&nearbyArea=348&nearbyArea=371&nearbyArea=377&searchNearby=2', 'https://hartford.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=59&nearbyArea=34&nearbyArea=248&nearbyArea=4&nearbyArea=239&nearbyArea=451&nearbyArea=349&nearbyArea=193&nearbyArea=281&nearbyArea=328&nearbyArea=686&nearbyArea=166&nearbyArea=249&nearbyArea=561&nearbyArea=279&nearbyArea=167&nearbyArea=250&nearbyArea=198&nearbyArea=168&nearbyArea=3&nearbyArea=170&nearbyArea=354&nearbyArea=684&nearbyArea=17&nearbyArea=356&nearbyArea=278&nearbyArea=38&nearbyArea=276&nearbyArea=378&nearbyArea=286&nearbyArea=130&nearbyArea=247&nearbyArea=93&nearbyArea=173&nearbyArea=463&nearbyArea=240&nearbyArea=357', 'https://buffalo.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=355&nearbyArea=700&nearbyArea=389&nearbyArea=483&nearbyArea=248&nearbyArea=484&nearbyArea=452&nearbyArea=27&nearbyArea=453&nearbyArea=275&nearbyArea=685&nearbyArea=482&nearbyArea=213&nearbyArea=201&nearbyArea=385&nearbyArea=214&nearbyArea=234&nearbyArea=706&nearbyArea=386&nearbyArea=487&nearbyArea=126&nearbyArea=277&nearbyArea=130&nearbyArea=704&nearbyArea=337&nearbyArea=463', 'https://vermont.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=281&nearbyArea=44&nearbyArea=169&nearbyArea=168&nearbyArea=354&nearbyArea=338&nearbyArea=683', 'https://bn.craigslist.org/search/cta? sort=date&srchType=T&nearbyArea=229&nearbyArea=190&nearbyArea=11&nearbyArea=569&nearbyArea=362&nearbyArea=698&nearbyArea=699&nearbyArea=224&nearbyArea=345&nearbyArea=225&searchNearby=2', 'https://billings.craigslist.org/search/cta? sort=date&srchType=T&searchNearby=2&nearbyArea=658&nearbyArea=661&nearbyArea=192&nearbyArea=660&nearbyArea=659&nearbyArea=656', 'https://imperial.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=8', 'https://lincoln.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=432&nearbyArea=55', 'https://holland.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=554&nearbyArea=309&nearbyArea=572&nearbyArea=627', 'https://wheeling.craigslist.org/search/cta?sort=date&srchType=T&searchNearby=2&nearbyArea=440&nearbyArea=704']

    def __init__(self):
        resp = requests.get(url=self.proxy_url, params=self.params)
        proxy_list = resp.text.split('\r\n')
        for proxy in proxy_list:
            self.proxy_list.append('https://'+proxy)
        # pdb.set_trace()

    def start_requests(self):
        for url in self.request_urls:
            self.ind += 1
            if self.ind % 100 == 0:
                self.ind = 0
            yield scrapy.Request(url=url, meta = {'parser': 'parse','proxy':self.proxy_list[self.ind]}, errback=self.errback_parse, callback=self.parse,dont_filter=True)
        

    def parse(self, response):
        totalCount = int(response.xpath('//span[@class="totalcount"]/text()').extract_first())
        base_url = response.url
        totalPage = totalCount / 120

        for index in range(0, totalPage):
            url = base_url + '&s=' + str(index * 120)
            self.ind += 1
            if self.ind % 100 == 0:
                self.ind = 0

            yield scrapy.Request(url, callback=self.parse_list, errback=self.errback_httpbin, meta = {'parser': 'parse_list','proxy':self.proxy_list[self.ind]},dont_filter=True)
        
    def parse_list(self, response):
        # pdb.set_trace()

        car_list = response.xpath('//li[@class="result-row"]')

        for car in car_list:
            try:
                item = ChainItem()
                item['link'] = car.xpath('.//p[@class="result-info"]/a[@class="result-title hdrlnk"]/@href').extract_first()
                item['title'] = car.xpath('.//p[@class="result-info"]/a[@class="result-title hdrlnk"]/text()').extract_first()
                item['price'] = car.xpath('.//p[@class="result-info"]//span[@class="result-price"]/text()').extract_first()

                yield item
            except Exception as e:
                pdb.set_trace()
                print e

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        #if isinstance(failure.value, HttpError):
        request = failure.request
        self.logger.error('TimeoutError on %s', request.url)
        self.ind += 1
        if self.ind % 100 == 0:
            self.ind = 0
        yield scrapy.Request(url=request.url, callback=self.parse_list, errback=self.errback_httpbin, meta = {'proxy':self.proxy_list[self.ind]},dont_filter=True)

            
    def errback_parse(self, failure):
        self.logger.error(repr(failure))
        request = failure.request
        self.logger.error('TimeoutError on %s', request.url)
        self.ind += 1
        if self.ind % 100 == 0:
            self.ind = 0

        yield scrapy.Request(url=request.url, callback=self.parse, errback=self.errback_parse, meta = {'proxy':self.proxy_list[self.ind]}, dont_filter=True)
            