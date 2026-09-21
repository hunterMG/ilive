import setuptools
from ilive import version

with open("README.md", "r", encoding = 'utf-8') as fh:
    long_description  =  fh.read()

REQ  =  ['PyExecJS', 'requests']

setuptools.setup(
    name = "ilive",
    version = version.__version__,
    description = version.__descriptrion__,
    author = "hunterMG",
    license = "AGPL-3.0-or-later",
    license_expression = "AGPL-3.0-or-later",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/hunterMG/ilive",
    project_urls = {
        "Upstream": "https://github.com/nICEnnnnnnnLee/LiveRecorder",
    },
    install_requires = REQ,
    zip_safe = True,
    packages = setuptools.find_packages(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video"
    ],
    entry_points={
        "console_scripts": ["ilive=ilive.__main__:main"]
    },
)
