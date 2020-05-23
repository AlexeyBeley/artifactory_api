test:

build:
mkdir build
cp src build
python setup.py sdist upload -r https://alexeybeley.jfrog.io/pypi-local

upload (build, test):
python get_version
check version
if no env vars user/pass raise
