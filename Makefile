PDF = cours_python_avance.pdf
ZIP = cours_python_avance.zip
SRC = $(shell find src -name "*.md" | sort -n)

FLAGS = --top-level-division=part --toc

GEN = $(PDF) $(ZIP)

$(PDF):	title.md $(SRC)
	pandoc -V lang=fr -V geometry:margin=1in -V colorlinks=true $^ -o $@ $(FLAGS)

$(ZIP): $(SRC)
	./gen_archive.py $@ $^

clean:
	rm -f $(GEN)

re:	clean $(GEN)

.PHONY:	clean re
