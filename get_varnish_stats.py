#!/usr/bin/python
# vim: set encoding=utf-8:
# Author: Elan Ruusamäe <glen@delfi.ee>
# URL: https://github.com/glensc/cacti-template-varnish
#
# Original varnish stat script by dmuntean from http://forums.cacti.net/viewtopic.php?t=31260
# Modified by glen to add support for new template: http://forums.cacti.net/viewtopic.php?p=182152

import telnetlib
import re
import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], "h:p:2d", ["host=", "port="])
host = '127.0.0.1'
port = 6082
debug = False
version = 3
for o, v in opts:
	if o in ("-h", "--host"):
		host = str(v)
	if o in ("-p", "--port"):
		port = int(v)
	if o in ("-2"):
		version = 2
	if o in ("-d"):
		debug = True

# This serves as template for matching keys.
# Also all entries present in this table must be present in result
# You should upgrade Varnish 2.1 as Varnish 2.0 does not have "uptime" column.
sample = """
uptime                  36897          .   Child uptime
client_conn           6724115       182.24 Client connections accepted
client_drop                 0         0.00 Connection dropped, no sess
client_req           29357678       795.67 Client requests received
cache_hit            27645207       749.25 Cache hits
cache_hitpass          114269         3.10 Cache hits for pass
cache_miss            1586933        43.01 Cache misses
backend_conn           995606        26.98 Backend conn. success
backend_unhealthy           0         0.00 Backend conn. not attempted
backend_busy                0         0.00 Backend conn. too many
backend_fail                1         0.00 Backend conn. failures
backend_reuse          716090        19.41 Backend conn. reuses
backend_toolate        937223        25.40 Backend conn. was closed
backend_recycle       1653334        44.81 Backend conn. recycles
backend_unused              0         0.00 Backend conn. unused
fetch_head                 33         0.00 Fetch head
fetch_length           613801        16.64 Fetch with Length
fetch_chunked         1087578        29.48 Fetch chunked
fetch_eof                   0         0.00 Fetch EOF
fetch_bad                   0         0.00 Fetch had bad headers
fetch_close              5649         0.15 Fetch wanted close
fetch_oldhttp               0         0.00 Fetch pre HTTP/1.1 closed
fetch_zero               2304         0.06 Fetch zero len
fetch_failed               17         0.00 Fetch failed
n_srcaddr                   0          .   N struct srcaddr
n_srcaddr_act               0          .   N active struct srcaddr
n_sess_mem               2200          .   N struct sess_mem
n_sess                   1168          .   N struct sess
n_object                76813          .   N struct object
n_objecthead            51153          .   N struct objecthead
n_smf                  159665          .   N struct smf
n_smf_frag               4500          .   N small free smf
n_smf_large              1979          .   N large free smf
n_vbe_conn                 29          .   N struct vbe_conn
n_bereq                   212          .   N struct bereq
n_wrk                     600          .   N worker threads
n_wrk_create              600         0.02 N worker threads created
n_wrk_failed                0         0.00 N worker threads not created
n_wrk_max                   0         0.00 N worker threads limited
n_wrk_queue                 0         0.00 N queued work requests
n_wrk_overflow           2639         0.07 N overflowed work requests
n_wrk_drop                  0         0.00 N dropped work requests
n_backend                  20          .   N backends
n_expired              808579          .   N expired objects
n_lru_nuked            701957          .   N LRU nuked objects
n_lru_saved                 0          .   N LRU saved objects
n_lru_moved          13197669          .   N LRU moved objects
n_deathrow                  0          .   N objects on deathrow
losthdr                    10         0.00 HTTP header overflows
n_objsendfile               0         0.00 Objects sent with sendfile
n_objwrite           27988657       758.56 Objects sent with write
n_objoverflow               0         0.00 Objects overflowing workspace
s_sess                6724087       182.24 Total Sessions
s_req                29358671       795.69 Total Requests
s_pipe                   2219         0.06 Total pipe
s_pass                 122593         3.32 Total pass
s_fetch               1709352        46.33 Total fetch
s_hdrbytes        10134822172    274678.76 Total header bytes
s_bodybytes      210452858412   5703793.22 Total body bytes
sess_closed            404260        10.96 Session Closed
sess_pipeline          110465         2.99 Session Pipeline
sess_readahead         117895         3.20 Session Read Ahead
sess_linger          28952376       784.68 Session Linger
sess_herd            23901613       647.79 Session herd
shm_records        1248208604     33829.54 SHM records
shm_writes           75556170      2047.76 SHM writes
shm_flushes             54950         1.49 SHM flushes due to overflow
shm_cont               238017         6.45 SHM MTX contention
shm_cycles                509         0.01 SHM cycles through buffer
sm_nreq               4123515       111.76 allocator requests
sm_nobj                153186          .   outstanding allocations
sm_balloc          2119176192          .   bytes allocated
sm_bfree           4323274752          .   bytes free
sma_nreq                    0         0.00 SMA allocator requests
sma_nobj                    0          .   SMA outstanding allocations
sma_nbytes                  0          .   SMA outstanding bytes
sma_balloc                  0          .   SMA bytes allocated
sma_bfree                   0          .   SMA bytes free
sms_nreq                  617         0.02 SMS allocator requests
sms_nobj                    0          .   SMS outstanding allocations
sms_nbytes                  0          .   SMS outstanding bytes
sms_balloc            4539572          .   SMS bytes allocated
sms_bfree             4539572          .   SMS bytes freed
backend_req           1709428        46.33 Backend requests made
n_vcl                       1         0.00 N vcl total
n_vcl_avail                 1         0.00 N vcl available
n_vcl_discard               0         0.00 N vcl discarded
n_purge                     1          .   N total active purges
n_purge_add                 1         0.00 N new purges added
n_purge_retire              0         0.00 N old purges deleted
n_purge_obj_test            0         0.00 N objects tested
n_purge_re_test             0         0.00 N regexps tested against
n_purge_dups                0         0.00 N duplicate purges removed
hcb_nolock                  0         0.00 HCB Lookups without lock
hcb_lock                    0         0.00 HCB Lookups with lock
hcb_insert                  0         0.00 HCB Inserts
esi_parse                   0         0.00 Objects ESI parsed (unlock)
esi_errors                  0         0.00 ESI parse errors (unlock)
"""

