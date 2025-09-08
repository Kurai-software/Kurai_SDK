#!/usr/bin/env python3
"""
Setup script para Kurai SDK
===========================

Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.
"""

from setuptools import setup, find_packages
import os

def read_file(filename):
    """Lee un archivo del directorio actual"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def read_requirements():
    """Lee los requirements desde requirements.txt"""
    content = read_file('requirements.txt')
    if content:
        return [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
    return ['requests>=2.25.0']

setup(
    name="kurai-sdk",
    version="1.0.0",
    author="Lexia Team",
    author_email="dev@lexia.la",
    description="Cliente oficial para la API pública de Lexia",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/lexia/kurai-sdk",
    project_urls={
        "Homepage": "https://lexia.la",
        "Documentation": "https://docs.lexia.la/sdk",
        "Source Code": "https://github.com/lexia/kurai-sdk",
        "Bug Reports": "https://github.com/lexia/kurai-sdk/issues",
        "Company": "https://lexia.la",
    },
    packages=find_packages(exclude=['tests*', 'examples*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Natural Language :: Spanish",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'responses>=0.18.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.812',
            'twine>=3.0',
            'build>=0.7.0',
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme>=1.0',
            'myst-parser>=0.15',
        ]
    },
    entry_points={
        'console_scripts': [
            'kurai=kurai.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'kurai': ['*.json', '*.yaml', '*.txt'],
    },
    zip_safe=False,
    keywords=[
        'lexia', 'kurai', 'api', 'sdk', 'client', 'automation', 
        'document-processing', 'ai', 'artificial-intelligence',
        'rpa', 'workflow', 'business-automation'
    ],
    license="Proprietary",
    platforms=['any'],
    maintainer="Lexia Team",
    maintainer_email="dev@lexia.la",
    license_files=('LICENSE',),
)