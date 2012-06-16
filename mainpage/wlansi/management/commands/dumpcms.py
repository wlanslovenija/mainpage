import itertools, optparse, os

from django.core.management import base
from django.core import serializers

from cms import models

class Command(base.NoArgsCommand):
    """
    This class defines a command for manage.py which generates a
    dump of Django CMS database.
    """

    option_list = base.BaseCommand.option_list + (
        optparse.make_option('--format', default='yaml', dest='format', help="Specifies the output serialization format for the dump."),
        optparse.make_option('--indent', default=None, dest='indent', type='int', help="Specifies the indent level to use when pretty-printing output."),
        optparse.make_option('-n', '--natural', action='store_true', default=False, dest='use_natural_keys', help="Use natural keys if they are available."),
        optparse.make_option('-a', '--all', action='store_true', default=False, dest='export_all', help="Export all plugins (not only Markup plugin)."),
    )
    help = "Generates a dump of Django CMS database."
    
    def handle_noargs(self, **options):
        """
        Generates a dump of Django CMS database.
        """

        format = options.get('format')
        indent = options.get('indent')
        use_natural_keys = options.get('use_natural_keys')
        export_all = options.get('export_all')
        show_traceback = options.get('traceback')

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in serializers.get_public_serializer_formats():
            raise base.CommandError("Unknown serialization format: %s" % format)

        try:
            serializers.get_serializer(format)
        except KeyError:
            raise CommandError("Unknown serialization format: %s" % format)

        pages = models.Page.objects.filter(published=True)
        placeholders = models.Placeholder.objects.filter(page__in=pages)
        
        plugins = models.CMSPlugin.objects.filter(placeholder__in=placeholders)
        if not export_all:
            plugins = plugins.filter(plugin_type='MarkupPlugin')
        plugin_objects = [plugin.get_plugin_instance()[0] for plugin in plugins]
        
        objects = itertools.chain(
            placeholders,
            pages,
            itertools.chain(*[page.title_set.all() for page in pages]),
            plugins,
            plugin_objects,
        )
        
        try:
            return serializers.serialize(format, objects, indent=indent, use_natural_keys=use_natural_keys)
        except Exception, e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)
