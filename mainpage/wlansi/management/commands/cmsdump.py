import itertools
import optparse
import os

from django.core.management import base
from django.core import serializers
from django.db.models import Q

from cms import models

class Command(base.BaseCommand):
    """
    This class defines a command for manage.py which generates a
    sanitized dump of the mainpage database.
    """
    option_list = base.BaseCommand.option_list + (
        optparse.make_option('--format', default='yaml', dest='format', help='Specifies the output serialization format for fixtures.'),
        optparse.make_option('-a', '--all', default=False, dest='export_all', help="Export all plugins (not only Markup Plugin)."),
    )
    args = "output_file"
    help = "Generates a sanitized dump of the mainpage database."
    
    def handle(self, *args, **options):
        """
        Generates a sanitized dump of the mainpage database.
        """
        if len(args) == 0:
            raise base.CommandError("Missing output file argument!")
        
        export_all = options.get('export_all')
        format = options.get('format')
        
        dest_file = args[0]
        if dest_file != '/':
            dest_file = os.path.join(os.getcwd(), dest_file)
        
        if format not in serializers.get_public_serializer_formats():
            raise base.CommandError("Unknown serialization format: %s" % format)
        
        pages = models.Page.objects.filter(published=True)
        placeholders = itertools.chain(*[page.placeholders.all() for page in pages])
        
        plugins = models.CMSPlugin.objects.filter(placeholder__in=placeholders)
        if not export_all:
            plugins = plugins.filter(plugin_type='MarkupPlugin')
        plugin_objects = [plugin.get_plugin_instance()[0] for plugin in plugins]
        
        all_objects = list(placeholders) + list(pages)
        all_objects += list(itertools.chain(*[page.title_set.all() for page in pages])) + list(plugins) + list(plugin_objects) 
        
        out = open(dest_file, "w")
        out.write(serializers.serialize(format, all_objects))
        out.close()