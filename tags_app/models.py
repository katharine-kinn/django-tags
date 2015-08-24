from django.db import models
from django.utils.translation import ugettext_lazy as _ 

# Create your models here.

class Tag(models.Model):
	tagline = models.CharField(max_length=100, verbose_name=_("Tag"), unique=True)

	def __unicode__(self):
		return self.tagline

class TagMeta(models.base.ModelBase):
	""" 
		Metaclass to use with models which need tags.
		When set as __metaclass__ of model, it creates ManyToManyField 'tags' on this model
		and adds two methods to operate model's tags. 
	"""

	def __new__(cls, name, bases, attrs):

		tag_model = Tag
		if "Meta" in attrs and hasattr(attrs["Meta"], "tag_model"):
			tag_model = attrs["Meta"].tag_model
			if not isinstance(tag_model, Tag):
				raise TypeError("\"tag_model\" instance should be of Tag type")

		attrs["tags"] = models.ManyToManyField(tag_model, null=True, blank=True)
		attrs["tagged_field_through"] = name.lower()
		new_class = super(TagMeta, cls).__new__(cls, name, bases, attrs)

		def get_tags_list(self):
			tags = type(self).tags.through.objects.filter(**{ self.tagged_field_through: self.id }).values_list('tag', flat=True)
			tags_list = tag_model.objects.filter(id__in=tags).values_list('tagline', flat=True)
			return list(tags_list)

		def get_tags(self):
			tags = type(self).tags.through.objects.filter(**{ self.tagged_field_through: self.id }).values_list('tag', flat=True)
			tags_list = tag_model.objects.filter(id__in=tags)
			return list(tags_list)

		setattr(new_class, 'get_tags_list', get_tags_list)
		setattr(new_class, 'get_tags', get_tags)

		return new_class