import setuptools
import os

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setuptools.setup(
    name='phrasal',
    version='0.0.1',
    author='Lucy Linder',
    author_email='lucy.derlin@gmail.com',
    license='Apache License 2.0',
    description='NLP tools to extract, normalize and filter sentences from text/HTML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/derlin/phrasal',

    # install all packages found under src/
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src', exclude=['showcase']),

    # include other files such as html, css, etc
    include_package_data=True,  # read from MANIFEST.in
    zip_safe=True,  # not safe if the library needs to read package data from os (path is different from a zip)

    python_requires='>=3.6',

    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ),

    # regular dependencies
    install_requires=[
        'requests>=2.22,<2.23',
        'regex>=2020.1, <2020.2',
        'bs4',
        'justext==2.2.0',
        'ftfy>=5.6',
        'pyyaml>=5.3',
        'get-html',
    ],
    # extra dependencies
    extras_require={
        'showcase': ['streamlit']
    }
)
