.PHONY: tests

SWAGGER_VERSION = "3.23.8"

ifeq ($(shell uname),Darwin)
    SED = sed -E
    SEDINPLACE = $(SED) -i '' -e
else
    SED = sed -r
    SEDINPLACE = $(SED) -i -e
endif


all: tests start

tests: deps test-deps piprot err-check-twigator mypy test coverage

deps:
	@pip3 install -r requirements.txt >/dev/null

test-deps:
	@pip3 install -r requirements.test.txt >/dev/null

piprot:
	@piprot; exit 0

test-dirs:
	@mkdir -p ./static

test: test-dirs
	@py.test -c ./tests/etc/pytest.ini -v tests/

coverage: test-dirs
	@py.test -c ./tests/etc/pytest.ini --cov=./twigator --cov-config=./tests/etc/coveragerc tests/

coverage_ci:	coverage
	@codeclimate-test-reporter

build: swagger
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

swagger:
	@if [ -f ./twigator/static/swagger/swagger-ui.js ]; then echo "Already downloaded..."; exit 0; fi
	@wget https://github.com/swagger-api/swagger-ui/archive/v$(SWAGGER_VERSION).tar.gz -O /tmp/v$(SWAGGER_VERSION).tar.gz
	@tar -xzpf /tmp/v$(SWAGGER_VERSION).tar.gz  -C /tmp
	@cp /tmp/swagger-ui-$(SWAGGER_VERSION)/dist/* ./twigator/static/swagger/
	@$(SEDINPLACE) '/url/s/https\:\/\/petstore.swagger.io\/v2\/swagger.json/\/schema/g' ./twigator/static/swagger/index.html

swagger-clean:
	@rm ./twigator/static/swagger/*
	@rm -rf /tmp/v$(SWAGGER_VERSION).tar.gz /tmp/swagger-ui-$(SWAGGER_VERSION)
