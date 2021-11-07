
.PHONY: all clean

all:
	@echo 'DONE'

clean:
	@rm -fv presentation_*/*.{aux,bbl,blg,log,nav,out,snm,synctex.gz,toc}
