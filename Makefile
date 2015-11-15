PDF = cours_python_avance.pdf
ZIP = cours_python_avance.zip
SRC = $(shell ls -v src/*/*.md)

FLAGS = --chapters --toc

GEN = $(PDF) $(ZIP)

$(PDF):	$(SRC)
	pandoc -V lang=french -V geometry:margin=1in $(SRC) -o $@ $(FLAGS)

$(ZIP): $(SRC)
	./gen_archive.py $@ $^

clean:
	rm -f $(GEN)

re:	clean $(GEN)

.PHONY:	clean re
