# import secrets stored in .env to Makefile
include .env
export

default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: start
start: # Start a local development server
	uvicorn src.api:app --reload --port 9001 --log-level debug

.PHONY: format
format: # Sort imports and format the entire project dir using ruff
	ruff check --select I --fix .
	ruff format .