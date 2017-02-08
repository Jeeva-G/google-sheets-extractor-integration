PACKAGE=$(shell dirname `find . -depth 2 -name "version.py" -print` | tr -d './')
VERSION=$(shell python -c "from $(PACKAGE).version import __version__ ; print(__version__)")
TAR_FILE=dist/$(PACKAGE)-$(VERSION).tar.gz

%.pdf: %.md $(DEPS)
	pandoc  $< -o $@

%.docx: %.md $(DEPS)
	pandoc  $< -o $@

%.html: %.md $(DEPS)
	pandoc  $< -o $@

all: install docx html pdf

SOURCES = $(basename $(shell ls -1 *.md))
MD_TARGETS = $(addsuffix .md, $(SOURCES))
DOCX_TARGETS = $(addsuffix .docx, $(SOURCES))
HTML_TARGETS = $(addsuffix .html, $(SOURCES))
PDF_TARGETS = $(addsuffix .pdf,$(SOURCES))
TARGETS = $(DOCX_TARGETS) $(HTML_TARGETS) $(PDF_TARGETS)

docx: $(DOCX_TARGETS)
html: $(HTML_TARGETS)
pdf: $(PDF_TARGETS)

install: build
	pip install $(TAR_FILE)

build: doc
	python setup.py sdist

doc: docx html pdf
	pandoc -f markdown -t plain README.md > README.txt

rebuild: clean install

upload:
	python setup.py sdist upload
	
clean:
	/bin/rm -rf build dist site MANIFEST
	pip freeze | grep "$(PACKAGE)==$(VERSION)" && pip uninstall -y $(PACKAGE)
	$(RM) $(TARGETS)
