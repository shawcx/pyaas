
# Dirty OS X hack
PATH := $(PATH):/usr/local/bin

COFFEE = PATH=$(PATH) coffee
LESSC = PATH=$(PATH) lessc

JS_OUT = share/static/js/example.js
JS_SRC = src/example.litcoffee \

CSS_OUT = share/static/css/example.css
CSS_SRC = src/example.less

all: $(JS_OUT) $(CSS_OUT)

$(JS_OUT): $(JS_SRC)
	$(COFFEE) -o `dirname $(JS_OUT)` -m -c $(JS_SRC)

$(CSS_OUT): $(CSS_SRC)
	$(LESSC) -x --no-color --include-path=src/external $< $@

clean:

distclean: clean
	@rm -f $(JS_OUT) $(CSS_OUT)

