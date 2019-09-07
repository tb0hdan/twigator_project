.PHONY: tests

all: tests start

tests: deps test-deps piprot err-check-twigator mypy test coverage

deps:
	@pip3 install -r requirements.txt >/dev/null

test-deps:
	@pip3 install -r requirements.test.txt >/dev/null

piprot:
	@piprot; exit 0

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

mypy: test-deps
	@# FIXME: Add --strict after fixing issues
	@printf "Running mypy static checks..."
	@mypy --ignore-missing-imports -p twigator
	@./bin/colorprint.sh green "\t\t\t[✓]\n"

schema:
	@python3 twigator/schemabuilder.py

schema_fixture:
	@python3 twigator/schemabuilder.py > tests/fixtures/schema.yml

cc:
	@echo "Checking cyclomatic complexity..."
	@radon cc twigator/

mi:
	@echo "Checking maintainability index..."
	@radon mi twigator/

purge:
	@docker-compose rm -s -f
