PDF = cours_python_avance.pdf
MANIFEST = manifest.json
ZIP = cours_python_avance.zip
SRC = $(shell ls -v src/*/*.md)

FLAGS = --chapters --toc

GEN = $(PDF) $(MANIFEST) $(ZIP)

$(PDF):	$(SRC)
	pandoc -V lang=french -V geometry:margin=1in $(SRC) -o $@ $(FLAGS)

$(MANIFEST): $(SRC)
	./gen_manifest.py $(SRC) > $@

$(ZIP): $(MANIFEST) $(SRC)
	zip $@ $^

clean:
	rm -f $(GEN)

re:	clean $(GEN)

.PHONY:	clean re
