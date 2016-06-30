all:	book.tex
	pdflatex book
	makeindex book.idx
	pdflatex book
	mv book.pdf thinkcomplexity.pdf
	evince thinkcomplexity.pdf

hevea:
	# replace the pdfs with eps
	sed s/.pdf/.eps/g book.tex > temp.tex
	sed s/.jpg/.eps/g temp.tex > thinkcomplexity.tex
	latex thinkcomplexity
	rm -rf html
	mkdir html
	hevea -O -e latexonly htmlonly thinkcomplexity
# the following greps are a kludge to prevent imagen from seeing
# the definitions in latexonly, and to avoid headers on the images
	grep -v latexonly thinkcomplexity.image.tex > a; mv a thinkcomplexity.image.tex
	grep -v fancyhdr thinkcomplexity.image.tex > a; mv a thinkcomplexity.image.tex
	imagen -png thinkcomplexity
	hacha thinkcomplexity.html
	cp up.png next.png back.png html
	mv index.html thinkcomplexity.css thinkcomplexity*.html thinkcomplexity*.png *motif.gif html

DEST = /home/downey/public_html/greent/complexity

distrib:
	rm -rf dist
	mkdir dist dist/tex dist/tex/figs
	rsync -a thinkcomplexity.pdf html dist
	rsync -a Makefile book.tex latexonly htmlonly dist/tex
	rsync -a figs/*.fig figs/*.eps dist/tex/figs
	cd dist; zip -r complexity.tex.zip tex; rm -r tex
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
	rsync -a thinkcomplexity.pdf $(OREILLY)/pdf

clean:
	rm -f *~ *.aux *.log *.dvi *.idx *.ilg *.ind *.toc

