PDF = cours_python_avance.pdf
SRC = $(shell ls -v src/*/*.md)

FLAGS = --chapters --toc

GEN = $(PDF)

$(PDF):	$(SRC)
	pandoc -V lang=french -V geometry:margin=1in $(SRC) -o $@ $(FLAGS)

clean:
	rm -f $(GEN)

re:	clean $(GEN)

.PHONY:	clean re
