build:
	docker build -f docker/Dockerfile -t stripping .

test:
	docker run -it --rm stripping python -m unittest -v -f tests

# Run specific tests by calling like such:
# make test_name=tests.test_cache_with_catalysis unit-test
unit-test:
	docker run -it --rm stripping python  -m unittest -v $(test_name)

# Run specific script by calling like such:
# make script_name=tests.test_cache_with_catalysis script
script:
	docker run -it --rm stripping python  $(script_name)

build-example:
	docker build  -f docker/example/Dockerfile -t stripping-example .

# Eg make run-example black_friday
run-example:
	grep -l  $(word 2, $(MAKECMDGOALS) ) ./examples/*.py |  xargs -n 1 docker run --rm stripping-example python

# Run specific script by calling like such:
# make script_name=tests.test_cache_with_catalysis example-script
example-script:
	docker run -it --rm stripping-example python  $(script_name)


ssh:
	docker run -it --rm stripping /bin/bash