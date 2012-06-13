ALL: xmp16.pdf

%.pdf: %.tex Makefile
	pdflatex --shell-escape --synctex=1 --enable-write18 $< &&	pdflatex $< && pdflatex $<

clean:
	  rm -f *.aux *.bbl *.blg *.log *.synctex.gz *.nav *.snm *.out *.toc xmp16.pdf
