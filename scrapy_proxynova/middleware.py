from proxies import Proxies
import random

class HttpProxyMiddleware(object):
    def __init__(self, cache_file):
	self.proxies = Proxies(cache_file)	

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['PROXY_SERVER_LIST_CACHE_FILE'])

    def process_request(self, request, spider):
	proxy = self.proxies.getProxy()
	print "Using proxy %s"%proxy
	request.meta['proxy'] = "http://%s" % proxy
