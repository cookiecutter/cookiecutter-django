# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= 
SPHINXBUILD   ?= sphinx-build -c .
SOURCEDIR     = .
BUILDDIR      = ./_build
{%- if cookiecutter.use_docker == 'y' %}
APP = /app
{%- else %}
APP = ../{{cookiecutter.project_slug}}
{% endif %}

.PHONY: help livehtml apidocs Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build, watch and serve docs with live reload
livehtml:
	sphinx-autobuild -b html 
	{%- if cookiecutter.use_docker == 'y' %} --host 0.0.0.0
	{%- else %} --open-browser 
	{%- endif %} --port 7000 --watch $(APP) -c . $(SOURCEDIR) $(BUILDDIR)/html

# Outputs rst files from django application code
apidocs:
	{%- if cookiecutter.use_docker == 'y' %}
	sphinx-apidoc -o $(SOURCEDIR)/api /app
	{%- else %}
	sphinx-apidoc -o $(SOURCEDIR)/api ../{{cookiecutter.project_slug}}
	{%- endif %}

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
