#!/usr/bin/python
# vim: set encoding=utf-8:
# $Id$
# Author: Elan Ruusamäe <glen@delfi.ee>
#
# Original varnish stat script by dmuntean from http://forums.cacti.net/viewtopic.php?t=31260
# Modified by glen to add support for new template: http://forums.cacti.net/viewtopic.php?p=182152
#

import telnetlib
import re
import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
host = '127.0.0.1'
port = 6082
for o, v in opts:
    if o in ("-h", "--host"):
        host = str(v)
    if o in ("-p", "--port"):
        port = int(v)

telnet = telnetlib.Telnet()
telnet.open(host, port)
telnet.write('stats\r\n')
out = telnet.read_until("ESI parse errors (unlock)", 10)
telnet.write('quit\r\n')
telnet.close()

# This serves as template for matching keys.
# Also all entries present in this table must be present in result
# You should upgrade Varnish 2.1 as Varnish 2.0 does not have "uptime" column.
sample = """
uptime                  17903          .   Child uptime
client_conn           3333449       186.19 Client connections accepted
client_req           14776402       825.36 Client requests received
cache_hit            13929762       778.07 Cache hits
cache_hitpass           52996         2.96 Cache hits for pass
cache_miss             788513        44.04 Cache misses
backend_conn           494618        27.63 Backend conn. success
backend_unhealthy           0         0.00 Backend conn. not attempted
backend_busy                0         0.00 Backend conn. too many
backend_fail                0         0.00 Backend conn. failures
backend_reuse          351664        19.64 Backend conn. reuses
backend_recycle        817584        45.67 Backend conn. recycles
backend_unused              0         0.00 Backend conn. unused
backend_toolate        868693        25.81 Backend conn. was closed
n_srcaddr                   0          .   N struct srcaddr
n_srcaddr_act               0          .   N active struct srcaddr
n_sess_mem               2200          .   N struct sess_mem
n_sess                   1207          .   N struct sess
n_object               151202          .   N struct object
n_objecthead            91698          .   N struct objecthead
n_smf                  326799          .   N struct smf
n_smf_frag              24687          .   N small free smf
n_smf_large               326          .   N large free smf
n_vbe_conn                 26          .   N struct vbe_conn
n_bereq                   212          .   N struct bereq
n_wrk                     600          .   N worker threads
n_wrk_create              600         0.03 N worker threads created
n_wrk_failed                0         0.00 N worker threads not created
n_wrk_max                   0         0.00 N worker threads limited
n_wrk_queue                 0         0.00 N queued work requests
n_wrk_overflow           2639         0.15 N overflowed work requests
n_wrk_drop                  0         0.00 N dropped work requests
n_backend                  20          .   N backends
n_expired              472014          .   N expired objects
n_lru_nuked            165622          .   N LRU nuked objects
n_lru_saved                 0          .   N LRU saved objects
n_lru_moved           6575346          .   N LRU moved objects
n_objsendfile               0         0.00 Objects sent with sendfile
n_objwrite           14087414       786.87 Objects sent with write
n_objoverflow               0         0.00 Objects overflowing workspace
s_pipe                    879         0.05 Total pipe
s_pass                  56935         3.18 Total pass
s_hdrbytes         5095096301    284594.55 Total header bytes
s_bodybytes      105139468938   5872729.09 Total body bytes
s_fetch               1669741        46.49 Total fetch
s_req                28734002       799.12 Total Requests
s_sess                6579080       182.90 Total Sessions
sess_closed            211106        11.79 Session Closed
sess_pipeline           52085         2.91 Session Pipeline
sess_readahead          54758         3.06 Session Read Ahead
sess_linger          14576708       814.20 Session Linger
sess_herd            11874652       663.28 Session herd
shm_records         626744114     35007.77 SHM records
shm_writes           37710636      2106.39 SHM writes
shm_flushes             32226         1.80 SHM flushes due to overflow
shm_cont               101165         5.65 SHM MTX contention
shm_cycles                256         0.01 SHM cycles through buffer
sm_nreq               1857435       103.75 allocator requests
sm_balloc          3918831616          .   bytes allocated
sm_bfree           5332348928          .   bytes free
sm_nobj                 85307          .   outstanding allocations
sma_nreq                    0         0.00 SMA allocator requests
sma_nbytes                  0          .   SMA outstanding bytes
sms_nreq                  344         0.02 SMS allocator requests
sms_nbytes                  0          .   SMS outstanding bytes
sma_balloc                  0          .   SMA bytes allocated
sma_bfree                   0          .   SMA bytes free
sma_nobj                    0          .   SMA outstanding allocations
sms_balloc            4466012          .   SMS bytes allocated
sms_bfree             4466012          .   SMS bytes freed
sms_nobj                    0          .   SMS outstanding allocations
backend_req            845376        47.22 Backend requests made
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

# process results
split = re.compile('^\s*(?P<value>\S+)\s+(?P<key>.+)$')
res = {}
for line in out.split('\n'):
	m = re.search(split, line);
	if m:
		res[m.group('key')] = m.group('value')

# map for keys
split = re.compile('^(?P<key>\S+)\s+(\d+)\s+\S+\s+(?P<value>.+)$')
for line in sample.split('\n'):
	m = re.search(split, line);
	if m:
		if res.has_key(m.group('value')):
			value = res[m.group('value')]
			print "%s:%s" % (m.group('key'), value),
		else:
			# for missing value, print -1
			print "%s:-1" % m.group('key'),

# print results for original script
req = res['Client requests received']
hit = float(res['Cache hits'])
miss = float(res['Cache misses'])
print 'varnish_requests:'+str(req)+' varnish_hitrate:'+str(round(hit / (hit + miss) * 100, 1))
