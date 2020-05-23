#!/bin/bash

export TWINE_USERNAME="admin"
export TWINE_PASSWORD="IAMwckGYQlRdz1g8Z0rRLA1"
export TWINE_REPOSITORY_URL="https://alexeybeley.jfrog.io/artifactory/api/pypi/pypi-local"
twine upload dist/*
