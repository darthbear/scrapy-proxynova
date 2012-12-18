# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'example'

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

ITEM_PIPELINES = [
    'example.pipelines.ExamplePipeline',
]

DOWNLOADER_MIDDLEWARES = {
        'scrapy_proxynova.middleware.HttpProxyMiddleware': 543,
        'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware':100
}   

PROXY_SERVER_LIST_CACHE_FILE='/tmp/__proxy_servers.txt'
    
DOWNLOAD_TIMEOUT=30

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'example (+http://www.yourdomain.com)'
