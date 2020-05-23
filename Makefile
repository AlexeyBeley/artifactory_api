build_folder:
	mkdir -p ./_build

build: build_folder
	cp -r ./src ./_build/src
	cd ./_build/src && python ./setup.py sdist bdist_wheel

clear: build_folder
	rm -rf ./build/*


#upload (build, test):
#python get_version
#check version
#if no env vars user/pass raise
#export TWINE_USERNAME="admin"
#export TWINE_PASSWORD="IAMwckGYQlRdz1g8Z0rRLA1"
#export TWINE_REPOSITORY_URL="https://alexeybeley.jfrog.io/artifactory/api/pypi/pypi-local"
#twine upload dist/*
