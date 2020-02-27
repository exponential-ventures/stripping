build:
	docker build -t k2so.xnv.io/stripping .

test:
	docker run -it --rm k2so.xnv.io/stripping python -m unittest discover -v tests

ssh:
	docker run -it --rm k2so.xnv.io/stripping /bin/bash

build_package:
	docker run -v $(shell pwd):/usr/src/app -it --rm k2so.xnv.io/stripping python3 setup.py sdist bdist_wheel