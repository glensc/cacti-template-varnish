
PACKAGE_NAME    := $(patsubst %.spec,%,$(wildcard *.spec))
PACKAGE_VERSION := $(shell awk '/Version:/{print $$2}' $(PACKAGE_NAME).spec)

all:

dist:
	rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	install -d $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	cp -a get_varnish_stats.py cacti_host_template_varnish.xml README $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	tar czf $(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	rm -rf $(PACKAGE_NAME)-$(PACKAGE_VERSION)
	md5sum -b $(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz > $(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz.md5
