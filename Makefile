build_folder:
	mkdir -p ./_build

.PHONY: build
build: src_copy
	cd ./_build/src && python3 ./setup.py sdist bdist_wheel

.PHONY: src_copy
src_copy:
	mkdir -p ./_build/src && cp -rf ./src/* ./_build/src && rm -rf ./_build/src/_private

.PHONY: test_copy
test_copy: build_folder
	mkdir -p ./_build/test && cp -rf ./test/* ./_build/test

.PHONY: venv
venv:
	python3 -m venv ./_build/venv && . ./_build/venv/bin/activate && pip3 install -r ./_build/src/art_cli/requirements.txt

.PHONY: test
test: build_folder test_copy src_copy venv
	. ./_build/venv/bin/activate && cd ./_build/test && python3 -m unittest discover

upload: test build
	. ./_build/venv/bin/activate && cd ./_build/src && pip3 install -r ./requirements.txt && ./upload_package.sh

.PHONY: clean
clear: build_folder
	rm -rf ./_build/*


