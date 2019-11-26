build:
	docker build -f docker/Dockerfile -t stripping .


test-sidecar-up:
	docker network create catalysis || true
	docker run -d --name server --net catalysis catalysis_proxy

test-sidecar-down:
	docker rm -f server
	docker network rm catalysis

test:
	$(MAKE) test-sidecar-down || true
	$(MAKE) test-sidecar-up
	docker run -it --rm --net catalysis stripping:latest python -m unittest discover -v -f  tests
	$(MAKE) test-sidecar-down

unit-test-with_catalysis:
	$(MAKE) test-sidecar-down || true
	$(MAKE) test-sidecar-up
	docker run -it --rm --net catalysis stripping:latest python -m unittest -v -f $(test_name)
	$(MAKE) test-sidecar-down

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

clean-pyc:
	find . -path "*.pyc"  -delete