# map Varnish2 variables (keys) to related Varnish3 ones
remap = {
	'sm_nreq':			'SMA.s0.c_req',
	'sm_nobj':			'SMA.s0.g_alloc',
	'sm_balloc':		'SMA.s0.c_bytes',
	'sm_bfree':			'SMA.s0.c_freed',
	'n_purge':			'n_ban',
	'n_purge_add':		'n_ban_add',
	'n_purge_retire':	'n_ban_retire',
	'n_purge_obj_test':	'n_ban_obj_test',
	'n_purge_re_test':	'n_ban_re_test',
	'n_purge_dups':		'n_ban_dups',
	'backend_unused':	'backend_retry',
	'n_wrk_queue':		'n_wrk_queued',
	'sma_nreq':			'SMA.Transient.c_req',
	'sma_nobj':			'SMA.Transient.g_alloc',
	'sma_nbytes':		'SMA.Transient.g_bytes',
	'sma_balloc':		'SMA.Transient.c_bytes',
	'sma_bfree':		'SMA.Transient.g_space',
}

# gather raw varnishstat over tcp
def varnishstat_tcp():
	telnet = telnetlib.Telnet()
	telnet.open(host, port)

	if version == 3:
		# plain telnet, over xinetd
		out = telnet.read_until("VBE.", 10)
	else:
		# varnishstat port
		telnet.write('stats\r\nquit\r\n')
		out = telnet.read_until("ESI parse errors (unlock)", 10)
	telnet.close()

	return out

# process varnishstat data.
# return KEY=VALUE pairs
#
# Varnish 2 output looks like (we use long description as the key)
#200 3262
#           1  Client connections accepted
#           0  Connection dropped, no sess
#           1  Client requests received
# Varnish 3 output looks like (we use first column as the key)
#client_conn          915477075       543.26 Client connections accepted
#client_drop                  0         0.00 Connection dropped, no sess/wrk
#client_req          1611485157       956.27 Client requests received
def parse_input(text):
	if version == 3:
		line_re = re.compile('^(?P<key>\S+)\s+(?P<value>\d+).+$')
	else:
		line_re = re.compile('^\s*(?P<value>\S+)\s+(?P<key>.+)$')

	res = {}
	for line in text.split('\n'):
		m = re.search(line_re, line)
		if m:
			res[m.group('key')] = m.group('value')
	return res

# map dictionary from parse_input to keys from "sample" string
def map_keys(res):
	if version == 3:
		sample_key = 'key'
	else:
		sample_key = 'desc'

	split_re = re.compile('^(?P<key>\S+)\s+(?P<value>\d+)\s+\S+\s+(?P<desc>.+)$')
	data = {}
	for line in sample.split('\n'):
		m = re.search(split_re, line);
		if not m:
			continue

		key = m.group(sample_key)
		if remap.has_key(key):
			key = remap[key]

		if res.has_key(key):
			value = res[key]
		else:
			# for missing value, print -1
			value = '-1'

		data[m.group('key')] = value

	return data

def get_data():
	text = varnishstat_tcp()
	res = parse_input(text)
	data = map_keys(res)

	# add results for original script
	hit = float(data['cache_hit'])
	miss = float(data['cache_miss'])
	if hit + miss > 0:
		hitrate = round(hit / (hit + miss) * 100, 1)
	else:
		hitrate = 0
	data['varnish_requests'] = data['client_req']
	data['varnish_hitrate'] = hitrate
	return data

data = get_data()
stats = ''
for k, v in data.items():
	stats += '%s:%s ' %(k, v)

print stats
if debug:
	print >>sys.stderr, "[%s:%s]: %s" % (host, port, stats)
