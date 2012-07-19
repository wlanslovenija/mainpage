import itertools, optparse

from django.contrib.sites import models as sites_models
from django.core.management import base
from django.core.management.commands import dumpdata
from django.core import serializers
from django.db.models import Q

from cms import models as cms_models

from filer import models as filer_models

from cmsplugin_blog import models as blog_models

from cmsplugin_filer_image import models as filer_image_models

class Command(base.NoArgsCommand):
    """
    This class defines a command for manage.py which generates a
    dump of Django CMS database.
    """

    option_list = base.BaseCommand.option_list + (
        optparse.make_option('--format', default='yaml', dest='format', help="Specifies the output serialization format for the dump."),
        optparse.make_option('--indent', default=None, dest='indent', type='int', help="Specifies the indent level to use when pretty-printing output."),
        optparse.make_option('-n', '--natural', action='store_true', default=False, dest='use_natural_keys', help="Use natural keys if they are available."),
    )
    help = "Generates a dump of Django CMS database."
    
    def handle_noargs(self, **options):
        """
        Generates a dump of Django CMS database.
        """

        format = options.get('format')
        indent = options.get('indent')
        use_natural_keys = options.get('use_natural_keys')
        show_traceback = options.get('traceback')

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in serializers.get_public_serializer_formats():
            raise base.CommandError("Unknown serialization format: %s" % format)

        try:
            serializers.get_serializer(format)
        except KeyError:
            raise base.CommandError("Unknown serialization format: %s" % format)

        pages = cms_models.Page.objects.filter(published=True)
        placeholders = cms_models.Placeholder.objects.filter(page__in=pages)

        blog_entries = blog_models.Entry.published.all()
        blog_placeholders = cms_models.Placeholder.objects.filter(entry__in=blog_entries)

        plugins = cms_models.CMSPlugin.objects.filter(Q(placeholder__in=placeholders) | Q(placeholder__in=blog_placeholders))

        def plugin_objects():
            for plugin in plugins:
                instance = plugin.get_plugin_instance()[0]
                if instance is None:
                    raise base.CommandError("Invalid plugin instance: %s from placeholder %s" % (plugin.pk, plugin.placeholder.pk))
                yield instance
        
        objects = itertools.chain(
            sites_models.Site.objects.all(),
            placeholders,
            pages,
            cms_models.Title.objects.filter(page__in=pages),
            blog_placeholders,
            blog_entries,
            blog_models.EntryTitle.objects.filter(entry__in=blog_entries),
            plugins,
            plugin_objects(),
            filer_models.Folder.objects.all(),
            filer_models.File.objects.non_polymorphic().filter(is_public=True),
            filer_models.Image.objects.non_polymorphic().filter(is_public=True),
            filer_image_models.ThumbnailOption.objects.all(),
        )
        
        try:
            return serializers.serialize(format, objects, indent=indent, use_natural_keys=use_natural_keys)
        except Exception, e:
            if show_traceback:
                raise
            raise base.CommandError("Unable to serialize database: %s" % e)

def get_dependencies(models):
    """
    Function to help finding model dependencies.
    """

    all_models = set()

    to_process = models
    while len(to_process):
        new_to_process = []
        for model in to_process:
            if model in all_models:
                continue

            all_models.add(model)

            for field in model._meta.fields:
                if hasattr(field.rel, 'to'):
                    new_to_process.append(field.rel.to)
            for field in model._meta.many_to_many:
                new_to_process.append(field.rel.to)

        to_process = new_to_process

    return dumpdata.sort_dependencies([(None, (model,)) for model in all_models])
