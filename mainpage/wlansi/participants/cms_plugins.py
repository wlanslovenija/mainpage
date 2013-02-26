import itertools

from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from . import models

def user_name(user):
    if user.get_full_name() and user.get_profile().attribution == 'name':
        yield user.get_full_name()
    elif user.get_profile().attribution != 'nothing':
        yield user.username

class ParticipantsPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a list of participants.
    """

    module = 'wlan slovenija'
    name = _("Participants")
    render_template = 'participants/list.html'

    def render(self, context, instance, placeholder):
        participants = []

        # Donors-only are not listed in participants, but under supporters

        # Manually added participants or from external sources
        participants.extend(models.Participant.objects.filter(duplicate_of=None, user=None).values_list('name', flat=True))
        # Mapped participants to users
        participants.extend(itertools.chain(*(user_name(participant.user) for participant in models.Participant.objects.filter(duplicate_of=None).exclude(user=None))))
        # Users with at least one node
        participants.extend(itertools.chain(*(user_name(user) for user in auth_models.User.objects.exclude(node=None))))
        # Users with a blog entry
        participants.extend(itertools.chain(*(user_name(user) for user in auth_models.User.objects.filter(entrytitle__entry__is_published=True).order_by().distinct())))

        participants = sorted(set(participants), key=unicode.lower)
        context.update({
            'participants': participants,
        })
        return context

plugin_pool.register_plugin(ParticipantsPlugin)
