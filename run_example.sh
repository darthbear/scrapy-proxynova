#!/bin/sh

(cd scrapy_proxynova; python proxies.py us 5 10 /tmp/__proxy_servers.txt)
export PYTHONPATH=$PYTHONPATH:$PWD
(cd example-project; scrapy crawl dealsplus)
