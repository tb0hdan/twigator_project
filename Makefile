.PHONY: tests

all: tests start

tests: deps test-deps err-check-twigator-debug test coverage

deps:
	@pip3 install -r requirements.txt

test-deps:
	@pip3 install -r requirements.test.txt

test:
	@py.test -c ./tests/etc/pytest.ini -v tests/

coverage:
	@py.test -c ./tests/etc/pytest.ini --cov=./twigator --cov-config=./tests/etc/coveragerc tests/

coverage_ci:	coverage
	@codeclimate-test-reporter

build:
	@docker-compose build --build-arg TWITTER_CONSUMER_KEY=$${TWITTER_CONSUMER_KEY} --build-arg TWITTER_CONSUMER_SECRET=$${TWITTER_CONSUMER_SECRET}

start: build
	@docker-compose up -d

start-debug: build
	@docker-compose up

stop:
	@docker-compose stop

err-check-twigator:
	@printf "Checking twigator... "
	@if [ "$(shell pylint twigator/|egrep '(syntax-error|import-error)')" != "" ]; then exit 1; fi
	@./bin/colorprint.sh green "\t\t\t[✓]\n"

err-check-twigator-debug:
	@pylint twigator/

metrics: test-deps cc mi

cc:
	@echo "Checking cyclomatic complexity..."
	@radon cc twigator/

mi:
	@echo "Checking maintainability index..."
	@radon mi twigator/

purge:
	@docker-compose rm -s -f
