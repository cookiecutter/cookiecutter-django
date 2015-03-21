# Makefile for Sphinx LaTeX output

ALLDOCS = $(basename $(wildcard *.tex))
ALLPDF = $(addsuffix .pdf,$(ALLDOCS))
ALLDVI = $(addsuffix .dvi,$(ALLDOCS))

# Prefix for archive names
ARCHIVEPRREFIX =
# Additional LaTeX options
LATEXOPTS =

all: $(ALLPDF)
all-pdf: $(ALLPDF)
all-dvi: $(ALLDVI)
all-ps: all-dvi
	for f in *.dvi; do dvips $$f; done

all-pdf-ja:
	for f in *.pdf *.png *.gif *.jpg *.jpeg; do extractbb $$f; done
	for f in *.tex; do platex -kanji=utf8 $(LATEXOPTS) $$f; done
	for f in *.tex; do platex -kanji=utf8 $(LATEXOPTS) $$f; done
	for f in *.tex; do platex -kanji=utf8 $(LATEXOPTS) $$f; done
	-for f in *.idx; do mendex -U -f -d "`basename $$f .idx`.dic" -s python.ist $$f; done
	for f in *.tex; do platex -kanji=utf8 $(LATEXOPTS) $$f; done
	for f in *.tex; do platex -kanji=utf8 $(LATEXOPTS) $$f; done
	for f in *.dvi; do dvipdfmx $$f; done

zip: all-$(FMT)
	mkdir $(ARCHIVEPREFIX)docs-$(FMT)
	cp $(ALLPDF) $(ARCHIVEPREFIX)docs-$(FMT)
	zip -q -r -9 $(ARCHIVEPREFIX)docs-$(FMT).zip $(ARCHIVEPREFIX)docs-$(FMT)
	rm -r $(ARCHIVEPREFIX)docs-$(FMT)

tar: all-$(FMT)
	mkdir $(ARCHIVEPREFIX)docs-$(FMT)
	cp $(ALLPDF) $(ARCHIVEPREFIX)docs-$(FMT)
	tar cf $(ARCHIVEPREFIX)docs-$(FMT).tar $(ARCHIVEPREFIX)docs-$(FMT)
	rm -r $(ARCHIVEPREFIX)docs-$(FMT)

bz2: tar
	bzip2 -9 -k $(ARCHIVEPREFIX)docs-$(FMT).tar

# The number of LaTeX runs is quite conservative, but I don't expect it
# to get run often, so the little extra time won't hurt.
%.dvi: %.tex
	latex $(LATEXOPTS) '$<'
	latex $(LATEXOPTS) '$<'
	latex $(LATEXOPTS) '$<'
	-makeindex -s python.ist '$(basename $<).idx'
	latex $(LATEXOPTS) '$<'
	latex $(LATEXOPTS) '$<'

%.pdf: %.tex
	pdflatex $(LATEXOPTS) '$<'
	pdflatex $(LATEXOPTS) '$<'
	pdflatex $(LATEXOPTS) '$<'
	-makeindex -s python.ist '$(basename $<).idx'
	pdflatex $(LATEXOPTS) '$<'
	pdflatex $(LATEXOPTS) '$<'

clean:
	rm -f *.dvi *.log *.ind *.aux *.toc *.syn *.idx *.out *.ilg *.pla

.PHONY: all all-pdf all-dvi all-ps clean
.PHONY: all-pdf-ja

