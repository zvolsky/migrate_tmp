# -*- coding: utf-8 -*-

from distutils.core import setup

readme_file = open('README.rst')

setup(
    name='django-migrate-file-storage',
    version='0.1.0',
    author='Mirek Zvolský',
    author_email='zvolsky@seznam.cz',
    packages=['migrate_file_storage'],
    url='https://github.com/zvolsky/migrate_file_storage',
    download_url='https://github.com/zvolsky/migrate_file_storage'
                 '/tarball/0.1.0',
    description="Export media files into standard Django FILE_STORAGE or migrate them between "
                "different file storage systems. (Initially django-db-file-storage is supported.)",
    long_description=readme_file.read(),
    install_requires=[
        'Django',
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

readme_file.close()
