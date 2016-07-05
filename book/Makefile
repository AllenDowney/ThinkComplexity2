F = thinkcomplexity2
DEST = /home/downey/public_html/greent/complexity2

all:	book.tex
	pdflatex book
	makeindex book.idx
	pdflatex book
	mv book.pdf $(F).pdf
	evince $(F).pdf

hevea:	book.tex header.html footer.html
	cp book.tex $(F).tex
	pdflatex $(F)
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

