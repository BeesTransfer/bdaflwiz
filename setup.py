import os
from distutils.command.install import INSTALL_SCHEMES
from distutils.command.sdist import sdist
from distutils.core import setup
from bdaflwiz import __author__, __email__, __version__


for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


DOCS_DIR = os.path.join(os.getcwd(), "docs")


def get_doc_files():
        doc_files = []
        build_dir = os.path.join(DOCS_DIR, "build", "html")
        for root, subFolders, files in os.walk(build_dir):
            for file_ in files:
                doc_files.append(os.path.join(root, file_))
        return doc_files
DOC_FILES = get_doc_files()


# The long description to be added to the package descriptor:
DESCRIPTION_TEXT = open("README.rest").read()


# The license text to be added to the package descriptor:
LICENSE_TEXT = open("LICENSE.txt").read()


class CustomSourceDistribution(sdist):
    def build_docs(self):
        """Build documentation before packaging."""
        os.system("cd %s && make clean html" % DOCS_DIR)

    def run(self):
        self.build_docs()
        sdist.run(self)  # old style class


setup(
    name="bdaflwiz",
    version=__version__,
    url="https://github.com/beesdom/bdaflwiz",
    author=__author__,
    author_email=__email__,
    license=LICENSE_TEXT,
    packages=["bdaflwiz"],
    package_data={},
    data_files=[
        ("bdaflwiz", ["CHANGES.txt", "LICENSE.txt", "README.rest"]),
        ("bdaflwiz/docs", DOC_FILES),
    ],
    description="Python Module for track and trace of AFL Deliveries",
    long_description=DESCRIPTION_TEXT,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
    ],
    install_requires=[
        "python-dateutil==1.5"
    ],
    cmdclass={'sdist': CustomSourceDistribution}
)
