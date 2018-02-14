# -*- coding: utf-8 -*-

"""
    Copies media files from file system into database
    see parser.description in class Command bellow
"""

import argparse
import importlib
import os
import re

from django.conf import settings  # proper settings must be found (search for DJANGO_SETTINGS_MODULE or --settings= in Django docs
from django.core.management.base import BaseCommand
from django.db.models.base import ModelBase
from django.db.models.fields import files
from django.db.models import FileField


_ = lambda x: x   # from django.utils.translation import ugettext_lazy as _

BASE_DIR = getattr(settings, "BASE_DIR")              # BASE_DIR must be in your settings.py
INSTALLED_APPS = getattr(settings, "INSTALLED_APPS")  # INSTALLED_APPS must be in your settings.py
FIELDS_FILE = os.path.join(BASE_DIR, 'files2db-fields')


def list(app_names):
    fields = []
    app_names = set(app_names)
    for app in app_names:
        if app in INSTALLED_APPS:
            try:
                app_models = importlib.import_module(app + '.models')
            except ImportError:
                print(_("models.py not found in %s. You can try temporary copy models.py into application root.") % app)
            for attr_name in dir(app_models):
                maybe_model = getattr(app_models, attr_name)
                if type(maybe_model) == ModelBase:
                    for fld in maybe_model._meta.get_fields():
                        if issubclass(type(fld), FileField):  # FileField, ImageField
                            prefix = ('#probably-already-in-db# '
                                      if re.match('^\w+\.\w+/\w+/\w+/\w+$', fld.upload_to) else '')
                            fields.append('%s%s %s %s' % (prefix, app, attr_name, fld.name))
        else:
            print(_("%s not in INSTALLED_APPS") % app)

    if fields:
        fields.insert(0, '# This list was created using "./manage.py files2db --list".')
        fields.insert(1, '# Do not remove or rewrite this file after the conversion into the database. It contains original paths useful for export.')
        fields.insert(2, '')
        fields.insert(3, '# Uncommented lines will be used during conversions and export. Add "#..." to skip such line(s).')
        fields.insert(4, '')
        fields.insert(5, '# Conversion from FS into db: a) change models and migrate, b) ./manage.py files2db --files2db')
        fields.insert(6, '# Export media from db: a) fix/change destination paths here bellow, b) ./manage.py db2files --export')
        fields.insert(7, '# Conversion from db into FS: a) ./manage.py db2files --export, b) change models and migrate, c) "./manage.py db2files --db2files".')
        fields.insert(8, '#    WARNING: during --export DO NOT USE DIFFERENT PATHS (here bellow) as you plan have in the changed model.')
        fields.insert(9, '#             (You should however omit date modifiers if you plan use them. Only ending date modifiers are supported.)')
        fields.insert(10, '#             db_file_storage-style paths ARE ALLOWED TOO (as generated with --list if you already have db fields).')
        fields.insert(11, '#             However other (completely different) paths will probably break the conversion!')
        fields.insert(12, '')
        fields.insert(13, '# application - model - field - path')
        fields.insert(14, '# ' + 80 * '-')
        fields.insert(15, '')
        if os.path.isfile(FIELDS_FILE):
            os.remove(FIELDS_FILE)
        with open(FIELDS_FILE, 'w') as f:
            for field in fields:
                f.write(field + os.linesep)



def convert(app_names):
    if os.path.isfile(FIELDS_FILE):
        print(5*'OK ')
    else:
        print(_("Text files from 1st phase aren't located in the BASE_DIR. Use with --help to read more."))


class Command(BaseCommand):
    help = _("Backup information about File(Image)Fields and stored media files into descriptive text files.")

    def add_arguments(self, parser):
        parser.formatter_class = argparse.RawTextHelpFormatter
        parser.description = """
            ------------------------------------------------------------
            Copies media files from file system into database

            manage.py files2db app_name [app_name2 [...]]
            Run with app_names as the 1st step before the model change and before the migration; this will create 2 textfiles
                files2db-fields  this is list of all fields found on the django site; fields on uncommented lines will be copied
                files2db-files   this is (internal) list of media files and id's; based on it the import will apply later

            Then change the model for django-db-file-storage and run makemigrations + migrate
            Do not remove MEDIA_ROOT, otherwise files from files2db-files cannot be found

            manage.py files2db -c | --convert
            Run with --convert as the 2nd step to copy files into database

            Now check the results
            Then you can remove MEDIA_ROOT in settings.py, remove (or backup) media files and remove files2db-fields, files2db-files
            ------------------------------------------------------------
        """

        #parser.add_argument('app_names', nargs='*', type=str, help=_("use this in 1st phase: 1 or more (separate with spaces) applications, where we plan copy the media files into db"))
        #parser.add_argument('-l', '--list-fields', action="store_true", help=_("use this as 2nd phase after the migration to copy files into db based on the descriptive text files"))
        #parser.add_argument('-d', '--files2db', action="store_true", help=_("use this as 2nd phase after the migration to copy files into db based on the descriptive text files"))

    def handle(self, *_args, **options):
        app_names = options.get('app_names')
        doit = options.get('convert')
        if not doit and app_names:
            prepare(app_names)
        elif doit and not app_names:
            doit()
        else:
            print(_("use with --help for info"))


'''
class Command(BaseCommand):
    help = _("Copies media files from file system into database.")

    def add_arguments(self, parser):
        parser.add_argument('app_names', nargs='*', type=str, help=_("use this in 1st phase: 1 or more (separate with spaces) applications, where we plan copy the media files into db"))
        parser.add_argument('-l', '--list', action="store_true", help=_("use this as 2nd phase after the migration to copy files into db based on the descriptive text files"))
        parser.add_argument('-f', '--db2files', action="store_true", help=_("use this as 2nd phase after the migration to copy files into db based on the descriptive text files"))
        parser.add_argument('-p', '--files2paths', action="store_true", help=_("use this as 2nd phase after the migration to copy files into db based on the descriptive text files"))
'''
