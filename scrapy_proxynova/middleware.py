from proxies import Proxies
from scrapy import log
import random

class HttpProxyMiddleware(object):
    def __init__(self, proxy_file, proxy_bypass_percent, **kwargs):
	self.bypass_percent = int(proxy_bypass_percent)
        self.proxies = Proxies(proxy_file, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get(
                'PROXY_SERVER_LIST_CACHE_FILE',
                'proxies.txt'
            ),
            crawler.settings.get(
            	'PROXY_BYPASS_PERCENT',
		0
	    ),
            logger=lambda message: log.msg(message),
        )

    def process_request(self, request, spider):
	n = random.randint(0, 100)
	if n > self.bypass_percent:
            proxy = self.proxies.get_proxy()
            log.msg('Using proxy ' + proxy, spider=spider)
            request.meta['proxy'] = 'http://' + proxy
	else:
	    if 'proxy' in request.meta:
	        del request.meta['proxy']
            log.msg('No proxy used', spider=spider)
