from setuptools import find_packages, setup

with open('README.md') as fp:
    description = fp.read()

with open('requirements.txt') as fp:
    requirements = fp.read()

setup(
    name='csvdoc',
    version='0.1.0',
    author="Kay Graubmann",
    author_email="kay.graubmann@gmail.com",
    packages=find_packages(),
    license='GPLv3',
    long_description=description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
    install_requires=requirements.splitlines()
)
