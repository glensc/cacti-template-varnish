Cacti Varnish Template
======================

Uses advanced template from:
<http://forums.cacti.net/viewtopic.php?p=182152>

Combines script to pull data via Varnish admin port from
<http://forums.cacti.net/viewtopic.php?t=31260>

How to install
--------------

 1. Import `cacti_host_template_varnish.xml` to Cacti (tested with `0.8.7e`)
 2. Copy `get_varnish_stats.py` to `scripts`
 3. Make the Varnish management daemon available to your Cacti machine
    (Make sure you lock down appropriately with `iptables` or similar,
    because there is no authentication for this interface)

**IMPORTANT**: You need to recompile `spine` with `./configure --with-results-buffer=2048`.

Author
------

Elan Ruusamäe <glen@delfi.ee>

