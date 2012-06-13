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
    args = "<output_file, output_format=yaml>"
    help = "Generates a sanitized dump of the mainpage database."
    
    def handle(self, *args, **options):
        """
        Generates a sanitized dump of the mainpage database.
        """
        if len(args) == 0:
            raise base.CommandError("Missing output file argument!")
        
        out_type = 'yaml'
        if len(args) > 1:
            out_type = args[1]
        if out_type not in ('json', 'yaml', 'xml'):
            raise base.CommandError("Output file format must be json, yaml, or xml!")
    
        dest_file = args[0]
        if dest_file != '/':
            dest_file = os.path.join(os.getcwd(), dest_file)
        
        aditional_ids = ('main', 'contentlicense',)
        pages = models.Page.objects.filter(Q(in_navigation=True) | Q(reverse_id__in=aditional_ids))
        page_ids = [page.id for page in pages]
        
        plugins = models.CMSPlugin.objects.filter(placeholder__page__in=page_ids)
        plugin_objects = [plugin.get_plugin_instance()[0] for plugin in plugins]
        
        all_objects = list(models.Placeholder.objects.filter(page__in=page_ids)) + list(pages)
        all_objects += list(models.Title.objects.filter(page__in=page_ids)) + list(plugins) + list(plugin_objects) 
        
        out = open(dest_file, "w")
        out.write(serializers.serialize(out_type, all_objects))
        out.close()