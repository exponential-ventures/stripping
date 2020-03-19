build:
	docker build -t k2so.xnv.io/stripping .

test:
	docker run -it --rm k2so.xnv.io/stripping python -m unittest discover -f -v tests

t:
#	docker run -it --rm k2so.xnv.io/stripping python -m unittest -f tests/test_executor_serialization.py
	docker run -it --rm k2so.xnv.io/stripping python -m unittest -f tests/test_weird_bug.py

ssh:
	docker run -it --rm --name stripping k2so.xnv.io/stripping /bin/bash

build_package:
	docker run -v $(shell pwd):/usr/src/app -it --rm k2so.xnv.io/stripping python3 setup.py sdist bdist_wheel