from django.conf import settings

from filer.models import foldermodels, imagemodels

def global_vars(request):
    """
    Adds global context variables to the context.
    """

    supporters_images = {}
    try:
        for supporter in foldermodels.Folder.objects.get(name=settings.SUPPORTERS_FILER_FOLDER_NAME).files.instance_of(imagemodels.Image).filter(is_public=True).order_by('name'):
            if '-color' in supporter.label:
                name = supporter.label.replace('-color', '')
                supporters_images.setdefault(name, {})['color'] = supporter
            elif '-gray' in supporter.label:
                name = supporter.label.replace('-gray', '')
                supporters_images.setdefault(name, {})['gray'] = supporter
    
    except foldermodels.Folder.DoesNotExist:
       pass
    
    supporters = []
    for name, images in supporters_images.items():
        if len(images) != 2:
            continue

        images['label'] = name

        supporters.append(images)

    return {
        'supporters': supporters,
    }
