PYTHON := python3
VENV := .venv/bin/activate
PELICAN := $(shell which pelican || echo .venv/bin/pelican)
PELICANOPTS :=

BASEDIR := $(CURDIR)
INPUTDIR := $(BASEDIR)/content
OUTPUTDIR := $(BASEDIR)/output
CONFFILE := $(BASEDIR)/pelicanconf.py
PUBLISHCONF := $(BASEDIR)/publishconf.py

help:
	@echo 'Makefile for a Pelican Web site'
	@echo ''
	@echo 'Usage:'
	@echo '   make html            (re)generate the web site'
	@echo '   make clean           remove the generated files'
	@echo '   make regenerate      regenerate files upon modification'
	@echo '   make publish         generate using production settings'
	@echo '   make serve           serve site at http://localhost:8000'
	@echo '   make devserver       start/restart develop_server.sh'
	@echo '   make stopserver      stop local server'
	@echo '   make css             build TailwindCSS'
	@echo '   make watch           watch and build CSS'
	@echo ''
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html'
	@echo 'Set the RELATIVE_URLS variable to 1 to enable relative urls'

html: css
	@if [ -f $(VENV) ]; then \
		. $(VENV) && $(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS); \
	else \
		$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS); \
	fi

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	@if [ -f $(VENV) ]; then \
		. $(VENV) && $(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS); \
	else \
		$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS); \
	fi

serve:
	cd $(OUTPUTDIR) && $(PYTHON) -m pelican.server

devserver:
	$(BASEDIR)/develop_server.sh restart

stopserver:
	$(BASEDIR)/develop_server.sh stop

publish: css
	@if [ -f $(VENV) ]; then \
		. $(VENV) && $(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS); \
	else \
		$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS); \
	fi

css:
	npm run build:css

watch:
	npm run watch:css

.PHONY: html help clean regenerate serve devserver stopserver publish css watch

