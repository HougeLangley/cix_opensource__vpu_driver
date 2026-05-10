PACKAGE := cix-vpu-driver
VERSION := 1.0.1
TARBALL := $(PACKAGE)-$(VERSION).tar.gz
RPMDIR  := /tmp/rpmbuild

srpm:
	@echo "==> Setting up rpmbuild directories..."
	mkdir -p $(RPMDIR)/{SOURCES,SPECS,SRPMS}
	@echo "==> Creating source tarball..."
	mkdir -p /tmp/pkg/$(PACKAGE)-$(VERSION)
	find . -mindepth 1 -maxdepth 1 \
		! -name '.git' \
		! -name '.copr' \
		! -name '*.spec' \
		-exec cp -a {} /tmp/pkg/$(PACKAGE)-$(VERSION)/ \;
	tar czf $(RPMDIR)/SOURCES/$(TARBALL) -C /tmp/pkg $(PACKAGE)-$(VERSION)
	@echo "==> Building SRPM..."
	cp $(PACKAGE).spec $(RPMDIR)/SPECS/
	rpmbuild -bs --define "_topdir $(RPMDIR)" $(RPMDIR)/SPECS/$(PACKAGE).spec
	@echo "==> Copying SRPM to output..."
	cp $(RPMDIR)/SRPMS/*.src.rpm $(outdir)/
