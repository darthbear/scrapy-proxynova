import os
import random
import re
import requests
import sys
import StringIO

countries = {
    'br': 'Brazil',
    'cn': 'China',
    'id': 'Indonesia',
    'th': 'Thailand',
    've': 'Venezuela',
    'eg': 'Egypt',
    'us': 'United States',
    'pe': 'Peru',
    'ru': 'Russia',
    'tw': 'Taiwan',
    'ae': 'United Arab Emirates',
    'in': 'India',
    'ar': 'Argentina',
    'za': 'South Africa',
    'co': 'Colombia',
    'de': 'Germany',
    'ua': 'Ukraine',
    'hk': 'Hong Kong',
    'fr': 'France',
    'mx': 'Mexico',
    'pl': 'Poland',
    'bd': 'Bangladesh',
    'it': 'Italy',
    'ec': 'Ecuador',
    'gb': 'United Kingdom',
    'jp': 'Japan',
    'nl': 'Netherlands',
    'tr': 'Turkey',
    'cl': 'Chile',
    'pk': 'Pakistan',
    'ca': 'Canada',
    'mn': 'Mongolia',
    'cz': 'Czech Republic',
    'kr': 'South Korea',
    'my': 'Malaysia',
    'kh': 'Cambodia',
    'ma': 'Morocco',
    'rs': 'Serbia',
    'bn': 'Brunei Darussalam',
    'ir': 'Iran',
    'iq': 'Iraq',
    'hu': 'Hungary',
    'bg': 'Bulgaria',
    'es': 'Spain',
    'vn': 'Vietnam',
    'lb': 'Lebanon',
    'ng': 'Nigeria',
    'ro': 'Romania',
    'eu': 'European Union',
    'ph': 'Philippines',
}


def get_proxies(country=None, timeout=None, limit=None, logger=None):
    country = 'us' if country is None else country
    timeout = 1 if timeout is None else timeout
    limit = 10 if limit is None else limit
    if logger is None:
        def logger(msg):
            print msg

    if country not in countries:
        raise RuntimeError('Not allowed country code.')

    base_url = ('http://www.proxynova.com/proxy_list.txt?country={country}')

    proxies = []

    url = base_url.format(**locals())
    response = requests.get(url)

    ip_port_pattern = re.compile("(\d+\.\d+\.\d+\.\d+:\d+)")
    buf = StringIO.StringIO(response.content)
    line = buf.readline()
    while line:
        if len(proxies) == limit:
           break

	match = ip_port_pattern.match(line)
        if match:
	    server = match.group(0)
            try:
	        response = requests.get(
		              'http://www.linkedin.com',
		              proxies=dict(http=server),
                              timeout=timeout,
                           )
	        if 'Company Directory' in response.content:
	            logger('Found alive proxy: ' + server)
	            proxies.append(server)
	        else:
	            logger(
		        'Error while reading data from '
		        'proxy {0}. Skipping...'.format(server)
	            )
            except Exception, e:
	        logger('An error occured: {}. Skipping server {}'.format(
	               e,
	               server
	         ))
	line = buf.readline()

    return proxies


class Proxies(object):
    def __init__(self, proxy_file, **kwargs):
        self.proxy_file = proxy_file
        if os.path.exists(self.proxy_file):
            with open(self.proxy_file) as f:
		self.proxies = []
		for line in iter(f):
		    server = line.strip()
		    if len(server) > 0:
		        self.proxies.append(line)
	        if len(self.proxies) == 0:
		    raise IOError("Proxy file '%s' is empty"%self.proxy_file)
        else:
	    raise IOError("Cannot find proxy file '%s'"%self.proxy_file)

    def get_proxy(self):
        return random.choice(self.proxies)


if __name__ == '__main__':
    if len(sys.argv) < 5:
	sys.exit('Usage: %s <country code> <timeout in secs> <max proxies> <output file>'%sys.argv[0])

    country = sys.argv[1].lower()
    timeout = int(sys.argv[2])
    max_proxies = int(sys.argv[3])
    proxy_file = sys.argv[4]

    try:
        proxies = get_proxies(country, timeout, max_proxies)
    except Exception, e:
        sys.stderr.write("Error while fetching proxies from proxynova.com: %s\n"%e)
	sys.exit(1)

    if len(proxies) == 0:
        sys.stderr.write("Error: Cannot find any available proxies\n")
	sys.exit(1)
    else:
        with open(proxy_file, 'w+') as f:
	    f.write('\n'.join(proxies))
