PDFFLAGS = -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress \
           -dCompressPages=true -dUseFlateCompression=true  \
           -dEmbedAllFonts=true -dSubsetFonts=true -dMaxSubsetPct=100

F = thinkcomplexity2
DEST = /home/downey/public_html/greent/complexity2

all:	book.tex
	pdflatex $(PDFFLAGS) book
	makeindex book.idx
	pdflatex $(PDFFLAGS) book
	mv book.pdf $(F).pdf
	evince $(F).pdf

hevea:	book.tex header.html footer.html
	cp book.tex $(F).tex
	pdflatex $(PDFFLAGS) $(F)
	hevea -O -e latexonly htmlonly $(F).tex
	imagen -png -pdf $(F)
	hacha $(F).html
	rm -rf html
	mkdir html
	cp up.png next.png back.png html
	mv index.html $(F).css $(F)*.html $(F)*.png html

distrib:
	rm -rf dist
	mkdir dist
	rsync -a $(F).pdf html dist
	rsync -a dist/* $(DEST)
	chmod -R o+r $(DEST)/*
	cd $(DEST)/..; sh back

plastex:
	# Before running plastex, we need the current directory in PYTHONPATH
	# export PYTHONPATH=$PYTHONPATH:.
	python Filist.py book.tex > book.plastex
	rm -rf /home/downey/complexity/trunk/book
	plastex --renderer=DocBook --theme=book --image-resolution=300 --filename=book.xml book.plastex
	rm -rf /home/downey/complexity/trunk/book/.svn

diff:
	diff book/book.xml /home/downey/complexity/branches/manuscript.1.1/book/book.xml > patch

xxe:
	~/Downloads/xxe-perso-4_8_0/bin/xxe book/book.xml

OREILLY = /home/downey/oreilly/complexity

oreilly:
	rsync -a book/ $(OREILLY)
	rsync -a figs/* $(OREILLY)/figs
	rsync -a $(F).pdf $(OREILLY)/pdf

clean:
	rm -f *~ *.aux *.log *.dvi *.idx *.ilg *.ind *.toc

pdfpextr = \
    gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
       -dFirstPage=$(1) \
       -dLastPage=$(2) \
       -sOutputFile=$(4) \
       $(3)

split:
	$(call pdfpextr,5,16,thinkcomplexity2.pdf,chap00.pdf)
	$(call pdfpextr,17,26,thinkcomplexity2.pdf,chap01.pdf)
	$(call pdfpextr,27,42,thinkcomplexity2.pdf,chap02.pdf)
	$(call pdfpextr,43,62,thinkcomplexity2.pdf,chap03.pdf)
	$(call pdfpextr,63,82,thinkcomplexity2.pdf,chap04.pdf)
	$(call pdfpextr,83,104,thinkcomplexity2.pdf,chap05.pdf)
	$(call pdfpextr,105,118,thinkcomplexity2.pdf,chap06.pdf)
	$(call pdfpextr,119,134,thinkcomplexity2.pdf,chap07.pdf)
	$(call pdfpextr,135,156,thinkcomplexity2.pdf,chap08.pdf)
	$(call pdfpextr,157,174,thinkcomplexity2.pdf,chap09.pdf)
	$(call pdfpextr,175,186,thinkcomplexity2.pdf,chap10.pdf)
	$(call pdfpextr,191,208,thinkcomplexity2.pdf,app01.pdf)

