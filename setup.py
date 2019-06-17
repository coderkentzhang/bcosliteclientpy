#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)


def merge_lists(base_list, *other_lists):
    new_list = base_list[:]

    for other_list in other_lists:
        new_list.extend(i for i in other_list if i not in new_list)

    return new_list


HYPOTHESIS_REQUIREMENT = "hypothesis>=3.6.1"

extras_require = {}
extras_require['tools'] = [
    HYPOTHESIS_REQUIREMENT,
]
extras_require['test'] = merge_lists(
    [
        "pytest==4.4.1",
        "pytest-pythonpath>=0.7.1",
        "pytest-xdist==1.22.3",
        "tox>=2.9.1,<3",
        HYPOTHESIS_REQUIREMENT,
    ],
    extras_require['tools'],
)
extras_require['lint'] = [
    "flake8==3.4.1",
    "isort>=4.2.15,<5",
    "mypy==0.620",
]
extras_require['doc'] = [
    "Sphinx>=1.6.5,<2",
    "sphinx_rtd_theme>=0.1.9",
]
extras_require['dev'] = merge_lists(
    [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
		"cytoolz",
		"toolz",
		"hexbytes",
		"requests",
		"attrdict",
		"Crypto",
    ],
    extras_require['test'],
    extras_require['lint'],
    extras_require['doc'],
)

setup(
    name='bcosliteclientpy',
    version='0.1.0',
    description="""bcosliteclientpy""",
    long_description_markdown_filename='README.md',
    author='',
    author_email='',
    url='',
    include_package_data=True,
    install_requires=[
        'parsimonious>=0.8.0,<0.9.0',
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    py_modules=['bcosliteclientpy'],
    license="MIT",
    zip_safe=False,
    keywords='ethereum',
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={'bcosliteclientpy': ['py.typed']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
