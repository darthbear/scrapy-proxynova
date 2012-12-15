from proxies import Proxies
from scrapy import log


class HttpProxyMiddleware(object):
    def __init__(self, *args, **kwargs):
        self.proxies = Proxies(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get(
                'PROXY_SERVER_LIST_CACHE_FILE',
                'proxies.json'
            ),
            country=crawler.settings['PROXY_SERVER_COUNTRY'],
            timeout=crawler.settings['PROXY_SERVER_TIMEOUT'],
            limit=crawler.settings['PROXY_SERVER_LIMIT'],
            logger=lambda message: log.msg(message),
        )

    def process_request(self, request, spider):
        proxy = self.proxies.get_proxy()
        log.msg('Using proxy ' + proxy, spider=spider)
        request.meta['proxy'] = 'http://' + proxy
