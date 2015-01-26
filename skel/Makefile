
# Dirty OS X hack
PATH := $(PATH):/usr/local/bin

COFFEE = PATH="$(PATH)" coffee
LESS = PATH="$(PATH)" lessc

STATIC_ROOT = share/example/static

COFFEE_FILES := $(wildcard src/*.litcoffee)
JS_FILES := $(patsubst src/%.litcoffee, $(STATIC_ROOT)/js/%.js, $(COFFEE_FILES))

CSS_OUT = share/example/static/css/example.css
CSS_SRC = src/example.less

all: $(JS_FILES) $(CSS_OUT)

$(STATIC_ROOT)/js/%.js: src/%.litcoffee
	$(COFFEE) -o `dirname $@` -m -c $<

$(CSS_OUT): $(CSS_SRC)
	$(LESS) -x --no-color --include-path=src/external $< $@

clean:
	@find . -type f -name \*.pyc -exec rm {} +

distclean: clean
	@rm -f $(JS_FILES) $(CSS_OUT)

