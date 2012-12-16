import json
import os
import random
import re
import requests

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
    'jp': 'selected="selected">Japan',
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

    base_url = ('http://www.proxynova.com/proxy-server-list/'
                'country-{country}/?p={page_number}')
    pattern = re.compile(
        'data-proxy-ip="450">.*?'
        'proxy_decode\\(\'([0-9]*)\'\\).*?port-([0-9]*)/',
        re.DOTALL
    )
    proxies = []

    for page_number in range(1, 5):
        if len(proxies) == limit:
            break

        url = base_url.format(**locals())
        response = requests.get(url)

        for m in pattern.finditer(response.content):
            if len(proxies) == limit:
                break

            ip = int(m.group(1))
            port = int(m.group(2))

            # they encode the ip as a 32 bit int.
            # just decode it to an X.X.X.X notation
            octet1 = int(ip / 16777216)
            octet2 = int((ip % 16777216) / 65536)
            octet3 = int((ip % 65536) / 256)
            octet4 = ip % 256
            full_ip = '.'.join(map(str, (octet1, octet2, octet3, octet4)))
            server = '{0}:{1}'.format(full_ip, port)
            logger('Checking ' + server)

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

    return proxies


class Proxies(object):
    def __init__(self, cache_file, **kwargs):
        self.cache_file = cache_file
        if os.path.exists(self.cache_file):
            with open(self.cache_file) as f:
                self.proxies = json.loads(f.read())
        else:
            self.proxies = get_proxies(**kwargs)

            with open(self.cache_file, 'w+') as f:
                f.write(json.dumps(self.proxies))

    def get_proxy(self):
        return random.choice(self.proxies)


if __name__ == '__main__':
    proxies = get_proxies()
    print '\n'.join(proxies)
