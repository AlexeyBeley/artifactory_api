# For users

1) Install
   `pip3 install art_cli -i https://alexeybeley.jfrog.io/artifactory/api/pypi/pypi-local/simple`
2) Create a runner for example:
   cat ./art_cli.py
   ```python

   #!/python3
   from art_cli.artifactory_cli import main
   main()
   ```
3) First thing - you have to configure it.
   See the example .json file for configuration 
   run `./art_cli.py configure -f <file_path>`
4) As an option you can put it as `+x` under `/usr/bin` and run it from console directly

# For developers how to use Makefile:

# `make upload`
build, test and upload the package

# `make build`
build the package under `_build`

# `make clear`
delete all _build data

# `make test`
run this command to test your package before uploading.

# todo:
1) Make it interactive (while loop)
2) Add option to interactive user intput (e.g. user-create should accept json from stdin).
3) Function to upload the package. So the `make upload` will use it.
4) Add __version__ under packages __init__.py