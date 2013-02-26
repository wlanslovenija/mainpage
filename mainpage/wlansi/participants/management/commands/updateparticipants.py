import os, unicodedata

from django.conf import settings
from django.core.management import base
from django.db import transaction
from django.utils import encoding

import git

import reversion

from mainpage.wlansi.participants import models

class Command(base.NoArgsCommand):
    """
    This class defines a command for manage.py which updates
    database of participants with code authors in git repositories.
    """

    help = "Updates database of participants with code authors in git repositories."

    @reversion.create_revision()
    def handle_noargs(self, **options):
        """
        Updates database of participants with code authors in git repositories.
        """

        verbosity = int(options.get('verbosity'))
        repositories_dir = getattr(settings, 'GIT_REPOSITORIES_DIR', None)
        
        if not repositories_dir:
            return

        for name in os.listdir(repositories_dir):
            repository_path = os.path.abspath(os.path.join(repositories_dir, name))

            if not os.path.isdir(repository_path):
                continue

            try:
                repository = git.Repo(repository_path)
            except git.exc.InvalidGitRepositoryError:
                continue

            if verbosity > 1:
                self.stdout.write("Processing '%s'.\n" % repository_path)

            names = set()
            for head in repository.heads:
                for entry in head.commit.iter_parents():
                    names.add(entry.author.name)

            if verbosity > 1:
                self.stdout.write("Found %s participants.\n" % len(names))

            for name in names:
                name = unicodedata.normalize('NFC', encoding.smart_unicode(name))
                try:
                    models.Participant.objects.get(name=name)
                except models.Participant.DoesNotExist:
                    if verbosity > 1:
                        self.stdout.write("Adding '%s'.\n" % encoding.smart_str(name))
                    models.Participant.objects.create(name=name, source='git', internal_comment="Source code contributor.")

        transaction.commit_unless_managed()
