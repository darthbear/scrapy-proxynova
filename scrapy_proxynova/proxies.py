import pycurl
import StringIO
import re
import random
import os
import json

class Proxies(object):
	PROXY_LIST_BASE_URL = "http://www.proxynova.com/proxy-server-list/country-us/?p=%d"
	pattern = re.compile('data-proxy-ip="450">.*?proxy_decode\\(\'([0-9]*)\'\\).*?port-([0-9]*)/', re.DOTALL)

	proxies = []

	def __init__(self, cache_file):
		self.cache_file = cache_file
		if os.path.exists(self.cache_file):
			f = open(self.cache_file, 'r')	
			self.proxies = json.loads(f.read())
			return

		for i in range(1,5):
			url = self.PROXY_LIST_BASE_URL%i
			c = pycurl.Curl()
			c.setopt(pycurl.URL, url)
			c.setopt(pycurl.HTTPHEADER, ["Accept:"])
			b = StringIO.StringIO()
			c.setopt(pycurl.WRITEFUNCTION, b.write)
			c.perform()
			for m in self.pattern.finditer(b.getvalue()):
				ip = int(m.group(1))
				port = int(m.group(2))

				# they encode the ip as a 32 bit int. 
				# just decode it to an X.X.X.X notation
				octet1 = int(ip / 16777216)
				octet2 = int((ip % 16777216) / 65536)
				octet3 = int((ip % 65536) / 256)
				octet4 = ip % 256
				full_ip = "%d.%d.%d.%d"%(octet1, octet2, octet3, octet4)
				print "Checking %s:%d"%(full_ip, port)
				# check if I can connect to the proxy
				c = pycurl.Curl()
				c.setopt(pycurl.URL, 'http://www.linkedin.com')
				c.setopt(pycurl.PROXY, full_ip)
				c.setopt(pycurl.PROXYPORT, port)
				#c.setopt(pycurl.VERBOSE, 1)		
				c.setopt(pycurl.CONNECTTIMEOUT, 10)
				c.setopt(pycurl.TIMEOUT, 10)
				c.setopt(pycurl.NOSIGNAL, 1)
				c.setopt(pycurl.HTTPGET, 1)
				b = StringIO.StringIO()
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				try:
					c.perform()
					if ("Company Directory" in b.getvalue()):
						server_name = "%s:%d"%(full_ip, port)
						print "adding: %s"%server_name
						self.proxies.append(server_name)
					else:
						print "Error while reading data from proxy %s:%d. Skipping..."%(full_ip, port)
				except pycurl.error, error:
					print "An error occured: %s. Skipping server %s:%d"%(error, full_ip, port)

		f = open(self.cache_file, 'w+')	
		f.write(json.dumps(self.proxies))
		f.close()

	def getProxy(self):
		return random.choice(self.proxies)
