test:

build:
mkdir build
cp src build
build setup

upload (build, test):
python get_version
check version
if no env vars user/pass raise
