# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = uv run --group docs sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean livehtml linkcheck

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "html        Build the docs as HTML"
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t

# Clean the build output
clean:
	-rm -rf $(BUILDDIR)/*

# Build and serve docs with live reload
livehtml:
	sphinx-autobuild -b html --port 9000 --watch . -c . $(SOURCEDIR) $(BUILDDIR)/html

# Check all external links for integrity
linkcheck:
	$(SPHINXBUILD) -b linkcheck $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -c .
