scrapy-proxynova
================

Use scrapy with a list of proxies generated from proxynova.com

The first run will generate the list of proxies from <http://proxynova.com> and store it in the cache.

It will individually check each proxy to see if they work and remove the ones that timed out or cannot connect to.

Example:

    ./run_example.sh

To regenerate the proxy list, run: python proxies.py

Options
-------

Set these options in the `settings.py`.

* PROXY_SERVER_LIST_CACHE_FILE — a file to store proxies list. Default: `proxies.txt`.
* PROXY_BYPASS_PERCENT — probability for a connection to use a direct connection and not use a proxy
