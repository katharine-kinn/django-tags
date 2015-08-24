=====
Tags
=====

django-tags-app is a simple app to add tags to your existing models.
It features special TagMeta class derived from django.models.base.ModelBase, 
which adds 'tags' ManyToMany field and 'get_tags' method to chosen model.

Quick start
-----------

1. Add "tags_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'tags_app',
    )

Usage
-----

    from tags_app import models as tag_models
    ...
    class TaggedItem(models.Model):
        __metaclass__ = tag_models.TagMeta
