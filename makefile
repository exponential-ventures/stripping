build:
	docker build  -f docker/Dockerfile -t stripping .

test:
	docker run -it --rm stripping python -m unittest -v -f tests

build-example:
	docker build  -f docker/example/Dockerfile -t stripping-example .

# Eg make run-example black_friday
run-example:
	grep -l  $(word 2, $(MAKECMDGOALS) ) ./examples/*.py |  xargs -n 1 docker run --rm stripping-example python

ssh:
	docker run -it --rm stripping /bin/bash