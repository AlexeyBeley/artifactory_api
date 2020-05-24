import setuptools

with open("./README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h_art_cli",
    version="1.0.4",
    author="Horey",
    author_email="alexey.beley@gmail.com",
    description="Artifactory API CLI package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://alexeybeley.jfrog.io/pypi-local",
    packages=setuptools.find_packages(include=["art_cli"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)