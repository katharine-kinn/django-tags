from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from tags_app.models import Tag

class TagStringInput(forms.TextInput):

    def render(self, name, value, attrs=None):

    	attrs.update({"style":"margin-right:10px"})

        html = super(TagStringInput, self).render(name, value, attrs)

        text = _("Enter tags separating them with comma")
        textHtml = format_html(
        	u'<span class="regularText" style="color:white; padding:0px; margin:3px 0px; vertical-align:top; font-size:0.7em" >{0}</span><br>',
        	text,
        )
        html = format_html(
        	u'{0}{1}',
        	html,
        	textHtml,
        )

        return mark_safe(html)

class TagInputForm(forms.Form):

	class Meta:
		abstract = True

	tags_to_add = forms.CharField(max_length=255, label=_("Tags"), widget=TagStringInput())

	def __init__(self, *args, **kwargs):
		instance = None
		if "instance" in kwargs:
			instance = kwargs.pop("instance")
		super(TagInputForm, self).__init__(*args, **kwargs)

		self.initial = {'tags_to_add':_("Add tags...")}
		if instance:
			tag_str = ''
			tag_ids = self.tagged_instance_type.tags.through.objects.filter(
                    **{instance.tagged_field_through: instance.id}
                ).values_list('tag', flat=True)

			if tag_ids:
				self.tag_ids = tag_ids
				tags = Tag.objects.filter(id__in=tag_ids)
				for tag in list(tags):
					tag_str += tag.tagline
					tag_str += ", "
				tag_str = tag_str[:-2]
				self.initial = {'tags_to_add':tag_str}	

	def clean_tags_to_add(self):
		tags_string = self.cleaned_data.get('tags_to_add')
		if tags_string == self.initial.get("tags_to_add"):
			tags_string = ''
		return tags_string

	def save(self, *args, **kwargs):
		
		instance = args[0].get("instance")

		tags_string = self.cleaned_data.get('tags_to_add')
		if tags_string and tags_string != '':
			tags_list = tags_string.split(",")
			for tag in tags_list:
				tag = tag.strip()
				tag_obj = None
				existing_tags = Tag.objects.filter(tagline__iexact=tag)
				if len(existing_tags) > 0:
					tag_obj = existing_tags[0]
				else:
					tag_obj = Tag(tagline=tag)
				tag_obj.save()

				if instance:
					if not self.tagged_instance_type.tags.through.objects.filter(tag=tag_obj).filter(**{self.tagged_instance_type.tagged_field_through: instance}):
						relation = self.tagged_instance_type.tags.through(**{self.tagged_instance_type.tagged_field_through: instance, "tag":tag_obj})
						relation.save()

def tag_form_class_factory(cls, bases=()):

	if not "tags" in dir(cls):
		raise TypeError("Class %s for form should have \"tags\" field" % (cls.__name__))

	if not isinstance(bases, tuple):
		bases = (bases,)
	b = bases + (TagInputForm, )

	return type(cls.__name__ + "TagInputForm", b, {'tagged_instance_type': cls})