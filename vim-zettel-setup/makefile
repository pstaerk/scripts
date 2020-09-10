# SOURCES := $(wildcard *.md)
# OBJECTS := $(patsubst %.md, ../markdown_html/%.html, $(SOURCES)))

# htmldir=../markdown_html

# all:
# 	python3 convert_zettels.py

OUTPUT=../markdown_html
MARKDOWNS=$(wildcard *.md)
HTMLS=$(patsubst %.md, $(OUTPUT)/%.html, $(MARKDOWNS))

.PHONY : all

all : $(HTMLS)

$(OUTPUT)/%.html : %.md	
	python3 convert_zettel.py -c $<

clean: 
	rm ../markdown_html/*.html
