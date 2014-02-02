Cacti Varnish Template
======================

Uses advanced template from:
<http://forums.cacti.net/viewtopic.php?p=182152>

Combines script to pull data via Varnish admin port from
<http://forums.cacti.net/viewtopic.php?t=31260>

How to install
--------------

 1. Import `cacti_host_template_varnish.xml` to Cacti
 2. Copy `get_varnish_stats.py` to `scripts`
 3. Make the varnishstat available to your Cacti machine (read below)

**IMPORTANT**: You need to recompile `spine` with `./configure --with-results-buffer=2048`.

For Varnish 2, you can use Varnish management service, configure it to be accessible. For 2.0 make sure you lock down appropriately with `iptables` or similar, because there is no authentication for this interface, for 2.1 the authentication is (currently) not implemented by this template poller.

Varnish 3 does not have `stats` command anymore in management interface. You can setup [inetd][1] daemon like [xinetd][2] to serve the `varnishstat` command remotely (again be sure to restrict access to prevent any unauthorized access):

```
service varnishstat
{
    socket_type         = stream
    wait                = no
    user                = nobody
    server              = /usr/bin/varnishstat
    server_args         = -1
    only_from          = 10.10.0.7
    log_on_success      = HOST
}
```

Samples
-------

**Backend Traffic**

![Backend Traffic](img/Backend Traffic.png)

**Critbit data**

![Critbit data](img/Critbit data.png)

**Data structure sizes**

![Data structure sizes](img/Data structure sizes.png)

**ESI**

![ESI](img/ESI.png)

**Hitrate %**

![Hitrate %](img/Hitrate %25.png)

**Hit rates**

![Hit rates](img/Hit rates.png)

**LRU activity**

![LRU activity](img/LRU activity.png)

**Memory allocation requests**

![Memory allocation requests](img/Memory allocation requests.png)

**Number of objects**

![Number of objects](img/Number of objects.png)

**Object expunging**

![Object expunging](img/Object expunging.png)

**Objects delivered with sendfile vs write**

![Objects delivered with sendfile vs write](img/Objects delivered with sendfile vs write.png)

**Objects overflowing workspace**

![Objects overflowing workspace](img/Objects overflowing workspace.png)

**Objects per objecthead**

![Objects per objecthead](img/Objects per objecthead.png)

**Request rates**

![Request rates](img/Request rates.png)

**Session herd**

![Session herd](img/Session herd.png)

**Sessions**

![Sessions](img/Sessions.png)

**Shared memory activity**

![Shared memory activity](img/Shared memory activity.png)

**SHM writes and records**

![SHM writes and records](img/SHM writes and records.png)

**Thread status**

![Thread status](img/Thread status.png)

**Memory Usage**
![Memory Usage](img/Memory Usage.png)

**Transfer rates**
![Transfer rates](img/Transfer rates.png)

**Uptime**
![Uptime](img/Uptime.png)

**VCL and purges**
![VCL and purges](img/VCL and purges.png)


Author
------

Elan Ruusamäe <glen@delfi.ee>


  [1]: http://en.wikipedia.org/wiki/Inetd
  [2]: http://en.wikipedia.org/wiki/Xinetd
