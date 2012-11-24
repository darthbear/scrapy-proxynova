scrapy-proxynova
================

Use scrapy with a list of proxies generated from proxynova.com

The first run will generate the list of proxies from proxynova and store
it in the file specified by the variable PROXY_SERVER_LIST_CACHE_FILE in settings.py 

It will individually check each proxy to see if they work and remove the ones that timed out or cannot connect to.

Example:
	./run_example.sh

To regenerate the proxy list, simply remove the cache file
