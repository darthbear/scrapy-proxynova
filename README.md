scrapy-proxynova
================

Use scrapy with a list of proxies generated from proxynova.com

The first run will generate the list of proxies from <http://proxynova.com> and store
it in the cache.

It will individually check each proxy to see if they work and remove the ones that timed out or cannot connect to.

Example:

    ./run_example.sh

To regenerate the proxy list, simply remove the cache file.

Options
-------

Set these options in the `settings.py`.

* PROXY_SERVER_LIST_CACHE_FILE — a file to store proxies list. Default: `proxies.json`.
* PROXY_SERVER_COUNTRY — country code, to select proxies from. Default: `us`.
* PROXY_SERVER_TIMEOUT — access timeout, in seconds. If proxy does not respond in time,
  during the check, then it considered dead. Default: 1 second.
* PROXY_SERVER_LIMIT — a number of proxies in the list. Default: 10.
