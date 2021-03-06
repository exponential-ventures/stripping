build:
	docker build -t k2so.xnv.io/stripping .

test:
	docker run -it --rm k2so.xnv.io/stripping python -m unittest discover -f -v tests

ssh:
	docker run -it --rm --name stripping k2so.xnv.io/stripping /bin/bash

build_package:
	docker run -v $(shell pwd):/usr/src/app -it --rm k2so.xnv.io/stripping python3 setup.py sdist bdist_wheel
	scp -r dist/* robot@l337:/home/robot/pypi_server/packages
	sudo rm -rf build/ dist/ stripping.egg-info