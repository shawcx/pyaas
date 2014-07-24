
# Dirty OS X hack
PATH := $(PATH):/usr/local/bin

COFFEE = PATH=$(PATH) coffee
LESS = PATH=$(PATH) lessc

JS_OUT = share/static/js/example.js
JS_SRC = src/coffee/example.litcoffee \
         src/coffee/util.litcoffee

CSS_OUT = share/static/css/example.css
CSS_SRC = src/less/example.less

all: $(JS_OUT) $(CSS_OUT)

$(JS_OUT): $(JS_SRC)
	$(COFFEE) -j $(JS_OUT) -c $(JS_SRC)

$(CSS_OUT): $(CSS_SRC)
	$(LESS) -x --no-color --include-path=less/external $< $@

clean:

distclean: clean
	@rm -f $(JS_OUT) $(CSS_OUT)

