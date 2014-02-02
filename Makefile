
SPECFILE        := $(firstword $(wildcard *.spec))
PACKAGE_NAME    := $(patsubst %.spec,%,$(SPECFILE))
PACKAGE_VERSION := $(shell awk '/Version:/{print $$2}' $(SPECFILE))

all:

dist:
	rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	install -d $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	cp -a get_varnish_stats.py cacti_host_template_varnish.xml README.md $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	tar czf $(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	md5sum -b $(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz > $(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz.md5
