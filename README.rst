=====
Tags
=====

django-tags-app is a simple app to add tags to your existing models.
It features special TagMeta class derived from django.models.base.ModelBase, 
which adds 'tags' ManyToMany field method to chosen model. 

Quick start
-----------

1. Add "tags_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'tags_app',
    )

Usage
-----

1. Set TagMeta as metaclass of your tagged model::

    from tags_app import models as tag_models
    ...
    class TaggedItem(models.Model):
        __metaclass__ = tag_models.TagMeta

2. To fetch model objects' tags as dictionary set model manager to tag_models.TaggedObjectManager subclass 
and use its get_tags method::

    Model.objects.get_tags((model_object_1, model_object_2...))

3. To use special tag input in your model forms::

	from tags_app import forms as tag_forms
	...
	TaggedItemTagForm = tag_forms.tag_form_class_factory(TaggedItem, bases=())
	...
	tagged_item_form = TaggedItemTagForm(instance=tagged_item)

