build:
	docker build -t k2so.xnv.io/stripping .

test:
	docker run -it --rm k2so.xnv.io/stripping python -m unittest discover -v tests

ssh:
	docker run -it --rm k2so.xnv.io/stripping /bin/bash
