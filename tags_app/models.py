from django.db import models
from django.utils.translation import ugettext_lazy as _ 

__all__ = [
    'TaggedObjectManager', 
    'Tag',
    'TagMeta'
]

class TaggedObjectManager(models.Manager):

    def get_tags(self, objs):
        tt = self.model.tags.through
        tt_filter = '%s__in' % (self.tagged_field_through)
        obj_id_list = set(x.id for x in objs)
        tag_q = tt.objects.filter(**{tt_filter: obj_id_list}).select_related("tag")
        tag_c = {}

        tft_key = "%s_id" % (self.tagged_field_through)
        for t in tag_q:
            obj_key = getattr(t, tft_key)
            if not obj_key in tag_c:
                tag_c[obj_key] = set()
            tag_c[obj_key].add(t._tag_cache)

        return tag_c


class Tag(models.Model):
    tagline = models.CharField(max_length=100, verbose_name=_("Tag"), unique=True)

    def __unicode__(self):
        return self.tagline

class TagMeta(models.base.ModelBase):

    def __new__(cls, name, bases, attrs):

        tag_model = Tag
        if "Meta" in attrs and hasattr(attrs["Meta"], "tag_model"):
            tag_model = attrs["Meta"].tag_model
            if not isinstance(tag_model, Tag):
                raise TypeError("\"tag_model\" instance should be of Tag type")

        attrs["tags"] = models.ManyToManyField(tag_model, null=True, blank=True)
        attrs["tagged_field_through"] = name.lower()
        new_class = super(TagMeta, cls).__new__(cls, name, bases, attrs)


        return new_class