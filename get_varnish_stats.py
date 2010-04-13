#!/usr/bin/python
import telnetlib
import re
import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
host = '127.0.0.1'
port = 9001
for o, v in opts:
    if o in ("-h", "--host"):
        host = str(v)
    if o in ("-p", "--port"):
        port = int(v)
	
telnet = telnetlib.Telnet()
telnet.open(host, port)
telnet.write('stats\r\n')
out=telnet.read_until("N duplicate purges removed", 10)
telnet.write('quit\r\n')
telnet.close()

req = re.search("\d+  Client requests received", out)
req = req.group(0).split()[0]

hit = re.search("\d+  Cache hits", out)
hit = float(hit.group(0).split()[0])

miss = re.search("\d+  Cache misses", out)
miss = float(miss.group(0).split()[0])

print 'varnish_requests:'+str(req)+' varnish_hitrate:'+str(round(hit / (hit + miss) * 100, 1))

