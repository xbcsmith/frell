
all: all-subdirs default-all

all-subdirs:
	for d in $(SUBDIRS); do make -C $$d DIR=$$d || exit 1; done

export TOPDIR = $(shell pwd)
export TIMESTAMP = $(shell python -c "import time; print time.time(); exit;")
export DISTDIR = $(TOPDIR)/$(MODULE)-$(VERSION)
export CHANGESET = $(shell ./scripts/short-commit-version.sh)


SUBDIRS=onepm commands

MANPAGES=$(notdir $(filter %.1,$(wildcard docs/manpages/*.1)))

extra_files = \
	Make.rules 		\
	Makefile		\
	Make.defs		\
	NEWS			\
	README			\
	LICENSE


.PHONY: clean dist install subdirs html

subdirs: default-subdirs

install: install-subdirs

clean: clean-subdirs default-clean

doc: html

man:
	mkdir -p $(DESTDIR)$(mandir)/man1
	for M in $(MANPAGES); do \
		install -m 0644 docs/manpages/$$M $(DESTDIR)$(mandir)/man1/; \
		gzip $(DESTDIR)$(mandir)/man1/$$M; \
	done

dist:
	if ! grep "^Changes in $(VERSION)" NEWS > /dev/null 2>&1; then \
		echo "no NEWS entry"; \
		exit 1; \
	fi
	$(MAKE) forcedist


archive:
	git archive --format=tar --prefix=$(NAME)-$(VERSION)/ HEAD | gzip -9c > $(NAME)-$(VERSION).tar.gz

tag:
	git tag $(NAME)-$(VERSION)


include Make.rules
include Make.defs
 
# vim: set sts=8 sw=8 noexpandtab :
