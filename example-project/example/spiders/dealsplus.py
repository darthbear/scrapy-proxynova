from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

from example.items import Deal


class DealsplusSpider(BaseSpider):
    name = "dealsplus"
    allowed_domains = ["dealspl.us"]
    start_urls = [
        "http://dealspl.us/deals/hot/recent",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select("//table[@id='allDealTable']/tr/td")

        for item in items:
            deal = Deal()
            deal['title'] = item.select(".//div[@class='deal_img_span']/a/@title").extract()[0]
            deal['url'] = item.select(".//div[@class='deal_img_span']/a/@href").extract()[0]
            yield deal

	nextPage = hxs.select("//a[@class='box_a' and contains(text(), 'Next')]/@href")
	if not not nextPage:
		yield Request("http://dealspl.us%s"%nextPage.extract()[0], self.parse)
