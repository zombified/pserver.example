# This make file assumes that you have a virtualenv at the location `./env`
VENV=./env

bootstrap:
	# directory used for data.fs and related files in this example
	mkdir -p var
	# install dependencies
	$(VENV)/bin/pip install -r requirements.txt
	# make sure to install your app into your environment ;)
	$(VENV)/bin/python setup.py develop

setup:
	# create your initial site in the selected database
	curl -X POST -H "Accept: application/json" --user root:admin -H "Content-Type: application/json" -d '{"@type": "Container","title": "Guillotina 1","id": "guillotina1","description": "Description"}' "http://127.0.0.1:8080/db/"

create_custom_type:
	# create an object of type CustomType and store it at the root
	curl -X POST -H "Accept: application/json" --user root:admin -H "Content-Type: application/json" -d '{"@type":"CustomType","title":"Custom Type 1","id":"customtype1","example.behaviors.ICustomBehavior":{"bar":"changed"}}' "http://127.0.0.1:8080/db/guillotina1/"

modify_custom_behavior_content:
	# this will change the data in the custom behavior for the object created
	# with the `create_custom_type` target
	#
	# For more info about commands, SEE: http://guillotina.readthedocs.io/en/latest/developer/behavior.html#dynamic-behaviors
	curl -X PATCH -H "Accept: application/json" --user root:admin -H "Content-Type: application/json" -d '{"example.behaviors.ICustomBehavior":{"bar":"value is now different"}}' "http://127.0.0.1:8080/db/guillotina1/customtype1"


# some docker related things to make it quicker to launch
start_db:
	docker-compose up -d db

build_and_start_web:
	docker-compose build web && docker-compose run --no-deps --service-ports --rm web


.PHONY: bootstrap setup createcustomtype modify_custom_behavior_content start_db build_and_start_web
